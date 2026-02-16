import logging
import os
from typing import List, ClassVar
import settings
import re
from BaseClasses import Tutorial, ItemClassification
# from Fill import fast_fill
from worlds.LauncherComponents import launch_subprocess
from worlds.AutoWorld import World, WebWorld
from .items import ALL_ITEMS, ITEMS_COUNT, EVENT_ITEMS, CLASS_ITEM_CHECK, EXTRA_FILLER_ITEMS, SPRINT_ITEM_CHECK
from .locations import location_init, remove_locations, REMOVED_LOCATIONS
from .regions import create_and_link_regions
from .options import DRGOptions
from .subclasses import DRGItem, DRGLocation
import json
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from .web_world import DRGWebWorld

class DRGSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Path to Deep Rock Galactic installation subfolder "Mods" inside FSD. Should contain the readme.txt
        Should look like :...\\Deep Rock Galactic\\FSD\\Mods
        By Default this assumes you have DRG installed on C drive in standard location.
        """
        description = r"Please Select the <DRG Install Directory>/FSD/Mods Folder"
    root_directory: RootDirectory = RootDirectory(None)

def launch_client():
    from .client import launch
    launch_subprocess(launch, name='DRG Client')
    
components.append(Component("DRG Client",
                            func=launch_client,
                            component_type=Type.CLIENT))

class DRGWorld(World):
    game = 'Deep Rock Galactic'
    web = DRGWebWorld()
    options_dataclass = DRGOptions
    options: DRGOptions
    settings: DRGSettings
    item_name_to_id = ALL_ITEMS
    location_name_to_id = location_init()
    event_items={}

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    def fill_slot_data(self) -> dict:
        slot_data = {}
        
        slot_data.update(self.options.as_dict('death_link','death_link_all','death_link_failure','goal_mode',\
            'error_cube_checks','avail_classes','traps_on','minigames_on','minigame_num','coin_shop_prices',\
            'gold_to_coin_rate','beermat_to_coin_rate','progression_diff','starting_stats',\
            'gold_rush_val','shop_item_num','events_on','max_hazard','hunter_trophies',\
            'hunter_targets','sprint_start'))
        
        ShopItemsDict = {}
        for i in range(1,(int(self.options.shop_item_num.value) + 1)): 
            thisLoc = self.multiworld.get_location(f"Shop Item:{i}", self.player)
            ShopItemsDict[f"Shop Item:{i}"] = {"player" : int(thisLoc.item.player), "item" : str(thisLoc.item.name)}

        slot_data.update({"shop_items" : ShopItemsDict})

        slot_data.update({"removed_locations" : REMOVED_LOCATIONS})

        return slot_data

    def create_item(self, item_name: str, item_classification = ItemClassification.filler) -> DRGItem:
        '''
        Returns created DRGItem
        '''
        created_item = DRGItem(item_name, item_classification, self.item_name_to_id[item_name], self.player)
        return created_item

    # def create_event(self, item_name: str) -> DRGItem:
        # item_classification = ItemClassification.progression
        # created_item = DRGItem(item_name, item_classification, 2^20-7, self.player) # id is None, so it's an event.
        # return created_item

    def create_item_filler_random(self) -> str:
        '''
        Returns random filler item.
        '''
        item_name = self.random.choice(EXTRA_FILLER_ITEMS)
        item_classification = ItemClassification.filler
        created_item = DRGItem(item_name, item_classification, self.item_name_to_id[item_name], self.player)

    def create_items(self) -> None:
        '''
        Fills ItemPool..
        '''
        
        item_pool = []
        movement_remove = 0
        for item_name in ALL_ITEMS:
            #skip event items because they have set locations
            if item_name in EVENT_ITEMS:
                continue
            #skip junk items because they're junk
            if item_name in EXTRA_FILLER_ITEMS:
                continue
            counts = ITEMS_COUNT[item_name]
            #skip adding classes to item pool because they start unlocked
            if (item_name in CLASS_ITEM_CHECK) and (self.options.avail_classes.value == 0):
                continue
            #skip adding movespeed to pool if starting with sprint allowed
            if (item_name in SPRINT_ITEM_CHECK) and (self.options.sprint_start.value == 1) and (movement_remove <= 3):
                movement_remove += 1
                continue
            #generate Rest of Items
            item_pool += [self.create_item(item_name, ItemClassification.progression) for _ in range(counts.progression)]
            item_pool += [self.create_item(item_name, ItemClassification.useful     ) for _ in range(counts.useful     )]
            item_pool += [self.create_item(item_name, ItemClassification.filler     ) for _ in range(counts.filler     )]
            if bool(self.options.traps_on):
                item_pool += [self.create_item(item_name, ItemClassification.trap       ) for _ in range(counts.trap       )]

        #fill as needed
        Unfilled_Locations = len(self.multiworld.get_unfilled_locations(self.player))
        Needed_Filler = Unfilled_Locations - len(item_pool) #- 1 #for range fix
        if Needed_Filler < 0:
            print(f"You've generated a negative number of unfilled locations. Generally this means some math went wrong with too many items.")
        if Needed_Filler > 0:
            print(f"Extra Items Needed:{Needed_Filler} = {Unfilled_Locations} - {len(item_pool)}")
            item_pool += [self.create_item(self.random.choice(EXTRA_FILLER_ITEMS), ItemClassification.filler) for _ in range(Needed_Filler)]
        
        #add to multiworld pool
        self.multiworld.itempool += item_pool
        
    def get_pre_fill_items_dictionary(self):
        # raise Exception()
        for item_name in EVENT_ITEMS:
            event_item =self.create_item(item_name,ItemClassification.progression)
            self.event_items[item_name] = event_item
        return self.event_items
        
    def checkSlotName(self):
        # The pattern explanation:
        # ^ : Matches the start of the string.
        # [a-zA-Z0-9_] : Matches any lowercase letter, uppercase letter, digit, or underscore.
        # * : Matches zero or more repetitions of the preceding character class.
        # $ : Matches the end of the string.
        pattern = '^[a-zA-Z0-9_]*$'
        if re.match(pattern, self.player_name): #Check if all characters are valid
            print("Slot Name is valid for DRG.")
        else:
            raise ValueError("DRG Slot names cannot contain anything but letters, numbers, and underscores. Please rename your slot.")

    def generate_early(self) -> None:
        '''
        Run early, after options are parsed but before locations or items are created.
        Execute /some/ options based stuff, like location deletions
        '''
        self.location_name_to_id = location_init()#int(self.options.error_cube_checks.value),bool(self.options.minigames_on.value))

        #try:
            #self.checkSlotName()
        #except ValueError as e:
            #print(f"Error: {e}")
            # Pause the program, waiting for the user to press the Enter key
            #input("Press the <Enter> key to exit the program.")
            # Exit the program with an error status code
            #import sys
            #sys.exit(1) #

        #print(f"{self.location_name_to_id}")
        # currently running remove locations in _regions.py
        return
    
    #moved from above
    # location_name_to_id = None 

    def pre_fill(self):
        '''
        things to do before AP fills stuff
        ie: set progression items in own world, etc...
        '''
        self.get_pre_fill_items_dictionary()
        victory_item=self.event_items['Victory']

        #print(f'Goal Mode Val:{self.options.goal_mode.value}')
        if self.options.goal_mode.value == 2: #goldrush win condition
            self.multiworld.get_location("Gold Rush:RICH", self.player).place_locked_item(victory_item)
        elif self.options.goal_mode.value == 3: #trophy hunter win condition
            self.multiworld.get_location("Trophy Hunter:MASTERED", self.player).place_locked_item(victory_item)
        else: #default win condition = Haz 5 Caretaker
            self.multiworld.get_location("OBJ:Magma Core:Industrial Sabotage:5", self.player).place_locked_item(victory_item)
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        

    def create_regions(self):
        '''
        Creates the Regions and Connects them.
        '''
        difficulty = [5,10,25,4,3,2] #Deault Easy [Haz3, Haz4, Haz5, Carry, Morkite, Ammo] Prog / 122
        match int(self.options.progression_diff.value):
            case 1: #leaflover / easy
                difficulty = [2,8,10,2,1,1] #10%
            case 2: #normal
                difficulty = [5,10,25,3,2,2] #20%
            case 3: #hard
                difficulty = [10,20,40,4,3,2] #33%
            case 4: #lethal
                difficulty = [20,40,60,6,3,3] #50%
            case 5: #karl
                difficulty = [30,60,90,8,3,4] #75%
            case _: #default
                difficulty = [5,10,25,3,2,2] #20%

        match int(self.options.max_hazard.value):
            case 3: #haz 3 max
                if int(self.options.progression_diff.value) >= 3: #progression too steep
                    difficulty = [10,10,10,4,3,2] #33%
            case 4:
                if int(self.options.progression_diff.value) >= 4: #progression too steep
                    difficulty = [20,30,30,4,3,2] #50%

        create_and_link_regions(self.multiworld, self.player, self.options, self.location_name_to_id, difficulty)

    def set_rules(self):
        '''
        Sets the Logic for the Regions and Location unlocks.
        '''
        # universal_logic = Rules.KH2WorldRules(self)
        # form_logic = Rules.KH2FormRules(self)
        # fight_rules = Rules.KH2FightRules(self)
        # fight_rules.set_kh2_fight_rules()
        # universal_logic.set_kh2_rules()
        # form_logic.set_kh2_form_rules()
        print('TODO: rules')

    def generate_output(self, output_directory: str):
        '''
        Generate Option File
        '''
        return

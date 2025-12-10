import logging
import os
from typing import List, ClassVar
import settings
from BaseClasses import Tutorial, ItemClassification
# from Fill import fast_fill
from worlds.LauncherComponents import launch_subprocess
from worlds.AutoWorld import World, WebWorld
from .items import ALL_ITEMS, ITEMS_COUNT, EVENT_ITEMS
from .locations import location_init, remove_locations
from .regions import create_and_link_regions
from .options import DRGOptions
from .subclasses import DRGItem, DRGLocation
import json
## BaseDirectory=r"E:\SteamLibrary\steamapps\common\Deep Rock Galactic\FSD\Mods"

#2 lines taken from J&D, not actually sure what's important here, but it works.
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths

class DRGSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Path to Deep Rock Galactic installation subfolder "Mods" inside FSD. Should contain the readme.txt
        Should look like :...\\Deep Rock Galactic\\FSD\\Mods
        By Default this assumes you have DRG installed on C drive in standard location.
        """
        description = r"DRG needs /FSD/Mods folder Directory"
    root_directory: RootDirectory = RootDirectory(r"C:/Program Files (x86)/Steam/steamapps/common/Deep Rock Galactic/FSD/Mods")

def launch_client():
    from .client import launch
    launch_subprocess(launch, name='DRG Client')
    
components.append(Component("DRG Client",
                            func=launch_client,
                            component_type=Type.CLIENT))

class DRGWebWorld(WebWorld):
    theme = 'stone'

class DRGWorld(World):
    game = 'Deep Rock Galactic'
    web = DRGWebWorld()
    options_dataclass = DRGOptions
    options: DRGOptions
    settings: ClassVar[DRGSettings]

    item_name_to_id = ALL_ITEMS
    location_name_to_id = location_init()
    #location_name_to_id = location_init(int(self.options.error_cube_count.value),bool(self.options.minigames_on.value))
    event_items={}

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    def fill_slot_data(self) -> dict:
        slot_data = {}
        
        slot_data.update(self.options.as_dict('death_link','death_link_all','goal_mode',\
            'error_cube_checks','avail_classes','traps_on','minigames_on','coin_shop_prices',\
            'gold_to_coin_rate','beermat_to_coin_rate','progression_diff'))
        
        ShopItemsDict = {}
        for i in range(1,26):
            thisLoc = self.multiworld.get_location(f"Shop Item:{i}", self.player)
            ShopItemsDict[f"Shop Item:{i}"] = {"player" : int(thisLoc.item.player), "item" : str(thisLoc.item.name)}

        slot_data.update({"shop_items" : ShopItemsDict})

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
        item_name = self.random.choice(FILLER_ITEMS)
        item_classification = ItemClassification.filler
        created_item = DRGItem(item_name, item_classification, self.item_name_to_id[item_name], self.player)

    def create_items(self) -> None:
        '''
        Fills ItemPool..
        '''
        
        item_pool = []
        for item_name in ALL_ITEMS:
            if item_name in EVENT_ITEMS:
                continue
            counts = ITEMS_COUNT[item_name]
            item_pool += [self.create_item(item_name, ItemClassification.progression) for _ in range(counts.progression)]
            item_pool += [self.create_item(item_name, ItemClassification.useful     ) for _ in range(counts.useful     )]
            item_pool += [self.create_item(item_name, ItemClassification.filler     ) for _ in range(counts.filler     )]
            if bool(self.options.traps_on):
                item_pool += [self.create_item(item_name, ItemClassification.trap       ) for _ in range(counts.trap       )]
        # if len(item_pool) != len(ALL_LOCATIONS):
            # print(f'something really bad happened! AP created {len(item_pool)} items, but found {len(ALL_LOCATIONS)} locations. These two numbers should be the same!')
        # alternatively, we can pad with fillers. This is usually the option when you may have variable numbers of locations (ie: sanity)
        # Creating filler for unfilled locations. Should do something more intelligent for tracking # known and ACTIVE locations.
        # item_pool += [self.create_item_filler_random() for _ in range(len(ALL_LOCATIONS) - len(item_pool))]        
        self.multiworld.itempool += item_pool
        
    def get_pre_fill_items_dictionary(self):
        # raise Exception()
        for item_name in EVENT_ITEMS:
            event_item =self.create_item(item_name,ItemClassification.progression)
            self.event_items[item_name] = event_item
        return self.event_items
        
    def checkSlotName(self):
        if ' ' in self.player_name:
            raise ValueError("DRG Slot names cannot contain spaces. Please use underscores if needed.")
        else:
            print("Slot Name is valid for DRG.")

    def generate_early(self) -> None:
        '''
        Run early, after options are parsed but before locations or items are created.
        Execute /some/ options based stuff, like location deletions
        '''
        self.location_name_to_id = location_init()#int(self.options.error_cube_checks.value),bool(self.options.minigames_on.value))

        try:
            self.checkSlotName()
        except ValueError as e:
            print(f"Error: {e}")
            # Pause the program, waiting for the user to press the Enter key
            input("Press the <Enter> key to exit the program.")
            # Exit the program with an error status code
            import sys
            sys.exit(1) #

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

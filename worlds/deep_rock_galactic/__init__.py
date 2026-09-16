import logging
import os
from typing import List, ClassVar
import settings
import re
import random
from BaseClasses import Tutorial, ItemClassification
# from Fill import fast_fill
from worlds.LauncherComponents import launch_subprocess
from worlds.AutoWorld import World, WebWorld
from .items import ALL_ITEMS, ITEMS_COUNT, EVENT_ITEMS, CLASS_ITEM_CHECK, EXTRA_FILLER_ITEMS, SPRINT_ITEM_CHECK, BIOME_ITEM_CHECK, WEAPONS_PRIMARY, WEAPONS_SECONDARY, DEPRECIATED_ITEMS, GAUNTLET_ITEMS
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
                            component_type=Type.CLIENT, 
                            icon='drg'))

icon_paths['drg'] = f"ap:{__name__}/icons/icon_drg.png"

@staticmethod
def create_groups(obj: dict[str, ITEMS_COUNT]) -> dict[str, set[str]]:
    groups: dict[str, set[str]] = dict()
    for key, data in obj.items():
        if data.tags is None:
            continue
        for tag in data.tags:
            tag_name = tag.name.replace('_', ' ')
            if tag_name not in groups:
                groups[tag_name] = set()
            groups[tag_name].add(str(key))
    return groups

class DRGWorld(World):
    game = 'Deep Rock Galactic'
    web = DRGWebWorld()
    options_dataclass = DRGOptions
    options: DRGOptions
    settings: DRGSettings
    item_name_to_id = ALL_ITEMS
    item_name_groups = create_groups(ITEMS_COUNT)
    location_name_to_id = location_init()
    event_items={}
    randClass=1 #Gunner

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    def fill_slot_data(self) -> dict:
        slot_data = {}
        
        slot_data.update(self.options.as_dict('death_link','death_link_all','death_link_failure','goal_mode',\
            'error_cube_checks','avail_classes','traps_on','minigames_on','minigame_num','coin_shop_prices',\
            'gold_to_coin_rate','beermat_to_coin_rate','progression_diff','starting_stats',\
            'gold_rush_val','shop_item_num','events_on','max_hazard','hunter_trophies',\
            'hunter_targets','hunter_bosses','hunter_trophies_b','sprint_start','biome_start','biome_end',\
            'wep_rando','gauntlet_stages','gauntlet_seed','gauntlet_start','gold_rush_increment',\
            'blacklist_biome','blacklist_obj','blacklist_sec','blacklist_warn'))
        
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
        
        #set all item pools
        item_pool_final = []
        items_required = []
        items_mandatory = []
        items_useful = []
        items_filler = []
        items_traps = []

        #Check for gauntlet manditory stages first
        if(self.options.goal_mode.value == 4):
            stagesToAdd = self.options.gauntlet_stages.value - self.options.gauntlet_start.value
            items_mandatory += [self.create_item('Progressive-Gauntlet-Stage', ItemClassification.progression) for _ in range(stagesToAdd)]

        #START ITEM LOOP
        movement_remove = 0
        for item_name in ALL_ITEMS:
            #skip event items because they have set locations
            if item_name in EVENT_ITEMS:
                continue
            #skip junk items because they're junk
            if item_name in EXTRA_FILLER_ITEMS:
                continue
            #skip gauntlet items because they're already handled
            if item_name in GAUNTLET_ITEMS:
                continue
            #skip depreciated items because they're no longer used (remain for old world support only)
            if item_name in DEPRECIATED_ITEMS:
                continue
            #skip adding classes to item pool because they start unlocked
            if (item_name in CLASS_ITEM_CHECK) and (self.options.avail_classes.value == 0):
                continue
            #skip specific class if on
            if (item_name in CLASS_ITEM_CHECK) and (self.options.avail_classes.value not in [0,5]):
                if (item_name == CLASS_ITEM_CHECK[(self.options.avail_classes.value-1)]):
                    continue
            #skip adding biomes to item pool because they start unlocked
            if (item_name in BIOME_ITEM_CHECK) and ((self.options.biome_start.value == 0) or (self.options.goal_mode.value != 1)):
                continue
            #skip adding movespeed to pool if starting with sprint allowed
            if (item_name in SPRINT_ITEM_CHECK) and (self.options.sprint_start.value == 1) and (movement_remove <= 3):
                movement_remove += 1
                continue
            #skip weapon rando if ignored
            if (item_name in WEAPONS_PRIMARY or item_name in WEAPONS_SECONDARY) and (self.options.wep_rando.value == 0):
                continue
            #skip weapon if selected
            if (item_name in WEAPONS_PRIMARY and self.options.wep_rando.value == 2):
                if (item_name == WEAPONS_PRIMARY[self.options.wep_primary.value]):
                    continue
            if (item_name in WEAPONS_SECONDARY and self.options.wep_rando.value == 2):
                if (item_name == WEAPONS_SECONDARY[self.options.wep_secondary.value]):
                    continue

            counts = ITEMS_COUNT[item_name]
            #generate Rest of Items
            items_mandatory += [self.create_item(item_name, ItemClassification.progression) for _ in range(counts.mandatory)]
            items_required += [self.create_item(item_name, ItemClassification.progression) for _ in range(counts.progression)]
            items_useful += [self.create_item(item_name, ItemClassification.useful     ) for _ in range(counts.useful     )]
            items_filler += [self.create_item(item_name, ItemClassification.filler     ) for _ in range(counts.filler     )]
            if bool(self.options.traps_on):
                items_traps += [self.create_item(item_name, ItemClassification.trap       ) for _ in range(counts.trap       )]
            #FINISHED ITEM LOOP
        
        #fill as needed
        Total_Locations = len(self.multiworld.get_unfilled_locations(self.player)) - 1 #fixes for victory location
        Max_Items = len(items_mandatory) + len(items_required) + len(items_useful) + len(items_filler) + len(items_traps)
        Needed_Items = Total_Locations - Max_Items #for range fix
        
        if Needed_Items < 0: #too many items, so remove some
            print(f"DRG - Too Many Items: {Needed_Items} = I({Max_Items}) - L({Total_Locations}), Adjusting Items Down")
            #needs < mandatory
            if(Total_Locations < len(items_mandatory)): 
                for item in items_mandatory:
                    if(len(item_pool_final) < Total_Locations):
                        item_pool_final.append(item)
                print(f"DRG - Too Few Locations for Required Items: {len(item_pool_final)}. Not all Mandatory Items placed! Add More Locations to your Yaml.")
            #needs mandatory + some required
            elif(len(items_mandatory) <= Total_Locations <= (len(items_mandatory)+len(items_required))): 
                item_pool_final.extend(items_mandatory)
                for item in items_required:
                    if(len(item_pool_final) < Total_Locations):
                        item_pool_final.append(item)
                print(f"DRG - Generated mandatory + some required: {len(item_pool_final)}")
            #needs mandatory, required + some useful
            elif((len(items_mandatory)+len(items_required)) <= Total_Locations <= (len(items_mandatory)+len(items_required)+len(items_useful))): 
                item_pool_final.extend(items_mandatory)
                item_pool_final.extend(items_required)
                for item in items_useful:
                    if(len(item_pool_final) < Total_Locations):
                        item_pool_final.append(item)
                print(f"DRG - Generated mandatory + required + some useful: {len(item_pool_final)}")
            #needs manditory + required + useful + some filler
            elif((len(items_mandatory)+len(items_required)+len(items_useful)) <= Total_Locations <= (len(items_mandatory)+len(items_required)+len(items_useful)+len(items_filler))): 
                item_pool_final.extend(items_mandatory)
                item_pool_final.extend(items_required)
                item_pool_final.extend(items_useful)
                for item in items_filler:
                    if(len(item_pool_final) < Total_Locations):
                        item_pool_final.append(item)
                print(f"DRG - Generated required + useful + some filler: {len(item_pool_final)}")
            #needs required + useful + some filler + traps
            else: 
                item_pool_final.extend(items_mandatory)
                item_pool_final.extend(items_required)
                item_pool_final.extend(items_useful)
                item_pool_final.extend(items_filler)
                for item in items_traps:
                    if(len(item_pool_final) < Total_Locations):
                        item_pool_final.append(item)
                print(f"DRG - Generated required + useful + filler + some traps: {len(item_pool_final)}")
        #needs more items, so add filler
        elif Needed_Items > 0: 
            print(f"DRG - Extra Items Needed: {Needed_Items} = L({Total_Locations}) - I({Max_Items}), Generating Extras")
            item_pool_final.extend(items_mandatory)
            item_pool_final.extend(items_required)
            item_pool_final.extend(items_useful)
            item_pool_final.extend(items_filler)
            item_pool_final.extend(items_traps)
            item_pool_final += [self.create_item(self.random.choice(EXTRA_FILLER_ITEMS), ItemClassification.filler) for _ in range(Needed_Items)]
            print(f"DRG - Generated + Extras: {len(item_pool_final)}")
        #flawless execution Needed_Items = 0
        else: 
            print(f"DRG - Items Match Perfectly!")
            item_pool_final.extend(items_mandatory)
            item_pool_final.extend(items_required)
            item_pool_final.extend(items_useful)
            item_pool_final.extend(items_filler)
            item_pool_final.extend(items_traps)
        
        #add to multiworld pool
        self.multiworld.itempool += item_pool_final
        
    def get_pre_fill_items_dictionary(self):
        # raise Exception()
        for item_name in EVENT_ITEMS:
            event_item = self.create_item(item_name,ItemClassification.progression)
            self.event_items[item_name] = event_item
        return self.event_items

    def generate_early(self) -> None:
        '''
        Run early, after options are parsed but before locations or items are created.
        Execute /some/ options based stuff, like location deletions
        '''
        self.location_name_to_id = location_init()#int(self.options.error_cube_checks.value),bool(self.options.minigames_on.value))

        #fix matching start and end biomes
        if self.options.biome_start.value == self.options.biome_end.value:
            if self.options.biome_end.value != 7:
                self.options.biome_end.value = 7
                #raise OptionError("DRG - Your Starting and Ending Biomes cannot be the same.")
                print("DRG - Starting and Ending Biome Cannot Match. Ending Biome Changed to Magma Core.")
            else:
                self.options.biome_end.value = 11
                print("DRG - Starting and Ending Biome Cannot Match. Ending Biome Changed to Ossuary Depths.")

        biome_keys = {"azure_weald":"Azure Weald","crystalline_caverns":"Crystalline Caverns","fungus_bogs":"Fungus Bogs","hollow_bough":"Hollow Bough",\
        "glacial_strata":"Glacial Strata","dense_biozone":"Dense Biozone","magma_core":"Magma Core","radioactive_exclusion_zone":"Radioactive Exclusion Zone",\
        "salt_pits":"Salt Pits","sandblasted_corridors":"Sandblasted Corridors","ossuary_depths":"Ossuary Depths"}

        #fix excluded start biome
        if biome_keys[self.options.biome_start.current_key] in self.options.blacklist_biome.value:
            self.options.blacklist_biome.value.discard(biome_keys[self.options.biome_start.current_key])

        #fix excluded end biome
        if biome_keys[self.options.biome_end.current_key] in self.options.blacklist_biome.value:
            self.options.blacklist_biome.value.discard(biome_keys[self.options.biome_end.current_key])

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

        biomeOptionNames = ['Magma Core','Azure Weald','Crystalline Caverns','Fungus Bogs','Hollow Bough','Glacial Strata',\
        'Dense Biozone','Magma Core','Radioactive Exclusion Zone','Salt Pits','Sandblasted Corridors','Ossuary Depths']

        #print(f'Goal Mode Val:{self.options.goal_mode.value}')
        if self.options.goal_mode.value == 2: #goldrush win condition
            self.multiworld.get_location("Gold Rush:RICH", self.player).place_locked_item(victory_item)
        elif self.options.goal_mode.value == 3: #trophy hunter win condition
            self.multiworld.get_location("Trophy Hunter:MASTERED", self.player).place_locked_item(victory_item)
        elif self.options.goal_mode.value == 4: #gauntlet win condition
            self.multiworld.get_location("Gauntlet:Victory", self.player).place_locked_item(victory_item)
        else: #default win condition = Haz 5 Caretaker
            self.multiworld.get_location(f"OBJ:{biomeOptionNames[self.options.biome_end.value]}:Industrial Sabotage:5", self.player).place_locked_item(victory_item)
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        #START - Pecollected Items
        self.randClass = random.randint(1,4) #Gunner, Driller, Scout, Engineer
        preItems = []
        self.chosenClass = 2;
        #START - Class Items
        match (self.options.avail_classes.value):
            case 1: #gunner
                preItems.append("Class-Gunner")
                self.chosenClass = 1;
            case 2: #driller
                preItems.append("Class-Driller")
                self.chosenClass = 2;
            case 3: #scout
                preItems.append("Class-Scout")
                self.chosenClass = 3;
            case 4: #engi
                preItems.append("Class-Engineer")
                self.chosenClass = 4;
            case 5:
                match (self.randClass): #if 5 = random then select 1-4 randomly
                    case 1: #gunner
                        preItems.append("Class-Gunner")
                        self.chosenClass = 1;
                    case 2: #driller
                        preItems.append("Class-Driller")
                        self.chosenClass = 2;
                    case 3: #scout
                        preItems.append("Class-Scout")
                        self.chosenClass = 3;
                    case 4: #engi
                        preItems.append("Class-Engineer")
                        self.chosenClass = 4;
            case _: #all
                preItems.extend(CLASS_ITEM_CHECK)
                self.chosenClass = 2;
        #END - Class Items

        #START - Biome Items
        match (self.options.biome_start.value):
            case 1:
                preItems.append('Biome-Azure-Weald')
            case 2:
                preItems.append('Biome-Crystalline-Caverns')
            case 3:
                preItems.append('Biome-Fungus-Bogs')
            case 4:
                preItems.append('Biome-Hollow-Bough')
            case 5:
                preItems.append('Biome-Glacial-Strata')
            case 6:
                preItems.append('Biome-Dense-Biozone')
            case 7:
                preItems.append('Biome-Magma-Core')
            case 8:
                preItems.append('Biome-Radioactive-Exclusion-Zone')
            case 9:
                preItems.append('Biome-Salt-Pits')
            case 10:
                preItems.append('Biome-Sandblasted-Corridors')
            case 11:
                preItems.append('Biome-Ossuary-Depths')
            case _:
                preItems.extend(BIOME_ITEM_CHECK)
        #END - Biome Items

        #START - Weapon Rando Items
        match (self.options.wep_rando.value):
            case 1:
                if (self.options.avail_classes.value > 0):
                    match (self.chosenClass): #if 5 = random then select 1-4 randomly
                        case 1: #gunner
                            randInt_prim = random.randint(6,8)
                        case 2: #driller
                            randInt_prim = random.randint(0,2)
                        case 3: #scout
                            randInt_prim = random.randint(9,11)
                        case 4: #engi
                            randInt_prim = random.randint(3,5)
                else:    
                    randInt_prim = random.randint(0,len(WEAPONS_PRIMARY)-1)
                match (randInt_prim):
                    case 0 | 1 | 2: #limit to Driller
                        randInt_sec = random.randint(0,2)
                    case 3 | 4 | 5: #limit to Engi
                        randInt_sec = random.randint(3,5)
                    case 6 | 7 | 8: #limit to Gunner
                        randInt_sec = random.randint(6,8)
                    case _: #limit to scout
                        randInt_sec = random.randint(9,11)
                preItems.append(WEAPONS_PRIMARY[randInt_prim])
                preItems.append(WEAPONS_SECONDARY[randInt_sec])
            case 2:
                preItems.append(WEAPONS_PRIMARY[self.options.wep_primary.value])
                preItems.append(WEAPONS_SECONDARY[self.options.wep_secondary.value])
            case _:
                preItems.extend(WEAPONS_PRIMARY)
                preItems.extend(WEAPONS_SECONDARY)
        #END - Wep Rando Settings

        #START - Gauntlet Items
        if(self.options.goal_mode.value == 4):
            for i in range(self.options.gauntlet_start.value):
                preItems.append('Progressive-Gauntlet-Stage')

        if(self.options.gauntlet_help.value == True and self.options.goal_mode.value == 4):
            #100% movement speed, ammo, shield base
            the_kit = ['Progressive-Movement-Speed','Progressive-Movement-Speed',\
            'Progressive-Max-Health','Progressive-Max-Shield','Progressive-Shield-Regen-Delay',\
            'Progressive-Gun-Ammo','Progressive-Gun-Ammo','Progressive-Gun-Ammo','Progressive-Resupply-Incremental-Cost',\
            'Progressive-Resupply-Start-Cost','Progressive-Carrying-Speed','Progressive-Carrying-Speed']
            preItems.extend(the_kit)

        #preFinal = []
        for item in preItems:
            self.multiworld.push_precollected(self.create_item(item, ItemClassification.progression))
        
        #self.multiworld.push_precollected(preFinal)

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
        # print('TODO: rules')

    def generate_output(self, output_directory: str):
        '''
        Generate Option File
        '''
        return

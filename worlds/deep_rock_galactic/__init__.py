import logging
from typing import List
import settings
from BaseClasses import Tutorial, ItemClassification
# from Fill import fast_fill
from worlds.LauncherComponents import launch_subprocess
from worlds.AutoWorld import World, WebWorld
from ._items import ALL_ITEMS, ITEMS_COUNT, EVENT_ITEMS
from ._locations import ALL_LOCATIONS
from ._regions import create_and_link_regions
from ._options import DRGOptions
from ._subclasses import DRGItem
import json

#2 lines taken from J&D, not actually sure what's important here, but it works.
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths

def launch_client():
    from .client import launch
    launch_subprocess(launch, name='DRGClient')
    
components.append(Component("DRGClient",
                            func=launch_client,
                            component_type=Type.CLIENT))

#also taken from J&D, I dont think it works, but haven't tried. Also imported settings in line 3.
# class DRGSettings(settings.Group):
    # class RootDirectory(settings.UserFolderPath):
        # """Path to Mods folder inside FSD containing the readme.txt
        # Should look like :...\Deep Rock Galactic\FSD\Mods"""
        # description = "Text File Directory"
        # root_path = Utils.get_settings()["DRG_options"]["root_directory"]

class DRGWebWorld(WebWorld):
    theme = 'stone'
#No idea what I am doing. Trying to get a prompt to appear and ask user for FSD directory. Was trying to start with getting ANY DIRECTORY
# class DRGSettings(settings.Group):
    # class ModsFolderPath(settings.UserFolderPath):
        # """"Directory that includes Deep Rock Galactic/FSD/Mods"""
        # description = 'Need /FSD/Mods folder from your DRG install.'
        # # ModsPath = settings.Group.__getattribute__(self,'Path')
        # # TextDirectory = settings.FolderPath(ModsPath)

class DRGWorld(World):
    game = 'Deep Rock Galactic'
    web = DRGWebWorld()
    options_dataclass = DRGOptions
    options = DRGOptions

    item_name_to_id = ALL_ITEMS
    location_name_to_id = ALL_LOCATIONS

    event_items={}

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

    def fill_slot_data(self) -> dict:
        slot_data = {}
        slot_data.update(self.options.as_dict('death_link'))
        return slot_data

    def create_item(self, item_name: str, item_classification) -> DRGItem:
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
        
    def generate_early(self) -> None:
        '''
        Run early, after options are parsed but before locations or items are created.
        Execute /some/ options based stuff, like location deletions
        '''
        
        return

    def pre_fill(self):
        '''
        things to do before AP fills stuff
        ie: set progression items in own world, etc...
        '''
        self.get_pre_fill_items_dictionary()
        victory_item=self.event_items['Victory']
        self.multiworld.get_location("Magma Core:Industrial Sabotage:5", self.player).place_locked_item(victory_item)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        

    def create_regions(self):
        '''
        Creates the Regions and Connects them.
        '''
        create_and_link_regions(self.multiworld, self.player)

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
        Does nothing. DRG has no patch file.
        '''
        return

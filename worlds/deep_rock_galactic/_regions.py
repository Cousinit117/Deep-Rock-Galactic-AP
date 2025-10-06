from typing import NamedTuple, Callable

from BaseClasses import CollectionState

from ._subclasses import DRGLocation, DRGRegion
from ._locations import location_init, remove_locations, Biomes, MissionTypes, SecondaryObjectives
from ._items import Generic_Progressives, Carrying_Buffs

class RegionData(NamedTuple):
    locations: list[DRGLocation] = []
    entrancerule: Callable[[CollectionState], bool] = lambda x: True
    connected_regions: list[DRGRegion] = []

def create_region(multiworld, player, name, locations):
    region = DRGRegion(name, player, multiworld)
    region.add_locations(locations, DRGLocation)
    return region

def create_and_link_regions(multiworld, player, options, ALL_LOCATIONS):
    
    def rule_generic_progressive4(state):
        return state.has_from_list(Generic_Progressives,player,6) #This number will need balancing later.
    def rule_generic_progressive5(state):
        return state.has_from_list(Generic_Progressives,player,15) #This number will need heavy balancing later.
    def rule_carrying(state):
        return state.has_from_list(Carrying_Buffs,player,4) #This number will likely be in the range of 4-8.
    def rule_morkite(state):
        return state.has('Progressive-Morkite-Mining',player,3) #This number is safe at 3. As far as a tracker goes, MAY be completable at 2. sometimes     
    def rule_ammo(state):
        return state.has('Progressive-Gun-Ammo',player,2) #Requires at least 2 ammo buffs

    MissionsDefault=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and ('1' in Mission or '2' in Mission or '3' in Mission)
        ]
        
    MissionsDefaultHaz4=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'Elimination' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and '4' in Mission
        ]

    MissionsDefaultHaz5=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'Elimination' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and '5' in Mission
        ]
    
    MissionsAmmo123=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('1' in Mission or '2' in Mission or '3' in Mission)
        ]

    MissionsAmmo4=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('4' in Mission)
        ]

    MissionsAmmo5=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('5' in Mission)
        ]
    
    MissionsCarrying123=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and ('1' in Mission or '2' in Mission or '3' in Mission)
        ]

    MissionsCarrying4=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and '4' in Mission
        ]

    MissionsCarrying5=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and '5' in Mission
        ]

    MissionsMining123=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and ('1' in Mission or '2' in Mission or '3' in Mission)
        ]

    MissionsMining4=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and '4' in Mission
        ]
    
    MissionsMining5=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and '5' in Mission
        ]

    #Only one not plural. You probably hate it, change if you want
    MissionVictory=[Mission for Mission in ALL_LOCATIONS if
        'Industrial Sabotage' in Mission \
        and '5' in Mission
        ]

    SecondariesDefault=[Secondary for Secondary in ALL_LOCATIONS if (
        'Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or 'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Scan' in Secondary)
        ]

    SecondariesCarrying=[Secondary for Secondary in ALL_LOCATIONS if ('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary)]

    SecondariesAmmo=[Secondary for Secondary in ALL_LOCATIONS if 'Elimination Eggs' in Secondary]
    
    REGIONS = {
        'Menu': RegionData(connected_regions=['AlwaysAccessLocations', 'AlwaysAccessSecondaries', 'GenericHaz4', 'GenericHaz5', \
        'Mining123', 'Mining4', 'Mining5', 'Ammo123', 'Ammo4', 'Ammo5', 'AmmoSecondary', 'Carrying123', 'Carrying4', 'Carrying5','CarryingSecondary','VictoryAccess']), 
        # Should contain all
        
        'AlwaysAccessLocations': RegionData(
            locations    = MissionsDefault,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'AlwaysAccessSecondaries': RegionData(
            locations    = SecondariesDefault,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'GenericHaz4': RegionData(
            locations    = MissionsDefaultHaz4,
            entrancerule = lambda state:    rule_generic_progressive4(state),
            connected_regions        = [],
        ), # Haz 4 will require N progressives for access rule
        'GenericHaz5': RegionData(
            locations    = MissionsDefaultHaz5,
            entrancerule = lambda state:    rule_generic_progressive5(state),
            connected_regions        = [],
        ),  #Haz 5 will require N progressives for access rule
        
        #Mining missions require Progressive morkite checks to be completable
        'Mining123': RegionData(
            locations    = MissionsMining123,
            entrancerule = lambda state:    rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining4': RegionData(
            locations    = MissionsMining4,
            entrancerule = lambda state:    rule_morkite(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining5': RegionData(
            locations    = MissionsMining5,
            entrancerule = lambda state:    rule_morkite(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Elimination missions require Progressive ammo checks to be completable
        'Ammo123': RegionData(
            locations    = MissionsAmmo123,
            entrancerule = lambda state:    rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo4': RegionData(
            locations    = MissionsAmmo4,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo5': RegionData(
            locations    = MissionsAmmo5,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'AmmoSecondary': RegionData(
            locations    = SecondariesAmmo,
            entrancerule = lambda state:    rule_ammo(state),
            connected_regions        = [],
        ),
        
        #Missions with carriable steps to complete require a few checks to be practical/completable
        'Carrying123': RegionData(
            locations    = MissionsCarrying123,
            entrancerule = lambda state:    rule_carrying(state),
            connected_regions        = [],
        ),
        'Carrying4': RegionData(
            locations    = MissionsCarrying4,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carrying5': RegionData(
            locations    = MissionsCarrying5,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'CarryingSecondary': RegionData(
            locations    = SecondariesCarrying,
            entrancerule = lambda state:    rule_carrying(state),
            connected_regions        = [],
        ),

        #Sabotage mission is a carrying type mission, and must be on Haz 5 for victory
        'VictoryAccess': RegionData(
            locations    =  MissionVictory, #Haz5 on magmacore, sabotage.
            entrancerule = lambda state:    rule_carrying(state) and rule_ammo(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
    }



# additional entry rules notes:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#L869

# can also place "Victory" at "Final Boss" and set collection as win condition
# self.multiworld.get_location("Final Boss", self.player).place_locked_item(self.create_event("Victory"))
# self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    
    #This is what changes number of locations. Will need to adjust this function later, and/or change how remove_locations works

    remove_locations(ALL_LOCATIONS, options.locations_to_remove.value)
    # ALL_LOCATIONS=remove_locations(ALL_LOCATIONS, 420)

    for region in REGIONS:
        #Added a check at the end of "if location in ALL_LOCATIONS"
        region_locations = {location: ALL_LOCATIONS[location] for location in REGIONS[region].locations if location in ALL_LOCATIONS}
        multiworld.regions += [create_region(multiworld, player, region, region_locations)]
        # x=create_region(multiworld, player, region, region_locations)
        # print(x)
        # print(x.get_locations()._list)
        # print (region)
        # print (region_locations)
    # import time
    # time.sleep(1000)
    for source in REGIONS:
        source_region = multiworld.get_region(source, player)        
        for target in REGIONS[source].connected_regions:
            target_region = multiworld.get_region(target, player)
            source_region.connect(
                connecting_region = target_region,
                name              = None, # autogen name to be 'REGION1 -> REGION2'
                rule              = REGIONS[target].entrancerule
            )

#Derp
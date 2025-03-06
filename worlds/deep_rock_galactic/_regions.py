from typing import NamedTuple, Callable

from BaseClasses import CollectionState

from ._subclasses import DRGLocation, DRGRegion
from ._locations import *
from ._items import Generic_Progressives, Carrying_Buffs

class RegionData(NamedTuple):
    locations: list[DRGLocation] = []
    entrancerule: Callable[[CollectionState], bool] = lambda x: True
    connected_regions: list[DRGRegion] = []

def create_region(multiworld, player, name, locations):
    region = DRGRegion(name, player, multiworld)
    region.add_locations(locations, DRGLocation)
    return region



def create_and_link_regions(multiworld, player):
    
    def rule_generic_progressive4(state):
        return state.has_from_list(Generic_Progressives,player,6) #This number will need balancing later.
    def rule_generic_progressive5(state):
        return state.has_from_list(Generic_Progressives,player,15) #This number will need heavy balancing later.
    def rule_carrying(state):
        return state.has_from_list(Carrying_Buffs,player,4) #This number will likely be in the range of 4-8.
    def rule_morkite(state):
        return state.has('Progressive-Morkite-Mining',player,3) #This number is safe at 3. As far as a tracker goes, MAY be completable at 2. sometimes.      
    
    
    REGIONS = {
        'Menu': RegionData(connected_regions=['AlwaysAccessLocations', 'AlwaysAccessSecondaries', 'GenericHaz4', 'GenericHaz5', \
        'Mining123', 'Mining4', 'Mining5', 'Carrying123', 'Carrying4', 'Carrying5','CarryingSecondary','VictoryAccess']), 
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
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
    }



# additional entry rules notes:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#L869

# can also place "Victory" at "Final Boss" and set collection as win condition
# self.multiworld.get_location("Final Boss", self.player).place_locked_item(self.create_event("Victory"))
# self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    
    #Taz didn't change any of this, and doesn't know what it does.
    for region in REGIONS:
        region_locations = {location: ALL_LOCATIONS[location] for location in REGIONS[region].locations}
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


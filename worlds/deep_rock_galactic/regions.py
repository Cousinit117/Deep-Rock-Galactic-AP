from typing import NamedTuple, Callable

from BaseClasses import CollectionState

from .subclasses import DRGLocation, DRGRegion
from .locations import location_init, remove_locations, Biomes, MissionTypes, SecondaryObjectives, Events, Warnings
from .items import Generic_Progressives, Carrying_Buffs

class RegionData(NamedTuple):
    locations: list[DRGLocation] = []
    entrancerule: Callable[[CollectionState], bool] = lambda x: True
    connected_regions: list[DRGRegion] = []

def create_region(multiworld, player, name, locations):
    region = DRGRegion(name, player, multiworld)
    region.add_locations(locations, DRGLocation)
    return region

def create_and_link_regions(multiworld, player, options, ALL_LOCATIONS, diffArr = [5,10,25,4,3,2]):
    
    def rule_generic_progressive3(state):
        return state.has_from_list(Generic_Progressives,player,diffArr[0]) #This number will need balancing later.
    def rule_generic_progressive4(state):
        return state.has_from_list(Generic_Progressives,player,diffArr[1]) #This number will need balancing later.
    def rule_generic_progressive5(state):
        return state.has_from_list(Generic_Progressives,player,diffArr[2]) #This number will need heavy balancing later.
    def rule_carrying(state):
        return state.has_from_list(Carrying_Buffs,player,diffArr[3]) #This number will likely be in the range of 4-8.
    def rule_morkite(state):
        return state.has('Progressive-Morkite-Mining',player,diffArr[4]) #This number is safe at 3. As far as a tracker goes, MAY be completable at 2. sometimes     
    def rule_ammo(state):
        return state.has('Progressive-Gun-Ammo',player,diffArr[5]) #Requires at least 2 ammo buffs

    MissionsDefault=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and ('1' in Mission or '2' in Mission)
        ]

    MissionsDefaultHaz3=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and ('3' in Mission)
        ]
        
    MissionsDefaultHaz4=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and ('4' in Mission)
        ]

    MissionsDefaultHaz5=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
        and ('5' in Mission)
        ]
    
    MissionsAmmo12=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('1' in Mission or '2' in Mission)
        ]

    MissionsAmmo3=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('3' in Mission)
        ]

    MissionsAmmo4=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('4' in Mission)
        ]

    MissionsAmmo5=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        and ('5' in Mission)
        ]
    
    MissionsCarrying12=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and ('1' in Mission or '2' in Mission)
        ]

    MissionsCarrying3=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and ('3' in Mission)
        ]

    MissionsCarrying4=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and ('4' in Mission)
        ]

    MissionsCarrying5=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
        and ('5' in Mission)
        ]

    MissionsMining12=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and ('1' in Mission or '2' in Mission)
        ]

    MissionsMining3=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and ('3' in Mission)
        ]

    MissionsMining4=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and ('4' in Mission)
        ]
    
    MissionsMining5=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission \
        and ('5' in Mission)
        ]

    ErrorCubes=[Mission for Mission in ALL_LOCATIONS if
        'Error Cube' in Mission
        ]

    Minigames=[Mission for Mission in ALL_LOCATIONS if
        'JettyBoot' in Mission
        ]

    CoinShop=[Mission for Mission in ALL_LOCATIONS if
        'Shop Item' in Mission
        ]

    Events12=[Mission for Mission in ALL_LOCATIONS if
        'Event' in Mission \
        and ('1' in Mission or '2' in Mission)
        ]

    Events3=[Mission for Mission in ALL_LOCATIONS if
        'Event' in Mission and '3' in Mission
        ]

    Events4=[Mission for Mission in ALL_LOCATIONS if
        'Event' in Mission and '4' in Mission
        ]
        
    Events5=[Mission for Mission in ALL_LOCATIONS if
        'Event' in Mission and '5' in Mission
        ]
        
    Warnings12=[Mission for Mission in ALL_LOCATIONS if
        'Warning' in Mission \
        and ('1' in Mission or '2' in Mission)
        ]

    Warnings3=[Mission for Mission in ALL_LOCATIONS if
        'Warning' in Mission and '3' in Mission
        ]
        
    Warnings4=[Mission for Mission in ALL_LOCATIONS if
        'Warning' in Mission and '4' in Mission
        ]
        
    Warnings5=[Mission for Mission in ALL_LOCATIONS if
        'Warning' in Mission and '5' in Mission
        ]

    #Only one not plural. You probably hate it, change if you want
    MissionVictory=[Mission for Mission in ALL_LOCATIONS if
        'Industrial Sabotage' in Mission \
        and '5' in Mission
        ]

    Secondaries12=[Secondary for Secondary in ALL_LOCATIONS if (
        ('Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or \
        'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Secondary Scan' in Secondary) \
        and ('1' in Secondary or '2' in Secondary))
        ]

    Secondaries3=[Secondary for Secondary in ALL_LOCATIONS if (
        ('Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or \
        'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Secondary Scan' in Secondary) \
        and ('3' in Secondary))
        ]

    Secondaries4=[Secondary for Secondary in ALL_LOCATIONS if (
        ('Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or \
        'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Secondary Scan' in Secondary) \
        and ('4' in Secondary))
        ]

    Secondaries5=[Secondary for Secondary in ALL_LOCATIONS if (
        ('Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or \
        'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Secondary Scan' in Secondary) \
        and ('5' in Secondary))
        ]

    SecondariesCarrying12=[Secondary for Secondary in ALL_LOCATIONS if (('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary) \
        and ('1' in Secondary or '2' in Secondary))
        ]

    SecondariesCarrying3=[Secondary for Secondary in ALL_LOCATIONS if (('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary) \
        and ('3' in Secondary))
        ]

    SecondariesCarrying4=[Secondary for Secondary in ALL_LOCATIONS if (('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary) \
        and ('4' in Secondary))
        ]

    SecondariesCarrying5=[Secondary for Secondary in ALL_LOCATIONS if (('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary) \
        and ('5' in Secondary))
        ]

    SecondariesAmmo12=[Secondary for Secondary in ALL_LOCATIONS if (('Dreadnought Eggs' in Secondary) and ('1' in Secondary or '2' in Secondary))]

    SecondariesAmmo3=[Secondary for Secondary in ALL_LOCATIONS if (('Dreadnought Eggs' in Secondary) and ('3' in Secondary))]

    SecondariesAmmo4=[Secondary for Secondary in ALL_LOCATIONS if (('Dreadnought Eggs' in Secondary) and ('4' in Secondary))]

    SecondariesAmmo5=[Secondary for Secondary in ALL_LOCATIONS if (('Dreadnought Eggs' in Secondary) and ('5' in Secondary))]
    
    REGIONS = {
        'Menu': RegionData(connected_regions=['AlwaysAccessLocations', 'GenericHaz4', 'GenericHaz5', \
        'Ammo12', 'Ammo3', 'Ammo4', 'Ammo5', \
        'Carrying12', 'Carrying3', 'Carrying4', 'Carrying5', \
        'Mining12', 'Mining3', 'Mining4', 'Mining5', \
        'ErrorCubes', 'Minigames', 'CoinShop', \
        'Events12', 'Events3', 'Events4', 'Events5', \
        'Warnings12', 'Warnings3', 'Warnings4', 'Warnings5', \
        'AlwaysAccessSecondaries', 'Secondaries3', 'Secondaries4', 'Secondaries5', \
        'CarryingSecondary12', 'CarryingSecondary3', 'CarryingSecondary4', 'CarryingSecondary5', \
        'AmmoSecondary12', 'AmmoSecondary3', 'AmmoSecondary4', 'AmmoSecondary5', \
        'VictoryAccess']), 
        # Should contain all
        
        'AlwaysAccessLocations': RegionData(
            locations    = MissionsDefault,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'GenericHaz4': RegionData(
            locations    = MissionsDefaultHaz3,
            entrancerule = lambda state:    rule_generic_progressive3(state),
            connected_regions        = [],
        ), # Haz 3 will require N progressives for access rule
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

        #Elimination missions require Progressive ammo checks to be completable
        'Ammo12': RegionData(
            locations    = MissionsAmmo12,
            entrancerule = lambda state:    rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo3': RegionData(
            locations    = MissionsAmmo3,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive3(state),
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
        
        #Missions with carriable steps to complete require a few checks to be practical/completable
        'Carrying12': RegionData(
            locations    = MissionsCarrying12,
            entrancerule = lambda state:    rule_carrying(state),
            connected_regions        = [],
        ),
        'Carrying3': RegionData(
            locations    = MissionsCarrying3,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive3(state),
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
        
        #Mining missions require Progressive morkite checks to be completable
        'Mining12': RegionData(
            locations    = MissionsMining12,
            entrancerule = lambda state:    rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining3': RegionData(
            locations    = MissionsMining3,
            entrancerule = lambda state:    rule_morkite(state) \
            and rule_generic_progressive3(state),
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

        #Cubes
        'ErrorCubes': RegionData(
            locations    = ErrorCubes,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),

        #Minigames
        'Minigames': RegionData(
            locations    = Minigames,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),

        #Coin Shop
        'CoinShop': RegionData(
            locations    = CoinShop,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),

        #Events
        'Events12': RegionData(
            locations    = Events12,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Events3': RegionData(
            locations    = Events4,
            entrancerule = lambda state:    rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Events4': RegionData(
            locations    = Events4,
            entrancerule = lambda state:    rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Events5': RegionData(
            locations    = Events5,
            entrancerule = lambda state:    rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Warnings
        'Warnings12': RegionData(
            locations    = Warnings12,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Warnings3': RegionData(
            locations    = Warnings3,
            entrancerule = lambda state:    rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Warnings4': RegionData(
            locations    = Warnings4,
            entrancerule = lambda state:    rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Warnings5': RegionData(
            locations    = Warnings5,
            entrancerule = lambda state:    rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #secondaries generic
        'AlwaysAccessSecondaries': RegionData(
            locations    = Secondaries12,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Secondaries3': RegionData(
            locations    = Secondaries3,
            entrancerule = lambda state: rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Secondaries4': RegionData(
            locations    = Secondaries4,
            entrancerule = lambda state: rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Secondaries5': RegionData(
            locations    = Secondaries5,
            entrancerule = lambda state: rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Carry Secondaries
        'CarryingSecondary12': RegionData(
            locations    = SecondariesCarrying12,
            entrancerule = lambda state:    rule_carrying(state),
            connected_regions        = [],
        ),
        'CarryingSecondary3': RegionData(
            locations    = SecondariesCarrying3,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'CarryingSecondary4': RegionData(
            locations    = SecondariesCarrying4,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'CarryingSecondary5': RegionData(
            locations    = SecondariesCarrying5,
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Ammo Secondaries
        'AmmoSecondary12': RegionData(
            locations    = SecondariesAmmo12,
            entrancerule = lambda state:    rule_ammo(state),
            connected_regions        = [],
        ),
        'AmmoSecondary3': RegionData(
            locations    = SecondariesAmmo3,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'AmmoSecondary4': RegionData(
            locations    = SecondariesAmmo4,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'AmmoSecondary5': RegionData(
            locations    = SecondariesAmmo5,
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive5(state),
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

    # remove_locations(ALL_LOCATIONS, options.locations_to_remove.value)
    # remove_locations(ALL_LOCATIONS,100)
    baseRemoval = 3
    trapRemoval = 0
    if not bool(options.traps_on.value):
        trapRemoval = 48
    totalToRemove = baseRemoval + trapRemoval + options.locations_to_remove.value #81
    ALL_LOCATIONS=remove_locations(ALL_LOCATIONS,totalToRemove,int(options.error_cube_checks.value),bool(options.minigames_on.value),int(options.goal_mode.value))
    # print(REGIONS)
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
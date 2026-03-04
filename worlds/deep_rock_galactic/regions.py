from typing import NamedTuple, Callable

from BaseClasses import CollectionState

from .subclasses import DRGLocation, DRGRegion
from .locations import location_init, remove_locations, Biomes, MissionTypes, SecondaryObjectives, Events, Warnings
from .items import Generic_Progressives, Carrying_Buffs, WEAPONS_PRIMARY, WEAPONS_SECONDARY

class RegionData(NamedTuple):
    locations: list[DRGLocation] = []
    entrancerule: Callable[[CollectionState], bool] = lambda x: True
    connected_regions: list[DRGRegion] = []

def create_region(multiworld, player, name, locations):
    region = DRGRegion(name, player, multiworld)
    region.add_locations(locations, DRGLocation)
    return region

def generateLocationBiomes(locationlist,biome):
    newList = [item for item in locationlist if (biome in item)]
    return newList

def generateLocationHaz(locationlist,haz):
    newList = [item for item in locationlist if (any(sub in item for sub in haz))]
    return newList

def create_and_link_regions(multiworld, player, options, ALL_LOCATIONS, diffArr = [5,10,25,4,3,2]):
    
    biomeCheckList = ['all','Biome-Azure-Weald','Biome-Crystalline-Caverns','Biome-Fungus-Bogs','Biome-Hollow-Bough','Biome-Glacial-Strata',\
    'Biome-Dense-Biozone','Biome-Magma-Core','Biome-Radioactive-Exclusion-Zone','Biome-Salt-Pits','Biome-Sandblasted-Corridors','Biome-Ossuary-Depths']

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
    def rule_biome(state,biomeVal):
        if options.goal_mode.value == 1 and options.biome_start.value != 0 and options.biome_start.value != biomeVal: #only goal biomes matter for
            return state.has(biomeCheckList[biomeVal],player,1) #Requires at least 1 of the biome required
        else:
            return True
    def rule_weapons(state):
        if options.wep_rando.value == 1:
            TotalWeps = state.count_from_list(WEAPONS_PRIMARY,player) + state.count_from_list(WEAPONS_SECONDARY,player)
            if TotalWeps >= (diffArr[5]+2):
                return True
            else:
                return False
        else:
            return False

    GoldRush=[Mission for Mission in ALL_LOCATIONS if
        'Gold Rush' in Mission
        ]

    Hunting=[Mission for Mission in ALL_LOCATIONS if
        ('Hunting Trophy' in Mission or 'Hunting Boss Trophy' in Mission or 'Trophy Hunter' in Mission)
        ]

    MissionsDefault=[Mission for Mission in ALL_LOCATIONS if (
        'Egg Hunt' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission or 'Heavy Excavation' in Mission)
        ]
    
    MissionsAmmo=[Mission for Mission in ALL_LOCATIONS if (
        'Elimination' in Mission)
        ]
    
    MissionsCarrying=[Mission for Mission in ALL_LOCATIONS if (
        'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission)
        ]

    MissionsMining=[Mission for Mission in ALL_LOCATIONS if
        'Mining Expedition' in Mission
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

    Events=[Mission for Mission in ALL_LOCATIONS if
        'Event' in Mission
        ]
        
    Warnings=[Mission for Mission in ALL_LOCATIONS if
        'Warning' in Mission
        ]

    #Only one not plural. You probably hate it, change if you want
    MissionVictory=[Mission for Mission in ALL_LOCATIONS if
        'Industrial Sabotage' in Mission \
        and '5' in Mission
        ]

    Secondaries=[Secondary for Secondary in ALL_LOCATIONS if (
        ('Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
        or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or \
        'Hollomite' in Secondary or 'Black Box' in Secondary or 'Oil Pumping' in Secondary or 'Secondary Scan' in Secondary or 'Secondary Excavation' in Secondary))
        ]

    SecondariesCarrying=[Secondary for Secondary in ALL_LOCATIONS if (('Gunk Seeds' in Secondary or 'Mini Mules' in Secondary or 'Alien Eggs' in Secondary))
        ]

    SecondariesAmmo=[Secondary for Secondary in ALL_LOCATIONS if ('Dreadnought Eggs' in Secondary)]
    
    REGIONS = {
        'Menu': RegionData(connected_regions=['Generic12AW','Generic12CC','Generic12FB','Generic12HB','Generic12GS','Generic12DB','Generic12MC','Generic12REZ','Generic12SP','Generic12SC','Generic12OD', \
        'Generic3AW','Generic3CC','Generic3FB','Generic3HB','Generic3GS','Generic3DB','Generic3MC','Generic3REZ','Generic3SP','Generic3SC','Generic3OD', \
        'Generic4AW','Generic4CC','Generic4FB','Generic4HB','Generic4GS','Generic4DB','Generic4MC','Generic4REZ','Generic4SP','Generic4SC','Generic4OD', \
        'Generic5AW','Generic5CC','Generic5FB','Generic5HB','Generic5GS','Generic5DB','Generic5MC','Generic5REZ','Generic5SP','Generic5SC','Generic5OD', \
        'Ammo12AW','Ammo12CC','Ammo12FB','Ammo12HB','Ammo12GS','Ammo12DB','Ammo12MC','Ammo12REZ','Ammo12SP','Ammo12SC','Ammo12OD', \
        'Ammo3AW','Ammo3CC','Ammo3FB','Ammo3HB','Ammo3GS','Ammo3DB','Ammo3MC','Ammo3REZ','Ammo3SP','Ammo3SC','Ammo3OD', \
        'Ammo4AW','Ammo4CC','Ammo4FB','Ammo4HB','Ammo4GS','Ammo4DB','Ammo4MC','Ammo4REZ','Ammo4SP','Ammo4SC','Ammo4OD', \
        'Ammo5AW','Ammo5CC','Ammo5FB','Ammo5HB','Ammo5GS','Ammo5DB','Ammo5MC','Ammo5REZ','Ammo5SP','Ammo5SC','Ammo5OD', \
        'Carry12AW','Carry12CC','Carry12FB','Carry12HB','Carry12GS','Carry12DB','Carry12MC','Carry12REZ','Carry12SP','Carry12SC','Carry12OD', \
        'Carry3AW','Carry3CC','Carry3FB','Carry3HB','Carry3GS','Carry3DB','Carry3MC','Carry3REZ','Carry3SP','Carry3SC','Carry3OD', \
        'Carry4AW','Carry4CC','Carry4FB','Carry4HB','Carry4GS','Carry4DB','Carry4MC','Carry4REZ','Carry4SP','Carry4SC','Carry4OD', \
        'Carry5AW','Carry5CC','Carry5FB','Carry5HB','Carry5GS','Carry5DB','Carry5MC','Carry5REZ','Carry5SP','Carry5SC','Carry5OD', \
        'Mining12AW','Mining12CC','Mining12FB','Mining12HB','Mining12GS','Mining12DB','Mining12MC','Mining12REZ','Mining12SP','Mining12SC','Mining12OD', \
        'Mining3AW','Mining3CC','Mining3FB','Mining3HB','Mining3GS','Mining3DB','Mining3MC','Mining3REZ','Mining3SP','Mining3SC','Mining3OD', \
        'Mining4AW','Mining4CC','Mining4FB','Mining4HB','Mining4GS','Mining4DB','Mining4MC','Mining4REZ','Mining4SP','Mining4SC','Mining4OD', \
        'Mining5AW','Mining5CC','Mining5FB','Mining5HB','Mining5GS','Mining5DB','Mining5MC','Mining5REZ','Mining5SP','Mining5SC','Mining5OD', \
        'Hunting', 'GoldRush', \
        'ErrorCubes', 'Minigames', 'CoinShop', \
        'Events12', 'Events3', 'Events4', 'Events5', \
        'Warnings12', 'Warnings3', 'Warnings4', 'Warnings5', \
        'AlwaysAccessSecondaries', 'Secondaries3', 'Secondaries4', 'Secondaries5', \
        'CarryingSecondary12', 'CarryingSecondary3', 'CarryingSecondary4', 'CarryingSecondary5', \
        'AmmoSecondary12', 'AmmoSecondary3', 'AmmoSecondary4', 'AmmoSecondary5', \
        'VictoryAccess']), 
        # Should contain all
        
        #Generic Set 12
        'Generic12AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Azure Weald'),['1','2']),
            entrancerule = lambda state: rule_biome(state,1),
            connected_regions        = [],
        ),
        'Generic12CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Crystalline Caverns'),['1','2']),
            entrancerule = lambda state: rule_biome(state,2),
            connected_regions        = [],
        ),
        'Generic12FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Fungus Bogs'),['1','2']),
            entrancerule = lambda state: rule_biome(state,3),
            connected_regions        = [],
        ),
        'Generic12HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Hollow Bough'),['1','2']),
            entrancerule = lambda state: rule_biome(state,4),
            connected_regions        = [],
        ),
        'Generic12GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Glacial Strata'),['1','2']),
            entrancerule = lambda state: rule_biome(state,5),
            connected_regions        = [],
        ),
        'Generic12DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Dense Biozone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,6),
            connected_regions        = [],
        ),
        'Generic12MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Magma Core'),['1','2']),
            entrancerule = lambda state: rule_biome(state,7),
            connected_regions        = [],
        ),
        'Generic12REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Radioactive Exclusion Zone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,8),
            connected_regions        = [],
        ),
        'Generic12SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Salt Pits'),['1','2']),
            entrancerule = lambda state: rule_biome(state,9),
            connected_regions        = [],
        ),
        'Generic12SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Sandblasted Corridors'),['1','2']),
            entrancerule = lambda state: rule_biome(state,10),
            connected_regions        = [],
        ),
        'Generic12OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Ossuary Depths'),['1','2']),
            entrancerule = lambda state: rule_biome(state,11),
            connected_regions        = [],
        ),
        #End Generic Haz 1-2

        #Start Generic Haz 3
        'Generic3AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Azure Weald'),['3']),
            entrancerule = lambda state: rule_biome(state,1) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Crystalline Caverns'),['3']),
            entrancerule = lambda state: rule_biome(state,2) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Fungus Bogs'),['3']),
            entrancerule = lambda state: rule_biome(state,3) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Hollow Bough'),['3']),
            entrancerule = lambda state: rule_biome(state,4) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Glacial Strata'),['3']),
            entrancerule = lambda state: rule_biome(state,5) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Dense Biozone'),['3']),
            entrancerule = lambda state: rule_biome(state,6) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Magma Core'),['3']),
            entrancerule = lambda state: rule_biome(state,7) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Radioactive Exclusion Zone'),['3']),
            entrancerule = lambda state: rule_biome(state,8) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Salt Pits'),['3']),
            entrancerule = lambda state: rule_biome(state,9) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Sandblasted Corridors'),['3']),
            entrancerule = lambda state: rule_biome(state,10) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Generic3OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Ossuary Depths'),['3']),
            entrancerule = lambda state: rule_biome(state,11) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        #End Generic Haz 3

        #Start Generic Haz 4
        'Generic4AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Azure Weald'),['4']),
            entrancerule = lambda state: rule_biome(state,1) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Crystalline Caverns'),['4']),
            entrancerule = lambda state: rule_biome(state,2) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Fungus Bogs'),['4']),
            entrancerule = lambda state: rule_biome(state,3) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Hollow Bough'),['4']),
            entrancerule = lambda state: rule_biome(state,4) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Glacial Strata'),['4']),
            entrancerule = lambda state: rule_biome(state,5) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Dense Biozone'),['4']),
            entrancerule = lambda state: rule_biome(state,6) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Magma Core'),['4']),
            entrancerule = lambda state: rule_biome(state,7) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Radioactive Exclusion Zone'),['4']),
            entrancerule = lambda state: rule_biome(state,8) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Salt Pits'),['4']),
            entrancerule = lambda state: rule_biome(state,9) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Sandblasted Corridors'),['4']),
            entrancerule = lambda state: rule_biome(state,10) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Generic4OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Ossuary Depths'),['4']),
            entrancerule = lambda state: rule_biome(state,11) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        #End Generic Haz 4

        #Start Generic Haz 5
        'Generic5AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Azure Weald'),['5']),
            entrancerule = lambda state: rule_biome(state,1) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Crystalline Caverns'),['5']),
            entrancerule = lambda state: rule_biome(state,2) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Fungus Bogs'),['5']),
            entrancerule = lambda state: rule_biome(state,3) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Hollow Bough'),['5']),
            entrancerule = lambda state: rule_biome(state,4) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Glacial Strata'),['5']),
            entrancerule = lambda state: rule_biome(state,5) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Dense Biozone'),['5']),
            entrancerule = lambda state: rule_biome(state,6) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Magma Core'),['5']),
            entrancerule = lambda state: rule_biome(state,7) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Radioactive Exclusion Zone'),['5']),
            entrancerule = lambda state: rule_biome(state,8) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Salt Pits'),['5']),
            entrancerule = lambda state: rule_biome(state,9) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Sandblasted Corridors'),['5']),
            entrancerule = lambda state: rule_biome(state,10) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Generic5OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsDefault,'Ossuary Depths'),['5']),
            entrancerule = lambda state: rule_biome(state,11) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        #End Generic Haz 5

        #Elimination missions require Progressive ammo checks to be completable
        #Start Ammo 12
        'Ammo12AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Azure Weald'),['1','2']),
            entrancerule = lambda state: rule_biome(state,1) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Crystalline Caverns'),['1','2']),
            entrancerule = lambda state: rule_biome(state,2) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Fungus Bogs'),['1','2']),
            entrancerule = lambda state: rule_biome(state,3) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Hollow Bough'),['1','2']),
            entrancerule = lambda state: rule_biome(state,4) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Glacial Strata'),['1','2']),
            entrancerule = lambda state: rule_biome(state,5) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Dense Biozone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,6) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Magma Core'),['1','2']),
            entrancerule = lambda state: rule_biome(state,7) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Radioactive Exclusion Zone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,8) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Salt Pits'),['1','2']),
            entrancerule = lambda state: rule_biome(state,9) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Sandblasted Corridors'),['1','2']),
            entrancerule = lambda state: rule_biome(state,10) and rule_ammo(state),
            connected_regions        = [],
        ),
        'Ammo12OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Ossuary Depths'),['1','2']),
            entrancerule = lambda state: rule_biome(state,11) and rule_ammo(state),
            connected_regions        = [],
        ),
        #End Ammo Haz 1-2

        #Start Ammo 3
        'Ammo3AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Azure Weald'),['3']),
            entrancerule = lambda state: rule_biome(state,1) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Crystalline Caverns'),['3']),
            entrancerule = lambda state: rule_biome(state,2) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Fungus Bogs'),['3']),
            entrancerule = lambda state: rule_biome(state,3) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Hollow Bough'),['3']),
            entrancerule = lambda state: rule_biome(state,4) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Glacial Strata'),['3']),
            entrancerule = lambda state: rule_biome(state,5) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Dense Biozone'),['3']),
            entrancerule = lambda state: rule_biome(state,6) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Magma Core'),['3']),
            entrancerule = lambda state: rule_biome(state,7) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Radioactive Exclusion Zone'),['3']),
            entrancerule = lambda state: rule_biome(state,8) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Salt Pits'),['3']),
            entrancerule = lambda state: rule_biome(state,9) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Sandblasted Corridors'),['3']),
            entrancerule = lambda state: rule_biome(state,10) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Ammo3OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Ossuary Depths'),['3']),
            entrancerule = lambda state: rule_biome(state,11) and rule_ammo(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        #End Ammo Haz 3

        #Start Ammo 4
        'Ammo4AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Azure Weald'),['4']),
            entrancerule = lambda state: rule_biome(state,1) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Crystalline Caverns'),['4']),
            entrancerule = lambda state: rule_biome(state,2) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Fungus Bogs'),['4']),
            entrancerule = lambda state: rule_biome(state,3) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Hollow Bough'),['4']),
            entrancerule = lambda state: rule_biome(state,4) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Glacial Strata'),['4']),
            entrancerule = lambda state: rule_biome(state,5) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Dense Biozone'),['4']),
            entrancerule = lambda state: rule_biome(state,6) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Magma Core'),['4']),
            entrancerule = lambda state: rule_biome(state,7) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Radioactive Exclusion Zone'),['4']),
            entrancerule = lambda state: rule_biome(state,8) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Salt Pits'),['4']),
            entrancerule = lambda state: rule_biome(state,9) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Sandblasted Corridors'),['4']),
            entrancerule = lambda state: rule_biome(state,10) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Ammo4OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Ossuary Depths'),['4']),
            entrancerule = lambda state: rule_biome(state,11) and rule_ammo(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        #End Ammo Haz 4

        #Start Ammo 5
        'Ammo5AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Azure Weald'),['5']),
            entrancerule = lambda state: rule_biome(state,1) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Crystalline Caverns'),['5']),
            entrancerule = lambda state: rule_biome(state,2) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Fungus Bogs'),['5']),
            entrancerule = lambda state: rule_biome(state,3) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Hollow Bough'),['5']),
            entrancerule = lambda state: rule_biome(state,4) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Glacial Strata'),['5']),
            entrancerule = lambda state: rule_biome(state,5) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Dense Biozone'),['5']),
            entrancerule = lambda state: rule_biome(state,6) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Magma Core'),['5']),
            entrancerule = lambda state: rule_biome(state,7) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Radioactive Exclusion Zone'),['5']),
            entrancerule = lambda state: rule_biome(state,8) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Salt Pits'),['5']),
            entrancerule = lambda state: rule_biome(state,9) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Sandblasted Corridors'),['5']),
            entrancerule = lambda state: rule_biome(state,10) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Ammo5OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsAmmo,'Ossuary Depths'),['5']),
            entrancerule = lambda state: rule_biome(state,11) and rule_ammo(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        #End Ammo Haz 5
        
        #Missions with carriable steps to complete require a few checks to be practical/completable
        #Start Carry 12
        'Carry12AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Azure Weald'),['1','2']),
            entrancerule = lambda state: rule_biome(state,1) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Crystalline Caverns'),['1','2']),
            entrancerule = lambda state: rule_biome(state,2) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Fungus Bogs'),['1','2']),
            entrancerule = lambda state: rule_biome(state,3) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Hollow Bough'),['1','2']),
            entrancerule = lambda state: rule_biome(state,4) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Glacial Strata'),['1','2']),
            entrancerule = lambda state: rule_biome(state,5) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Dense Biozone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,6) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Magma Core'),['1','2']),
            entrancerule = lambda state: rule_biome(state,7) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Radioactive Exclusion Zone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,8) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Salt Pits'),['1','2']),
            entrancerule = lambda state: rule_biome(state,9) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Sandblasted Corridors'),['1','2']),
            entrancerule = lambda state: rule_biome(state,10) and rule_carrying(state),
            connected_regions        = [],
        ),
        'Carry12OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Ossuary Depths'),['1','2']),
            entrancerule = lambda state: rule_biome(state,11) and rule_carrying(state),
            connected_regions        = [],
        ),
        #End Carry Haz 1-2

        #Start Carry 3
        'Carry3AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Azure Weald'),['3']),
            entrancerule = lambda state: rule_biome(state,1) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Crystalline Caverns'),['3']),
            entrancerule = lambda state: rule_biome(state,2) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Fungus Bogs'),['3']),
            entrancerule = lambda state: rule_biome(state,3) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Hollow Bough'),['3']),
            entrancerule = lambda state: rule_biome(state,4) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Glacial Strata'),['3']),
            entrancerule = lambda state: rule_biome(state,5) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Dense Biozone'),['3']),
            entrancerule = lambda state: rule_biome(state,6) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Magma Core'),['3']),
            entrancerule = lambda state: rule_biome(state,7) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Radioactive Exclusion Zone'),['3']),
            entrancerule = lambda state: rule_biome(state,8) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Salt Pits'),['3']),
            entrancerule = lambda state: rule_biome(state,9) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Sandblasted Corridors'),['3']),
            entrancerule = lambda state: rule_biome(state,10) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Carry3OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Ossuary Depths'),['3']),
            entrancerule = lambda state: rule_biome(state,11) and rule_carrying(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        #End Carry Haz 3

        #Start Carry 4
        'Carry4AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Azure Weald'),['4']),
            entrancerule = lambda state: rule_biome(state,1) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Crystalline Caverns'),['4']),
            entrancerule = lambda state: rule_biome(state,2) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Fungus Bogs'),['4']),
            entrancerule = lambda state: rule_biome(state,3) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Hollow Bough'),['4']),
            entrancerule = lambda state: rule_biome(state,4) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Glacial Strata'),['4']),
            entrancerule = lambda state: rule_biome(state,5) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Dense Biozone'),['4']),
            entrancerule = lambda state: rule_biome(state,6) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Magma Core'),['4']),
            entrancerule = lambda state: rule_biome(state,7) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Radioactive Exclusion Zone'),['4']),
            entrancerule = lambda state: rule_biome(state,8) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Salt Pits'),['4']),
            entrancerule = lambda state: rule_biome(state,9) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Sandblasted Corridors'),['4']),
            entrancerule = lambda state: rule_biome(state,10) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Carry4OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Ossuary Depths'),['4']),
            entrancerule = lambda state: rule_biome(state,11) and rule_carrying(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        #End Carry Haz 4

        #Start Carry 5
        'Carry5AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Azure Weald'),['5']),
            entrancerule = lambda state: rule_biome(state,1) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Crystalline Caverns'),['5']),
            entrancerule = lambda state: rule_biome(state,2) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Fungus Bogs'),['5']),
            entrancerule = lambda state: rule_biome(state,3) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Hollow Bough'),['5']),
            entrancerule = lambda state: rule_biome(state,4) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Glacial Strata'),['5']),
            entrancerule = lambda state: rule_biome(state,5) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Dense Biozone'),['5']),
            entrancerule = lambda state: rule_biome(state,6) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Magma Core'),['5']),
            entrancerule = lambda state: rule_biome(state,7) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Radioactive Exclusion Zone'),['5']),
            entrancerule = lambda state: rule_biome(state,8) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Salt Pits'),['5']),
            entrancerule = lambda state: rule_biome(state,9) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Sandblasted Corridors'),['5']),
            entrancerule = lambda state: rule_biome(state,10) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Carry5OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsCarrying,'Ossuary Depths'),['5']),
            entrancerule = lambda state: rule_biome(state,11) and rule_carrying(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        #End Carry Haz 5
        
        #Mining missions require Progressive morkite checks to be completable
        #Mining Set 12
        'Mining12AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Azure Weald'),['1','2']),
            entrancerule = lambda state: rule_biome(state,1) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Crystalline Caverns'),['1','2']),
            entrancerule = lambda state: rule_biome(state,2) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Fungus Bogs'),['1','2']),
            entrancerule = lambda state: rule_biome(state,3) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Hollow Bough'),['1','2']),
            entrancerule = lambda state: rule_biome(state,4) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Glacial Strata'),['1','2']),
            entrancerule = lambda state: rule_biome(state,5) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Dense Biozone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,6) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Magma Core'),['1','2']),
            entrancerule = lambda state: rule_biome(state,7) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Radioactive Exclusion Zone'),['1','2']),
            entrancerule = lambda state: rule_biome(state,8) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Salt Pits'),['1','2']),
            entrancerule = lambda state: rule_biome(state,9) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Sandblasted Corridors'),['1','2']),
            entrancerule = lambda state: rule_biome(state,10) and rule_morkite(state),
            connected_regions        = [],
        ),
        'Mining12OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Ossuary Depths'),['1','2']),
            entrancerule = lambda state: rule_biome(state,11) and rule_morkite(state),
            connected_regions        = [],
        ),
        #End Mining Haz 1-2

        #Mining Set 3
        'Mining3AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Azure Weald'),['3']),
            entrancerule = lambda state: rule_biome(state,1) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Crystalline Caverns'),['3']),
            entrancerule = lambda state: rule_biome(state,2) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Fungus Bogs'),['3']),
            entrancerule = lambda state: rule_biome(state,3) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Hollow Bough'),['3']),
            entrancerule = lambda state: rule_biome(state,4) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Glacial Strata'),['3']),
            entrancerule = lambda state: rule_biome(state,5) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Dense Biozone'),['3']),
            entrancerule = lambda state: rule_biome(state,6) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Magma Core'),['3']),
            entrancerule = lambda state: rule_biome(state,7) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Radioactive Exclusion Zone'),['3']),
            entrancerule = lambda state: rule_biome(state,8) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Salt Pits'),['3']),
            entrancerule = lambda state: rule_biome(state,9) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Sandblasted Corridors'),['3']),
            entrancerule = lambda state: rule_biome(state,10) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Mining3OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Ossuary Depths'),['3']),
            entrancerule = lambda state: rule_biome(state,11) and rule_morkite(state) and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        #End Mining Haz 3

        #Mining Set 4
        'Mining4AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Azure Weald'),['4']),
            entrancerule = lambda state: rule_biome(state,1) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Crystalline Caverns'),['4']),
            entrancerule = lambda state: rule_biome(state,2) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Fungus Bogs'),['4']),
            entrancerule = lambda state: rule_biome(state,3) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Hollow Bough'),['4']),
            entrancerule = lambda state: rule_biome(state,4) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Glacial Strata'),['4']),
            entrancerule = lambda state: rule_biome(state,5) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Dense Biozone'),['4']),
            entrancerule = lambda state: rule_biome(state,6) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Magma Core'),['4']),
            entrancerule = lambda state: rule_biome(state,7) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Radioactive Exclusion Zone'),['4']),
            entrancerule = lambda state: rule_biome(state,8) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Salt Pits'),['4']),
            entrancerule = lambda state: rule_biome(state,9) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Sandblasted Corridors'),['4']),
            entrancerule = lambda state: rule_biome(state,10) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Mining4OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Ossuary Depths'),['4']),
            entrancerule = lambda state: rule_biome(state,11) and rule_morkite(state) and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        #End Mining Haz 4

        #Mining Set 5
        'Mining5AW': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Azure Weald'),['5']),
            entrancerule = lambda state: rule_biome(state,1) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5CC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Crystalline Caverns'),['5']),
            entrancerule = lambda state: rule_biome(state,2) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5FB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Fungus Bogs'),['5']),
            entrancerule = lambda state: rule_biome(state,3) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5HB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Hollow Bough'),['5']),
            entrancerule = lambda state: rule_biome(state,4) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5GS': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Glacial Strata'),['5']),
            entrancerule = lambda state: rule_biome(state,5) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5DB': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Dense Biozone'),['5']),
            entrancerule = lambda state: rule_biome(state,6) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5MC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Magma Core'),['5']),
            entrancerule = lambda state: rule_biome(state,7) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5REZ': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Radioactive Exclusion Zone'),['5']),
            entrancerule = lambda state: rule_biome(state,8) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5SP': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Salt Pits'),['5']),
            entrancerule = lambda state: rule_biome(state,9) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5SC': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Sandblasted Corridors'),['5']),
            entrancerule = lambda state: rule_biome(state,10) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        'Mining5OD': RegionData(
            locations    = generateLocationHaz(generateLocationBiomes(MissionsMining,'Ossuary Depths'),['5']),
            entrancerule = lambda state: rule_biome(state,11) and rule_morkite(state) and rule_generic_progressive5(state),
            connected_regions        = [],
        ),
        #End Mining Haz 4

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
            locations    = generateLocationHaz(Events,['1','2']),
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Events3': RegionData(
            locations    = generateLocationHaz(Events,['3']),
            entrancerule = lambda state:    rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Events4': RegionData(
            locations    = generateLocationHaz(Events,['4']),
            entrancerule = lambda state:    rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Events5': RegionData(
            locations    = generateLocationHaz(Events,['5']),
            entrancerule = lambda state:    rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Warnings
        'Warnings12': RegionData(
            locations    = generateLocationHaz(Warnings,['1','2']),
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Warnings3': RegionData(
            locations    = generateLocationHaz(Warnings,['3']),
            entrancerule = lambda state:    rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Warnings4': RegionData(
            locations    = generateLocationHaz(Warnings,['4']),
            entrancerule = lambda state:    rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Warnings5': RegionData(
            locations    = generateLocationHaz(Warnings,['5']),
            entrancerule = lambda state:    rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #secondaries generic
        'AlwaysAccessSecondaries': RegionData(
            locations    = generateLocationHaz(Secondaries,['1','2']),
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),
        'Secondaries3': RegionData(
            locations    = generateLocationHaz(Secondaries,['3']),
            entrancerule = lambda state: rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'Secondaries4': RegionData(
            locations    = generateLocationHaz(Secondaries,['4']),
            entrancerule = lambda state: rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'Secondaries5': RegionData(
            locations    = generateLocationHaz(Secondaries,['5']),
            entrancerule = lambda state: rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Carry Secondaries
        'CarryingSecondary12': RegionData(
            locations    = generateLocationHaz(SecondariesCarrying,['1','2']),
            entrancerule = lambda state:    rule_carrying(state),
            connected_regions        = [],
        ),
        'CarryingSecondary3': RegionData(
            locations    = generateLocationHaz(SecondariesCarrying,['3']),
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'CarryingSecondary4': RegionData(
            locations    = generateLocationHaz(SecondariesCarrying,['4']),
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'CarryingSecondary5': RegionData(
            locations    = generateLocationHaz(SecondariesCarrying,['5']),
            entrancerule = lambda state:    rule_carrying(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        #Ammo Secondaries
        'AmmoSecondary12': RegionData(
            locations    = generateLocationHaz(SecondariesAmmo,['1','2']),
            entrancerule = lambda state:    rule_ammo(state),
            connected_regions        = [],
        ),
        'AmmoSecondary3': RegionData(
            locations    = generateLocationHaz(SecondariesAmmo,['3']),
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive3(state),
            connected_regions        = [],
        ),
        'AmmoSecondary4': RegionData(
            locations    = generateLocationHaz(SecondariesAmmo,['4']),
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive4(state),
            connected_regions        = [],
        ),
        'AmmoSecondary5': RegionData(
            locations    = generateLocationHaz(SecondariesAmmo,['5']),
            entrancerule = lambda state:    rule_ammo(state) \
            and rule_generic_progressive5(state),
            connected_regions        = [],
        ),

        'GoldRush': RegionData(
            locations    = GoldRush,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),

        'Hunting': RegionData(
            locations    = Hunting,
            entrancerule = lambda state: True,#No Access restrictions
            connected_regions        = [],
        ),

        #Sabotage mission is a carrying type mission, and must be on Haz 5 for victory
        'VictoryAccess': RegionData(
            locations    =  MissionVictory, #Haz5 on magmacore, sabotage.
            entrancerule = lambda state:    rule_carrying(state) and rule_ammo(state) \
            and rule_generic_progressive5(state) and rule_biome(state,options.biome_end.value),
            connected_regions        = [],
        ),
        
    }



    # additional entry rules notes:
    # https://github.com/ArchipelagoMW/Archipelago/blob/main/BaseClasses.py#L869

    # can also place "Victory" at "Final Boss" and set collection as win condition
    # self.multiworld.get_location("Final Boss", self.player).place_locked_item(self.create_event("Victory"))
    # self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
    
    #This is what changes number of locations. Will need to adjust this function later, and/or change how remove_locations works

    biomeNamesList = ['Magma Core','Azure Weald','Crystalline Caverns','Fungus Bogs','Hollow Bough','Glacial Strata',\
        'Dense Biozone','Magma Core','Radioactive Exclusion Zone','Salt Pits','Sandblasted Corridors','Ossuary Depths']

    # remove_locations(ALL_LOCATIONS, options.locations_to_remove.value)
    # remove_locations(ALL_LOCATIONS,100)
    baseRemoval = 0
    trapRemoval = 0
    classRemoval = 0
    sprintRemoval = 0
    if not bool(options.traps_on.value):
        trapRemoval = 48
    if options.avail_classes.value == 0:
        classRemoval = 4
    if options.sprint_start.value == 1:
        sprintRemoval = 4
    totalToRemove = baseRemoval + trapRemoval + classRemoval + sprintRemoval # + options.locations_to_remove.value #81
    ALL_LOCATIONS=remove_locations(ALL_LOCATIONS,totalToRemove,int(options.error_cube_checks.value),\
        bool(options.minigames_on.value),int(options.minigame_num.value),int(options.goal_mode.value),int(options.gold_rush_val.value),\
        int(options.shop_item_num.value),bool(options.events_on.value),int(options.max_hazard.value),\
        int(options.hunter_trophies.value),int(options.hunter_targets.value),int(options.hunter_trophies_b.value),biomeNamesList[options.biome_end.value])
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
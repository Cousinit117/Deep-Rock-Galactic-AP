from BaseClasses import MultiWorld
from typing import NamedTuple
from ._subclasses import DRGItem
import random
#does line below work?
# from ._options import locations_to_remove

#for writting location "spoiler" out
import json
LOCATION_BITSHIFT_DEFAULT       = 24

# LocationHelperFile = 'E:\SteamLibrary\steamapps\common\Deep Rock Galactic\FSD\Mods\LocationHelper.txt'


# don't worry about overlapping IDs (or 0 index) here.
# It'll all be resolved by the bitshifting as we expand
# stated keys into actual unique AP locations.
# All the below examples are entirely valid inputs.

#Remap biomes and missions types to be shorter named locations.
#Create secondary objectives as locations
#host.yaml (or something) caches file locations, get file locations from this?
#error checking on location matching done, maybe

Biomes=[
    'Azure Weald',
    'Crystalline Caverns',
    'Fungus Bogs',
    'Hollow Bough',
    'Glacial Strata',
    'Dense Biozone',
    'Magma Core',
    'Radioactive Exclusion Zone',
    'Salt Pits',
    'Sandblasted Corridors',
]

MissionTypes=[
    'Egg Hunt',
    'Elimination',
    'Escort Duty', #requires Carrying
    'Mining Expedition', #Requires morkite mining
    'Point Extraction', #Requires carrying
    'On-site Refining',
    'Salvage Operation', #Requires carrying
    'Deep Scan',
]

SecondaryObjectives=[
    'Glyphid Eggs',
    'Bha Barnacles',
    'Apoca Blooms',
    'Boolo Caps',
    'Ebonuts',
    'Alien Fossils',
    'Gunk Seeds', #Requires Carrying /sometimes/. Might be best to just set as always needed.
    'Fester Fleas',
    'Dystrum',
    'Hollomite',
]

MissionPermute={} #very nested for loop creates array/index/list of all locations that could be read from DRG.
CurrentID=0
for Biome in Biomes:
    for Mission in MissionTypes:
        for Hazard in [1,2,3,4,5]:
            MissionPermute[f'{Biome}:{Mission}:{Hazard}']=CurrentID
            CurrentID=CurrentID+1   

for Biome in Biomes:
    for Secondary in SecondaryObjectives:
        MissionPermute[f'{Biome}:{Secondary}']=CurrentID
        CurrentID=CurrentID+1
#Secondary location, BIOME_LushDownpour:DestroyBhaBarnacles
# 'MissionType_Facility',   #This is win condition only, requires carrying condition
MissionPermute['Magma Core:Industrial Sabotage:5']=CurrentID

CurrentID=0
ForbiddableLocations={}
for Biome in Biomes:
    for Mission in MissionTypes:
        for Hazard in [2,3,4,5]:
            ForbiddableLocations[f'{Biome}:{Mission}:{Hazard}']=CurrentID
            CurrentID=CurrentID+1
for Biome in Biomes:
    for Secondary in SecondaryObjectives:
        ForbiddableLocations[f'{Biome}:{Secondary}']=CurrentID
        CurrentID=CurrentID+1

#This subtracts a number of locations from the pool semi-randomly.
LocationDifference=00
# world.multiworld.random
def remove_random_dict_items(DictStart,DictToRemove, LocationDifference):
    # Get a random sample of keys to remove
    keys_to_remove = random.sample(list(DictToRemove.keys()), LocationDifference)
    # Remove the selected items from the dictionary
    for key in keys_to_remove:
        del DictStart[key]
    return DictStart

MissionPermute = remove_random_dict_items(MissionPermute, ForbiddableLocations, LocationDifference)
#Does this work, YES
#Need to put this in the proper directory though
# with open(LocationHelperFile,'w') as file:
    # file.write("\n".join( list(MissionPermute.keys())) )



LOCATIONS = {k: v + 1 << (LOCATION_BITSHIFT_DEFAULT) for k, v in MissionPermute.items()}

ALL_LOCATIONS = {
    **LOCATIONS,
}

#MissionsDefault is completable under any conditions. Allegedly.
MissionsDefault=[Mission for Mission in LOCATIONS if (
    'Egg Hunt' in Mission or 'Elimination' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
    and ('1' in Mission or '2' in Mission or '3' in Mission)
    ]
    
MissionsDefaultHaz4=[Mission for Mission in LOCATIONS if (
    'Egg Hunt' in Mission or 'Elimination' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
    and '4' in Mission
    ]

MissionsDefaultHaz5=[Mission for Mission in LOCATIONS if (
    'Egg Hunt' in Mission or 'Elimination' in Mission or 'On-site Refining' in Mission or 'Deep Scan' in Mission) \
    and '5' in Mission
    ]
    
MissionsCarrying123=[Mission for Mission in LOCATIONS if (
    'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
    and ('1' in Mission or '2' in Mission or '3' in Mission)
    ]

MissionsCarrying4=[Mission for Mission in LOCATIONS if (
    'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
    and '4' in Mission 
    ]

MissionsCarrying5=[Mission for Mission in LOCATIONS if (
    'Escort Duty' in Mission or 'Point Extraction' in Mission or 'Salvage Operation' in Mission) \
    and '5' in Mission 
    ]

MissionsMining123=[Mission for Mission in LOCATIONS if
    'Mining Expedition' in Mission \
    and ('1' in Mission or '2' in Mission or '3' in Mission)
    ]

MissionsMining4=[Mission for Mission in LOCATIONS if
    'Mining Expedition' in Mission \
    and '4' in Mission
    ]
    
MissionsMining5=[Mission for Mission in LOCATIONS if
    'Mining Expedition' in Mission \
    and '5' in Mission
    ]

#Only one not plural. You probably hate it, change if you want
MissionVictory=[Mission for Mission in LOCATIONS if
    'Industrial Sabotage' in Mission \
    and '5' in Mission
    ]

SecondariesDefault=[Secondary for Secondary in LOCATIONS if (
    'Glyphid Eggs' in Secondary or 'Bha Barnacles' in Secondary or 'Apoca Blooms' in Secondary or 'Boolo Caps' in Secondary \
    or 'Ebonuts' in Secondary or 'Alien Fossils' in Secondary or 'Fester Fleas' in Secondary or 'Dystrum' in Secondary or 'Hollomite' in Secondary)
    ]

SecondariesCarrying=[Secondary for Secondary in LOCATIONS if 'Gunk Seeds' in Secondary]

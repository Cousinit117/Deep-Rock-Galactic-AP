from BaseClasses import MultiWorld
from typing import NamedTuple
from ._subclasses import DRGItem
import random
import settings
import json
LOCATION_BITSHIFT_DEFAULT       = 24

# don't worry about overlapping IDs (or 0 index) here.
# It'll all be resolved by the bitshifting as we expand
# stated keys into actual unique AP locations.
# All the below examples are entirely valid inputs.

#host.yaml (or something) caches file locations, get file locations from this?

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
    'Black Box',
    'Oil Pumping',
    'Scan',
    'Elimination Eggs',
    'Mini Mules',
    'Alien Eggs',
]

Events=[
    'Ebonite Mutation',
    'Kursite Infection',
    'Tritilyte Crystal',
    'Omen Modular Exterminator',
    #'Seasonal 2:Prospector Drone',
    #'Seasonal 2:Prospector Data Deposit',
    #'Seasonal 2:Rival Communication Router',
    #'Seasonal 3:Meteor Impact',
    #'Seasonal 3:Meteor Shower',
    #'Seasonal 4:Rockpox Corruptor',
    #'Seasonal 5:Core Stone',
]

Warnings=[ 
    'Cave Leech Cluster',
    'Elite Threat',
    'Exploder Infestation',
    'Haunted Cave',
    'Lethal Enemies',
    'Lithophage Outbreak',
    'Low Oxygen',
    'Mactera Plague',
    'Parasites',
    'Regenerative Bugs',
    'Rival Presence',
    'Shield Disruption',
    'Swarmageddon',
    'Duck And Cover',
    'Ebonite Outbreak',
]

def location_init():
    MissionPermute={} #very nested for loop creates array/index/list of all locations that could be read from DRG
    CurrentID=0
    # May separate this out. Not sure if that is easier, or if making separate functions to delete specific permutes is easier.
    # e.g. below but for Haz 1, then 2, 
    for Biome in Biomes:
        for Mission in MissionTypes:
            for Hazard in [1,2,3,4,5]:
                MissionPermute[f'{Biome}:{Mission}:{Hazard}']=CurrentID
                CurrentID=CurrentID+1

    #Secondary location, Azure Weald:Bha Barnacles
    for Biome in Biomes:
        for Secondary in SecondaryObjectives:
            MissionPermute[f'{Biome}:{Secondary}']=CurrentID
            CurrentID=CurrentID+1
    
    #Error Cube Checks
    errCubeNum = 10 #self.options.error_cube_checks.value
    if errCubeNum > 0:
        for i in range(1,errCubeNum):
            MissionPermute[f'Error Cube:{i}']=CurrentID
            CurrentID=CurrentID+1

    #Events
    for event in Events:
        for Hazard in [1,2,3,4,5]:
            MissionPermute[f'Event:{event}:{Hazard}']=CurrentID
            CurrentID=CurrentID+1

    #Warnings
    #minwarnlvl = self.options.min_warning_haz.value #unsure please test
    for warn in Warnings:
        for Hazard in [1,2,3,4,5]:
            MissionPermute[f'Warning:{warn}:{Hazard}']=CurrentID
            CurrentID=CurrentID+1

    # 'MissionType_Facility',   #This is win condition only, requires carrying condition
    MissionPermute['Magma Core:Industrial Sabotage:5']=CurrentID

    ALL_LOCATIONS = {k: v + 1 << (LOCATION_BITSHIFT_DEFAULT) for k, v in MissionPermute.items()}
    return ALL_LOCATIONS

def remove_locations(ALL_LOCATIONS, LocationDifference):
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
    # LocationDifference=0    #self.options.locations_to_remove.value
    # world.multiworld.random
    
    def remove_random_dict_items(DictStart,DictToRemove, NumToRemove):
        # Get a random sample of keys to remove
        keys_to_remove = random.sample(list(DictToRemove.keys()), NumToRemove)
        # Remove the selected items from the dictionary
        if NumToRemove > 0:
            for key in keys_to_remove:
                del DictStart[key]
        return DictStart
    TRUNC_ALL_LOCATIONS = remove_random_dict_items(ALL_LOCATIONS, ForbiddableLocations, LocationDifference)    
    return TRUNC_ALL_LOCATIONS

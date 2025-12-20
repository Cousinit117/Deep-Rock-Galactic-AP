from BaseClasses import MultiWorld
from typing import NamedTuple
from .subclasses import DRGItem
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
    #'Magma Core',
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
    'Secondary Scan',
    'Dreadnought Eggs',
    'Mini Mules',
    'Alien Eggs',
]

Events=[
    'Ebonite Mutation',
    'Kursite Infection',
    'Tritilyte Crystal',
    'Omen Modular Exterminator',
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

PassiveCreatures=[
    'LootBug',
    'Huuli Hoarder',
    'Naedocyte Cave Cruiser',
    'Fester Flea',
    'Hexwing Gniffer',
    'Cave Vine',
    'Mobula Cave Angel',
    'Silicate Harvester',
]

EnemiesNormal=[
    'Glyphid Swarmer',
    'Glyphid Exploder',
    'Glyphid Webspitter',
    'Glyphid Grunt',
    'Glyphid Acid Spitter',
    'Glyphid Slasher',
    'Glyphid Septic Spreader',
    'Glyphid Guard',
    'Glyphid Stalker',
    'Glyphid Stingtail',
    'Glyphid Menace',
    'Glyphid Praetorian',
    'Glyphid Warden',
    'Glyphid Opressor',
    'Brood Nexus',
    'Shellback Youngling',
    'Shellback Adult',
    'Nayaka Trawler',
    'Rockpox Exploder',
    'Rockpox Grunt',
    'Rockpox Spitter',
    'Rockpox Praetorian',
    'Rockpox Goo Bomber',
    'Rockpox Naedocyte Breeder',
    'Cave Leech',
    'Vartok Scalebramble',
    'Core Spawn Crawler',
    'Stabber Vine',
    'Spitball Infector',
    'Barrage Infector',
    'Mactera Shooter',
    'Mactera TriJaw',
    'Mactera Grabber',
    'Mactera Brundle',
    'Mactera Goo Bomber',
    'Maedocyte Breeder',
    'Rival Shredder',
    'Rival Sniper Turret',
    'Rival Repulsion Turret',
    'Rival Burst Turret',
    'Rival Patrol Bot',
]

EnemiesBosses=[
    'Glyphid Bulk Detonator',
    'Glyphid Crassus Bulk Detonator',
    'Dreadnaught Arbalest',
    'Dreadnaught Lacerator',
    'Dreadnaught Hiveguard',
    'Glyphid Dreadnaught',
    'Korlok Tyrant Weed',
    'BET-C',
    'Rival Prospector Drone',
    'Rival Nemesis',
    'Rival Caretaker',
]

def getLocationGroup(group = "MainObj"):
    thisList=[]
    match group:
        case "MainObj": #Get Main Objs
            thisList.append('OBJ:Magma Core:Industrial Sabotage:5')
            for Biome in Biomes:
                for Mission in MissionTypes:
                    for Hazard in [1,2,3,4,5]:
                        thisList.append(f'OBJ:{Biome}:{Mission}:{Hazard}')
        case "SecObj": #Get Sec Objs
            for Secondary in SecondaryObjectives:
                for Hazard in [1,2,3,4,5]:
                    thisList.append(f'Secondary:{Secondary}:{Hazard}')
        case "ErrCube":
            for i in range(1,16):
                thisList.append(f'Error Cube:{i}')
        case "Events":
            for event in Events:
                for Hazard in [1,2,3,4,5]:
                    thisList.append(f'Event:{event}:{Hazard}')
        case "Minigames":
            for i in range(5,105,5):
                thisList.append(f'JettyBoot:{i}')
        case "Shop":
            for i in range(1,41):
                thisList.append(f'Shop Item:{i}')
        case "GoldRush":
            thisList.append('Gold Rush:RICH')
            for i in range(50,20050,50):
                thisList.append(f'Gold Rush:{i}')
        case "Warnings":
            for warn in Warnings:
                for Hazard in [1,2,3,4,5]:
                    thisList.append(f'Warning:{warn}:{Hazard}')
        case "HunterNormal":
            for hunt in EnemiesNormal:
                for i in range(1,11):
                    thisList.append(f'Hunting Trophy:{hunt}:{i}')
        case "HunterBoss":
            thisList.append('Trophy Hunter:MASTERED')
            for hunt in EnemiesBosses:
                for i in range(1,6):
                    thisList.append(f'Hunting Boss Trophy:{hunt}:{i}')
        case "HunterPassive":
            for hunt in PassiveCreatures:
                for i in range(1,11):
                    thisList.append(f'Hunting Trophy:{hunt}:{i}')

    return thisList

def location_init():
    MissionPermute={} #very nested for loop creates array/index/list of all locations that could be read from DRG
    CurrentID=0
    # May separate this out. Not sure if that is easier, or if making separate functions to delete specific permutes is easier.
    # e.g. below but for Haz 1, then 2,

    #Mission Obj Locations
    ObjList = getLocationGroup("MainObj")
    for x in ObjList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Secondary locations
    SecList = getLocationGroup("SecObj")
    for x in SecList:
        MissionPermute[x]=CurrentID
        CurrentID+=1
    
    #Error Cube Checks
    ErrList = getLocationGroup("ErrCube")
    for x in ErrList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Events
    EvList = getLocationGroup("Events")
    for x in EvList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Minigames
    MGList = getLocationGroup("Minigames")
    for x in MGList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Shop Items
    ShopList = getLocationGroup("Shop")
    for x in ShopList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Gold Rush
    GoldList = getLocationGroup("GoldRush")
    for x in GoldList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Warnings
    WarnList = getLocationGroup("Warnings")
    for x in WarnList:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    #Hunting Goal
    HuntList1 = getLocationGroup("HunterNormal")
    for x in HuntList1:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    HuntList2 = getLocationGroup("HunterBoss")
    for x in HuntList2:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    HuntList3 = getLocationGroup("HunterPassive")
    for x in HuntList3:
        MissionPermute[x]=CurrentID
        CurrentID+=1

    ALL_LOCATIONS = {k: v + 1 << (LOCATION_BITSHIFT_DEFAULT) for k, v in MissionPermute.items()}
    return ALL_LOCATIONS

def remove_locations(ALL_LOCATIONS, LocationDifference, Cubes = 10, MiniGames = True,\
    MGMax = 30, Goal = 1, GoldRushVal = 15000, ShopItems = 25, EventsOn = True, MaxHaz = 5,\
    HunterNum = 5, HunterTargets = 1):
    CurrentID=0
    RemovableLocations=[]
    MustRemove=[]
    ValidHaz=[2,3,4,5]
    RemoveHaz=[]
    #generate Haz Removal
    match MaxHaz:
        case 3:
            ValidHaz=[2,3]
            RemoveHaz=[4,5]
        case 4:
            ValidHaz=[2,3,4]
            RemoveHaz=[5]
        case _:
            ValidHaz=[2,3,4,5]
            RemoveHaz=[]

    #Handle Goal Objectives Caretaker
    if Goal == 1: #Only Removable if Possible with Goal 1
        for Biome in Biomes:
            for Mission in MissionTypes:
                for Hazard in ValidHaz:
                    RemovableLocations.append(f'OBJ:{Biome}:{Mission}:{Hazard}')
                for Hazard in RemoveHaz:
                    MustRemove.append(f'OBJ:{Biome}:{Mission}:{Hazard}')
    
    #Handle Secondary objectives
    for Secondary in SecondaryObjectives:
        for Hazard in ValidHaz:
            RemovableLocations.append(f'Secondary:{Secondary}:{Hazard}')
        for Hazard in RemoveHaz:
            MustRemove.append(f'Secondary:{Secondary}:{Hazard}')
    
    #Handle Minigames
    if not MiniGames:
        MustRemove.extend(getLocationGroup("Minigames"))
    
    #Handle Events
    if not EventsOn:
        MustRemove.extend(getLocationGroup("Events"))
    for event in Events:
        for Hazard in RemoveHaz:
            MustRemove.append(f'Event:{event}:{Hazard}')

    #Handle Cubes
    for i in range(15,Cubes,-1):
        MustRemove.append(f'Error Cube:{i}')

    #Handle Shop Items
    for i in range(40,ShopItems,-1):
        MustRemove.append(f'Shop Item:{i}')

    #Minigames
    for i in range(100,MGMax,-5):
        MustRemove.append(f'JettyBoot:{i}')

    #Handle GoldRush Gold value
    for i in range(20000,GoldRushVal,-50):
        MustRemove.append(f'Gold Rush:{i}')

    #Handle Warnings
    for warn in Warnings:
        for Hazard in RemoveHaz:
           MustRemove.append(f'Warning:{warn}:{Hazard}')

    #Handle Trophy Hunter
    match HunterTargets:
        case 2: #only bosses
            MustRemove.extend(getLocationGroup("HunterNormal"))
            MustRemove.extend(getLocationGroup("HunterPassive"))
        case 3: #no passives
            MustRemove.extend(getLocationGroup("HunterPassive"))
    for hunt in EnemiesNormal:
        for i in range(10,HunterNum,-1):
            thisList.append(f'Hunting Trophy:{hunt}:{i}')
    for hunt in PassiveCreatures:
        for i in range(10,HunterNum,-1):
            thisList.append(f'Hunting Trophy:{hunt}:{i}')
    for hunt in EnemiesBosses:
        for i in range(5,round(HunterNum/2),-1):
            thisList.append(f'Hunting Boss Trophy:{hunt}:{i}')

    #Handle Goal Removals
    match Goal:
        case 1: #default ind sabo haz 5
            MustRemove.extend(getLocationGroup("GoldRush"))
            MustRemove.extend(getLocationGroup("HunterNormal"))
            MustRemove.extend(getLocationGroup("HunterBoss"))
            MustRemove.extend(getLocationGroup("HunterPassive"))
        case 2: #goldrush
            MustRemove.extend(getLocationGroup("MainObj"))
            MustRemove.extend(getLocationGroup("HunterNormal"))
            MustRemove.extend(getLocationGroup("HunterBoss"))
            MustRemove.extend(getLocationGroup("HunterPassive"))
        case 3: #hunter
            MustRemove.extend(getLocationGroup("MainObj"))
            MustRemove.extend(getLocationGroup("GoldRush"))
        #case 4: #world tour
        case _:
            #Remove Goldrush Goals, locations -401
            MustRemove.extend(getLocationGroup("GoldRush"))
            MustRemove.extend(getLocationGroup("HunterNormal"))
            MustRemove.extend(getLocationGroup("HunterBoss"))
            MustRemove.extend(getLocationGroup("HunterPassive"))
            print(f"Goal is defaulted. This shouldn't happen! PANIC!")

    #This subtracts a number of locations from the pool semi-randomly.
    # LocationDifference=0    #self.options.locations_to_remove.value
    # world.multiworld.random
    
    def remove_random_dict_items(DictStart, DictRemoveRand, DictRemoveMust, NumToRemove):
        
        keys_must = DictRemoveMust
        for key in keys_must:
            if key in DictStart:
                del DictStart[key]
                #NumToRemove -= 1

        # Remove the selected items from the dictionary
        if NumToRemove > 0:
            keys_to_remove = random.sample(DictRemoveRand, NumToRemove)
            for key in keys_to_remove:
                del DictStart[key]
        return DictStart
    
    TRUNC_ALL_LOCATIONS = remove_random_dict_items(ALL_LOCATIONS, RemovableLocations, MustRemove, LocationDifference)    
    return TRUNC_ALL_LOCATIONS

from typing import NamedTuple
from enum import IntEnum, IntFlag, Enum, auto
from BaseClasses import Item, ItemClassification as IC

from .subclasses import DRGItem
ITEM_BITSHIFT_DEFAULT = 8

class GroupTag(IntFlag):
    Equipment = auto()
    Movement = auto()
    Carrying = auto()
    Mining = auto()
    Stats = auto()
    Melee = auto()
    Perks = auto()
    Weapon = auto()
    Other = auto()
    Bosco = auto()
    Mutator = auto()
    Biome = auto()

class ItemData(NamedTuple):
    #item_id: int | None
    tags: GroupTag | None = None
    mandatory:   int = 0
    progression: int = 0
    useful:      int = 0
    filler:      int = 0
    trap:        int = 0

ITEMS = {
#Progression, highest number among items is now 131
    'Progressive-Flare-Count': 47,
    'Progressive-Flare-Recharge':1,
    'Progressive-Carriable-Throwing':2,
    'Progressive-Carrying-Speed':3, 
    'Progressive-Morkite-Mining':4,
    'Progressive-Movement-Speed':5,
    'Progressive-RedSugar-Healing':6,
    'Progressive-Resupply-Speed':7,
    'Progressive-Max-Health': 8,
    'Progressive-Max-Shield':9,
    'Progressive-Shield-Regen-Delay':10,
    'Progressive-Jet-Boots':11, #Cannot go over 2 (as in useless)
    'Progressive-Melee-Damage':12,
    'Progressive-Melee-Special-Damage':13, #Generally shouldn't go over 4
    'Progressive-Melee-Cooldown': 14,
    'Progressive-Melee-Range': 15,
    'Progressive-Vampirism': 16, #Currently no effect over 1, plan to change later.
    'Progressive-Thorns': 17, #Currently no effect over 1, plan to change later.
    'Progressive-Steve-Cooldown': 18,
    'Progressive-Berzerker': 19, #No effect above 7
    'Progressive-Field-Medic': 20,
    'Progressive-Iron-Will': 21,
    'Progressive-Gun-Ammo': 22,
    'Progressive-Traversal-Tool': 23,
    'Progressive-Utility': 24,
    'Progressive-Grenades': 25,
    'Progressive-Resupply-Incremental-Cost':48,
    'Progressive-Resupply-Start-Cost':49,
    'Progressive-Bosco-Revive':50,
    'Progressive-Bosco-Gun':51, 
#Usefuls
    'Progressive-Flare-Throwing': 26, #Gets to be a trap/bad if over like 12
    'Progressive-Deposit-Speed': 27,
    'Progressive-Fall-Resistance': 28, #No effect over 7
    'Progressive-Sprint-Speed': 29,
    'Progressive-Max-Shield-Regen': 30,
    'Supply-Sentries': 31, #Cannot go over 1
    'Progressive-Rock-Mining': 32, #Cannot go over 2 
    'Dirt-Mining-Speed': 33, #Cannot go over 1
    'Progressive-Hover-Boots': 34, #Should not exceed 4, may break. (Clamped at .5s)
    'Progressive-See-You-In-Hell': 35, #May break over 4, not sure. would set cooldown to negative. (Clamped at .5s)
    'Progressive-Bosco-Mining':69,
#filler
    'Progressive-Carrying-Capacity': 36,
    'Progressive-Gold-Mining': 37, #No benefit to player, gold unused.
    'Resource-Mining-Strength': 38, #No effect above 1
    'Progressive-Gunner-Zipline': 39, #Higher than I want, but w/e
    'Progressive-Slow-Resistance': 40,
    'Progressive-Revive-Speed': 41,
    'Progressive-Cold-Resistance': 42, #max 2 currently for below checks.
    'Progressive-Poison-Resistance': 43,
    'Progressive-Fire-Resistance': 44,
    'Progressive-Radiation-Resistance': 45,
    'Progressive-Electric-Resistance': 46, #47 is start of list
    'Progressive-BET-C': 57,
#traps
    'Trap-Extraction-Bulk': 52, #once per trap? MULTI OR SINGLE
    'Trap-Cave-Haunting': 53, #one off, SINGLE
    'Trap-Bedrock-Encasing': 54, #triggers once per trap, MULTI
    'Trap-MULE-Coolant-Leak': 55, #one misson per trap?, MULTI OR SINGLE
    'Trap-Not-The-Bees': 56, #triggers per trap, MULTI
    'Trap-Phase-Bomb': 58, #trigger per trap, MULTI
    'Trap-Jumpscare-Bulk': 59, #trigger per trap, MULTI
    'Trap-Intoxication': 60, #trigger per trap, MULTI
#anomolies
    'Mutator-Critical-Weakness': 61,
    'Mutator-Gold-Rush': 62,
    'Mutator-Golden-Bugs': 63,
    'Mutator-Low-Gravity': 64,
    'Mutator-Mineral-Mania': 65,
    'Mutator-Rich-Atmosphere': 66,
    'Mutator-Volatile-Guts': 67,
    'Mutator-Blood-Sugar': 68,
    #Skipped double exp and secret secondary
#class progressives
    'Progressive-Gunner-Shield':70,
    'Progressive-Engineer-Platforms':71,
    'Progressive-Engineer-Turrets':72,
    'Progressive-Scout-Grapple':73,
    'Progressive-Scout-FlareGun':74,
    'Progressive-Driller-Drills':75,
    'Progressive-Driller-C4':76,
    'Class-Gunner':77,
    'Class-Driller':78,
    'Class-Scout':79,
    'Class-Engineer':80,
    'Progressive-Gear-Upgrades':83,
    'Overclocks-Unlocked':84,
#spacerig stuff
    'Open-Bar':81,
    'Free-Drink':82,
#missing perks
    'Progressive-Dash':85,
    'Progressive-Heightened-Senses':86,
    'Progressive-Born-Ready':87,
#junk / nothing items
    'Beard-Waxing':88,
    'Hydrate-Water':89,
    'Gnome-Spray':90,
    'Takeout-Food-Order':91,
    'Mushroom':92,
    'Gold-Chunk':93,
    'APCoin-1':129,
    'APCoin-5':130,
    'APCoin-10':131,
#biome Items
    'Biome-Azure-Weald':94,
    'Biome-Crystalline-Caverns':95,
    'Biome-Fungus-Bogs':96,
    'Biome-Hollow-Bough':97,
    'Biome-Glacial-Strata':98,
    'Biome-Dense-Biozone':99,
    'Biome-Magma-Core':100,
    'Biome-Radioactive-Exclusion-Zone':101,
    'Biome-Salt-Pits':102,
    'Biome-Sandblasted-Corridors':103,
    'Biome-Ossuary-Depths':104,
#weapon Items Primary
    'Driller-Flamethrower':105,
    'Driller-Cryo':106,
    'Driller-SludgePump':107,
    'Engineer-Warthog-Shotgun':108,
    'Engineer-Stubby-SMG':109,
    'Engineer-LOK1-Rifle':110,
    'Gunner-Minigun':111,
    'Gunner-Autocanon':112,
    'Gunner-Guided-Rocket':113,
    'Scout-Assault-Rifle':114,
    'Scout-M1000-Sniper':115,
    'Scout-Plasma-Carbine':116,
#Weapon Items Secondary
    'Driller-Pistol':117,
    'Driller-Plasma-Charger':118,
    'Driller-Wave-Cooker':119,
    'Engineer-Deepcore-PGL':120,
    'Engineer-Breach-Cutter':121,
    'Engineer-Shard-Diffractor':122,
    'Gunner-Revolver':123,
    'Gunner-Burstfire-Pistol':124,
    'Gunner-Coil-Gun':125,
    'Scout-Boomstick-Shotgun':126,
    'Scout-Dual-Pistols':127,
    'Scout-Crossbow':128,
#Gauntlet
    'Progressive-Gauntlet-Stage':132,
}
ITEMS = {k: v + 1 << ITEM_BITSHIFT_DEFAULT for k, v in ITEMS.items()}

ITEMS_COUNT = {
    'Progressive-Flare-Count':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=1,
        filler=6,
),
    'Progressive-Flare-Recharge':ItemData(
        tags = GroupTag.Equipment,
        progression=2,
        filler=2,
),
    'Progressive-Carriable-Throwing':ItemData(
        tags = GroupTag.Carrying,
        mandatory=2,
        progression=3,
        useful=5,
        filler=20,
),
    'Progressive-Carrying-Speed': ItemData(
        tags = GroupTag.Carrying,
        mandatory=2,
        progression=3,
        useful=7,
        filler=7,
),
    'Progressive-Morkite-Mining':ItemData(
        tags = GroupTag.Mining,
        mandatory=2,
        progression=1,
        useful=7,
        filler=5,
),
    'Progressive-Movement-Speed':ItemData(
        tags = GroupTag.Movement,
        mandatory=3,
        progression=3,
        useful=6,
),
    'Progressive-RedSugar-Healing':ItemData(
        tags = GroupTag.Stats,
        progression=2,
        useful=3,
        filler=5,
),
    'Progressive-Resupply-Speed':ItemData(
        tags = GroupTag.Stats,
        mandatory=1,
        progression=1,
        useful=5,
        filler=5,
),
    'Progressive-Max-Health':ItemData(
        tags = GroupTag.Stats,
        mandatory=5,
        progression=10,
        useful=10,
),
    'Progressive-Max-Shield':ItemData(
        tags = GroupTag.Stats,
        mandatory=3,
        progression=2,
        useful=5,
        filler=5,
),
    'Progressive-Shield-Regen-Delay':ItemData(
        tags = GroupTag.Stats,
        mandatory=2,
        progression=2,
        useful=3,
),
    'Progressive-Jet-Boots':ItemData(
        tags = GroupTag.Movement,
        progression=2,
),
    'Progressive-Melee-Damage':ItemData(
        tags = GroupTag.Melee,
        progression=10,
        filler=5,
),
    'Progressive-Melee-Special-Damage':ItemData(
        tags = GroupTag.Melee,
        progression=10,
        filler=5,
),
    'Progressive-Melee-Cooldown':ItemData(
        tags = GroupTag.Melee,
        progression=5,
),
    'Progressive-Melee-Range':ItemData(
        tags = GroupTag.Melee,
        progression=5,
        useful=10,
),
    'Progressive-Vampirism':ItemData(
        tags = GroupTag.Perks,
        progression=1,
),
    'Progressive-Thorns':ItemData(
        tags = GroupTag.Perks,
        progression=1,
),
    'Progressive-Steve-Cooldown':ItemData(
        tags = GroupTag.Perks,
        progression=1,
        useful=3,
),
    'Progressive-Berzerker':ItemData(
        tags = GroupTag.Perks,
        progression=6,
),
    'Progressive-Field-Medic':ItemData(
        tags = GroupTag.Perks,
        progression=2,
        useful=8,
),
    'Progressive-Iron-Will':ItemData(
        tags = GroupTag.Perks,
        mandatory=1,
        progression=9,
),
    'Progressive-Gun-Ammo':ItemData(
        tags = GroupTag.Weapon,
        mandatory=3,
        progression=2,
        useful=5,
        filler=5,
),
    'Progressive-Traversal-Tool':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=4,
        useful=5,
),
    'Progressive-Utility':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=4,
        useful=5,
),
    'Progressive-Grenades':ItemData(
        tags = GroupTag.Weapon,
        mandatory=2,
        progression=4,
        useful=4,
),       
    'Progressive-Resupply-Incremental-Cost':ItemData(
        tags = GroupTag.Equipment,
        progression=3,
),
    'Progressive-Resupply-Start-Cost':ItemData(
        tags = GroupTag.Equipment,
        progression=4,
        useful=1,
),  
    'Progressive-Flare-Throwing':ItemData(
        tags = GroupTag.Equipment,
        useful=6,
        filler=7,
),
    'Progressive-Deposit-Speed':ItemData(
        tags = GroupTag.Equipment,
        useful=2,
        filler=10,
),
    'Progressive-Fall-Resistance':ItemData(
        tags = GroupTag.Stats,
        useful=6,
        filler=0,
),
    'Progressive-Sprint-Speed':ItemData(
        tags = GroupTag.Movement,
        useful=5,
        filler=5,
),
    'Progressive-Max-Shield-Regen':ItemData(
        tags = GroupTag.Stats,
        useful=18,
),
    'Supply-Sentries':ItemData(
        tags = GroupTag.Other,
        useful=10,
),
    'Progressive-Rock-Mining':ItemData(
        tags = GroupTag.Mining,
        useful=2,
),
    'Dirt-Mining-Speed':ItemData(
        tags = GroupTag.Mining,
        useful=1,
),
    'Progressive-Hover-Boots':ItemData(
        tags = GroupTag.Perks,
        useful=4,
),
    'Progressive-See-You-In-Hell':ItemData(
        tags = GroupTag.Perks,
        useful=4,
),
    'Progressive-Carrying-Capacity':ItemData(
        tags = GroupTag.Carrying,
        mandatory=1,
        progression=1,
        useful=6,
        filler=10,
),
    'Progressive-Gold-Mining':ItemData(
        tags = GroupTag.Mining,
        filler=5,
),
    'Resource-Mining-Strength':ItemData(
        tags = GroupTag.Mining,
        filler=1,
),
    'Progressive-Gunner-Zipline':ItemData(
        tags = GroupTag.Equipment,
        filler=5,
),
    'Progressive-Slow-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=5,
),
    'Progressive-Revive-Speed':ItemData(
        tags = GroupTag.Stats,
        filler=10,
),
    'Progressive-Cold-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=2,
),
    'Progressive-Poison-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=2,
),
    'Progressive-Fire-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=2,
),
    'Progressive-Radiation-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=2,
),
    'Progressive-Electric-Resistance':ItemData(
        tags = GroupTag.Stats,
        filler=2,
),
    'Progressive-Bosco-Revive':ItemData(
        tags = GroupTag.Bosco,
        mandatory=1,
        progression=3,
        useful=4,
),
    'Progressive-Bosco-Gun':ItemData(
        tags = GroupTag.Bosco,
        mandatory=2,
        progression=2,
        useful=4,
),
    'Trap-Extraction-Bulk':ItemData(
        tags = GroupTag.Other,
        trap=5,
),
    'Trap-Cave-Haunting':ItemData(
        tags = GroupTag.Other,
        trap=5,
),
    'Trap-Bedrock-Encasing':ItemData(
        tags = GroupTag.Other,
        trap=5,
),
    'Trap-MULE-Coolant-Leak':ItemData(
        tags = GroupTag.Other,
        trap=3,
),
    'Trap-Not-The-Bees':ItemData(
        tags = GroupTag.Other,
        trap=10,
),
    'Trap-Phase-Bomb':ItemData(
        tags = GroupTag.Other,
        trap=10,
),
    'Trap-Jumpscare-Bulk':ItemData(
        tags = GroupTag.Other,
        trap=5,
),
    'Progressive-BET-C':ItemData(
        tags = GroupTag.Other,
        filler=3,
),
    'Trap-Intoxication':ItemData(
        tags = GroupTag.Other,
        trap=5,
),
    'Mutator-Critical-Weakness':ItemData(
        tags = GroupTag.Mutator,
        useful=2,
),
    'Mutator-Gold-Rush':ItemData(
        tags = GroupTag.Mutator,
        filler=2,
),
    'Mutator-Golden-Bugs':ItemData(
        tags = GroupTag.Mutator,
        filler=2,
),
    'Mutator-Low-Gravity':ItemData(
        tags = GroupTag.Mutator,
        useful=1,
        filler=1,
),
    'Mutator-Mineral-Mania':ItemData(
        tags = GroupTag.Mutator,
        filler=2,
),
    'Mutator-Rich-Atmosphere':ItemData(
        tags = GroupTag.Mutator,
        useful=1,
        filler=1,
),
    'Mutator-Volatile-Guts':ItemData(
        tags = GroupTag.Mutator,
        filler=2,
),
    'Mutator-Blood-Sugar':ItemData(
        tags = GroupTag.Mutator,
        filler=2,
),
    'Progressive-Bosco-Mining':ItemData(
        tags = GroupTag.Bosco,
        filler=5,
),
    'Progressive-Gunner-Shield':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=1,
        useful=3,
),
    'Progressive-Engineer-Platforms':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=2,
        useful=3,
),
    'Progressive-Engineer-Turrets':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        useful=3,
        filler=1,
),
    'Progressive-Scout-Grapple':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=1,
        useful=4,
),
    'Progressive-Scout-FlareGun':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=1,
        useful=4,
),
    'Progressive-Driller-Drills':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=2,
        useful=4,
),
    'Progressive-Driller-C4':ItemData(
        tags = GroupTag.Equipment,
        mandatory=1,
        progression=1,
        useful=4,
),
    'Class-Gunner':ItemData(
        tags = GroupTag.Other,
        mandatory=1,
),
    'Class-Driller':ItemData(
        tags = GroupTag.Other,
        mandatory=1,
),
    'Class-Scout':ItemData(
        tags = GroupTag.Other,
        mandatory=1,
),
    'Class-Engineer':ItemData(
        tags = GroupTag.Other,
        mandatory=1,
),
    'Open-Bar':ItemData(
        tags = GroupTag.Other,
        progression=1,
),
    'Free-Drink':ItemData(
        tags = GroupTag.Other,
        filler=25,
),
    'Overclocks-Unlocked':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Progressive-Gear-Upgrades':ItemData(
        tags = GroupTag.Weapon,
        mandatory=5,
        useful=3,
),
    'Progressive-Dash':ItemData(
        tags = GroupTag.Perks,
        useful=6,
        filler=0,
),
    'Progressive-Heightened-Senses':ItemData(
        tags = GroupTag.Perks,
        useful=6,
),
    'Progressive-Born-Ready':ItemData(
        tags = GroupTag.Perks,
        useful=1,
),
    'Biome-Azure-Weald':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Crystalline-Caverns':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Fungus-Bogs':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Hollow-Bough':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Glacial-Strata':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Dense-Biozone':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Magma-Core':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Radioactive-Exclusion-Zone':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Salt-Pits':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Sandblasted-Corridors':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Biome-Ossuary-Depths':ItemData(
        tags = GroupTag.Biome,
        mandatory=1,
),
    'Driller-Flamethrower':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Driller-Cryo':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Driller-SludgePump':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-Warthog-Shotgun':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-Stubby-SMG':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-LOK1-Rifle':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Minigun':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Autocanon':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Guided-Rocket':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-Assault-Rifle':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-M1000-Sniper':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-Plasma-Carbine':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Driller-Pistol':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Driller-Plasma-Charger':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Driller-Wave-Cooker':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-Deepcore-PGL':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-Breach-Cutter':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Engineer-Shard-Diffractor':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Revolver':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Burstfire-Pistol':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Gunner-Coil-Gun':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-Boomstick-Shotgun':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-Dual-Pistols':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
    'Scout-Crossbow':ItemData(
        tags = GroupTag.Weapon,
        mandatory=1,
),
}

EVENT_ITEMS= {
  'Victory':2^20-8
}

ALL_ITEMS = {
    # we utilize the **dict syntax to expand each dictionary out into literal componenents
    **ITEMS,
    **EVENT_ITEMS,
}

EXTRA_FILLER_ITEMS = [
    #Contains only extra items used for filler generation
    'Free-Drink',
    'APCoin-1',
    'APCoin-5',
    'APCoin-10',
]

DEPRECIATED_ITEMS = [
    #Contains only extra items used for filler generation
    'Beard-Waxing',
    'Hydrate-Water',
    'Gnome-Spray',
    'Takeout-Food-Order',
    'Mushroom',
    'Gold-Chunk',
]

#Item group hardcode
Generic_Progressives = [ #Includes most but not all of progression checks. 
    'Progressive-Flare-Count',
    'Progressive-Flare-Recharge',
    'Progressive-Movement-Speed',
    'Progressive-RedSugar-Healing',
    'Progressive-Resupply-Speed',
    'Progressive-Max-Health',
    'Progressive-Max-Shield',
    'Progressive-Shield-Regen-Delay',
    'Progressive-Jet-Boots',
    'Progressive-Melee-Damage',
    'Progressive-Melee-Special-Damage',
    'Progressive-Melee-Cooldown',
    'Progressive-Melee-Range',
    'Progressive-Vampirism',
    'Progressive-Thorns',
    'Progressive-Steve-Cooldown',
    'Progressive-Berzerker',
    'Progressive-Field-Medic',
    'Progressive-Iron-Will',
    'Progressive-Gun-Ammo',
    'Progressive-Traversal-Tool',
    'Progressive-Utility',
    'Progressive-Grenades',
    'Class-Gunner',
    'Class-Driller',
    'Class-Scout',
    'Class-Engineer',
    'Progressive-Gear-Upgrades',
    'Overclocks-Unlocked',
]
Carrying_Buffs = [
    'Progressive-Carriable-Throwing',
    'Progressive-Carrying-Speed',
]

#Checks for Generation
CLASS_ITEM_CHECK = [
    'Class-Gunner',
    'Class-Driller',
    'Class-Scout',
    'Class-Engineer',
]

BIOME_ITEM_CHECK = [
    'Biome-Azure-Weald',
    'Biome-Crystalline-Caverns',
    'Biome-Fungus-Bogs',
    'Biome-Hollow-Bough',
    'Biome-Glacial-Strata',
    'Biome-Dense-Biozone',
    'Biome-Magma-Core',
    'Biome-Radioactive-Exclusion-Zone',
    'Biome-Salt-Pits',
    'Biome-Sandblasted-Corridors',
    'Biome-Ossuary-Depths',
]

WEAPONS_PRIMARY = [
    'Driller-Flamethrower',
    'Driller-Cryo',
    'Driller-SludgePump',
    'Engineer-Warthog-Shotgun',
    'Engineer-Stubby-SMG',
    'Engineer-LOK1-Rifle',
    'Gunner-Minigun',
    'Gunner-Autocanon',
    'Gunner-Guided-Rocket',
    'Scout-Assault-Rifle',
    'Scout-M1000-Sniper',
    'Scout-Plasma-Carbine',
]

WEAPONS_SECONDARY = [
    'Driller-Pistol',
    'Driller-Plasma-Charger',
    'Driller-Wave-Cooker',
    'Engineer-Deepcore-PGL',
    'Engineer-Breach-Cutter',
    'Engineer-Shard-Diffractor',
    'Gunner-Revolver',
    'Gunner-Burstfire-Pistol',
    'Gunner-Coil-Gun',
    'Scout-Boomstick-Shotgun',
    'Scout-Dual-Pistols',
    'Scout-Crossbow',
]

#Checks for Sprint Enabled
SPRINT_ITEM_CHECK = [
    'Progressive-Movement-Speed',
]

GAUNTLET_ITEMS = [
    'Progressive-Gauntlet-Stage',
]
#state.has_from_list(Generic_Progressives,player,5)
#has_from_list(self, items: Iterable[str], player: int, count: int) 
#count_from_list(self, items: Iterable[str], player: int) -> int:
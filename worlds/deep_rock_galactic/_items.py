from typing import NamedTuple

from ._subclasses import DRGItem

ITEM_BITSHIFT_DEFAULT       = 16





#Do we need to add "Victory" as an item? And force its location to be on the Haz 5 sabotage?

class ItemData(NamedTuple):
    progression: int = 0
    useful:      int = 0
    filler:      int = 0
    trap:        int = 0



ITEMS = {
#Progression
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
#Usefuls
    'Progressive-Flare-Throwing': 26, #Gets to be a trap/bad if over like 12
    'Progressive-Deposit-Speed': 27,
    'Progressive-Fall-Resistance': 28, #No effect over 7
    'Progressive-Sprint-Speed': 29,
    'Progressive-Max-Shield-Regen': 30,
    'Supply-Sentries': 31, #Cannot go over 1
    'Progressive-Rock-Mining': 32, #Cannot go over 2 
    'Dirt-Mining-Speed': 33, #Cannot go over 1
    'Progressive-Hover-Boots': 34, #Should not exceed 4, may break.
    'Progressive-See-You-In-Hell': 35, #May break over 4, not sure. would set cooldown to negative.
#filler
    'Progressive-Carrying-Capacity': 36,
    'Progressive-Gold-Mining': 37, #No benefit to player, gold unused.
    'Resource-Mining-Strength': 38, #No effect above 1
    'Progressive-Zipline-Speed': 39, #Higher than I want, but w/e
    'Progressive-Slow-Resistance': 40,
    'Progressive-Revive-Speed': 41,
    'Progressive-Cold-Resistance': 42, #max 2 currently for below checks.
    'Progressive-Poison-Resistance': 43,
    'Progressive-Fire-Resistance': 44,
    'Progressive-Radiation-Resistance': 45,
    'Progressive-Electric-Resistance': 46, #47 is start of list

}
ITEMS = {k: v + 1 << ITEM_BITSHIFT_DEFAULT for k, v in ITEMS.items()}

ITEMS_COUNT = {
    'Progressive-Flare-Count':ItemData(
        progression=2,
        useful=0,
        filler=6,
),
    'Progressive-Flare-Recharge':ItemData(
        progression=2,
        useful=0,
        filler=2,
),
    'Progressive-Carriable-Throwing':ItemData(
        progression=5,
        useful=5,
        filler=20,
),
    'Progressive-Carrying-Speed': ItemData(
        progression=5,
        useful=7,
        filler=7,
),
    'Progressive-Morkite-Mining':ItemData(
        progression=3,
        useful=7,
        filler=5,
),
    'Progressive-Movement-Speed':ItemData(
        progression=6,
        useful=5,
        filler=20,#should be 0
),
    'Progressive-RedSugar-Healing':ItemData(
        progression=2,
        useful=3,
        filler=15,#was 5
),
    'Progressive-Resupply-Speed':ItemData(
        progression=2,
        useful=10,
        filler=10,#was 0
),
    'Progressive-Max-Health':ItemData(
        progression=15,
        useful=10,
        filler=20,#was 0
),
    'Progressive-Max-Shield':ItemData(
        progression=5,
        useful=5,
        filler=0,
),
    'Progressive-Shield-Regen-Delay':ItemData(
        progression=4,
        useful=3,
        filler=0,
),
    'Progressive-Jet-Boots':ItemData(
        progression=2,
        useful=0,
        filler=0,
),
    'Progressive-Melee-Damage':ItemData(
        progression=10,
        useful=0,
        filler=10,#was 0
),
    'Progressive-Melee-Special-Damage':ItemData(
        progression=10,
        useful=0,
        filler=10,#was 0
),
    'Progressive-Melee-Cooldown':ItemData(
        progression=4,
        useful=0,
        filler=0,
),
    'Progressive-Melee-Range':ItemData(
        progression=5,
        useful=10,
        filler=10,#was 0
),
    'Progressive-Vampirism':ItemData(
        progression=1,
        useful=0,
        filler=0,
),
    'Progressive-Thorns':ItemData(
        progression=1,
        useful=0,
        filler=0,
),
    'Progressive-Steve-Cooldown':ItemData(
        progression=1,
        useful=3,
        filler=0,
),
    'Progressive-Berzerker':ItemData(
        progression=6,
        useful=0,
        filler=0,
),
    'Progressive-Field-Medic':ItemData(
        progression=2,
        useful=8,
        filler=0,
),
    'Progressive-Iron-Will':ItemData(
        progression=10,
        useful=0,
        filler=0,
),
    'Progressive-Gun-Ammo':ItemData(
        progression=5,
        useful=0,
        filler=0,
),
    'Progressive-Traversal-Tool':ItemData(
        progression=2,
        useful=0,
        filler=0,
),
    'Progressive-Utility':ItemData(
        progression=2,
        useful=0,
        filler=0,
),
    'Progressive-Grenades':ItemData(
        progression=9,
        useful=0,
        filler=0,
),
    'Progressive-Flare-Throwing':ItemData(
        progression=0,
        useful=6,
        filler=7,
),
    'Progressive-Deposit-Speed':ItemData(
        progression=0,
        useful=2,
        filler=15,
),
    'Progressive-Fall-Resistance':ItemData(
        progression=0,
        useful=6,
        filler=0,
),
    'Progressive-Sprint-Speed':ItemData(
        progression=0,
        useful=5,
        filler=25,#was 15
),
    'Progressive-Max-Shield-Regen':ItemData(
        progression=0,
        useful=19,
        filler=0,
),
    'Supply-Sentries':ItemData(
        progression=0,
        useful=1,
        filler=0,
),
    'Progressive-Rock-Mining':ItemData(
        progression=0,
        useful=2,
        filler=0,
),
    'Dirt-Mining-Speed':ItemData(
        progression=0,
        useful=1,
        filler=0,
),
    'Progressive-Hover-Boots':ItemData(
        progression=0,
        useful=4,
        filler=0,
),
    'Progressive-See-You-In-Hell':ItemData(
        progression=0,
        useful=4,
        filler=0,
),
    'Progressive-Carrying-Capacity':ItemData(
        progression=0,
        useful=8,
        filler=12,
),
    'Progressive-Gold-Mining':ItemData(
        progression=0,
        useful=0,
        filler=9,
),
    'Resource-Mining-Strength':ItemData(
        progression=0,
        useful=0,
        filler=1,
),
    'Progressive-Zipline-Speed':ItemData(
        progression=0,
        useful=0,
        filler=16,
),
    'Progressive-Slow-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=5,
),
    'Progressive-Revive-Speed':ItemData(
        progression=0,
        useful=0,
        filler=20,#was 10
),
    'Progressive-Cold-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=2,
),
    'Progressive-Poison-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=2,
),
    'Progressive-Fire-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=2,
),
    'Progressive-Radiation-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=2,
),
    'Progressive-Electric-Resistance':ItemData(
        progression=0,
        useful=0,
        filler=2,
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
]
Carrying_Buffs = [
'Progressive-Carriable-Throwing',
'Progressive-Carrying-Speed',
]
#state.has_from_list(Generic_Progressives,player,5)
#has_from_list(self, items: Iterable[str], player: int, count: int) 
#count_from_list(self, items: Iterable[str], player: int) -> int:
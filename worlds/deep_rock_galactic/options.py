from dataclasses import dataclass
from Options import Choice, Range, Toggle, ItemDict, PerGameCommonOptions, StartInventory, Visibility, DeathLink


class Goal(Choice):
    """Set The Current Run Goal [Working Options = haz5_caretaker (default), goldrush, hunter (in dev)]"""
    display_name = "Goal of the Run"
    option_kill_caretaker = 1
    option_goldrush = 2
    option_hunter = 3
    #option_worldtour = 4
    default = 1
    #visibility = Visibility.none

class HazMax(Choice):
    """Determines how high the highest generated hazard level will be for objectives."""
    display_name = "Set Max Hazard for All Objectives"
    option_haz3 = 3
    option_haz4 = 4
    option_haz5 = 5
    default = 5

class GoldRushGoalValue(Range):
    """Set The Current Gold Rush Gold needed (if that's your goal)"""
    display_name = "Goal Gold for Gold Rush"
    range_start = 7500
    range_end   = 20000
    default     = 15000

class HunterTrophyAmount(Range):
    #"""Set The Current Hunter Trophies Needed per enemy (if that's your goal) [NOT YET FINISHED]"""
    display_name = "Trophy Hunter Goal Amount"
    range_start = 1
    range_end   = 20
    default     = 10

class ProgressionDifficulty(Choice):
    """Determines how high the progressive check locks are for each sphere. (Completion by Diff LeafLover=10%, Normal=25%, Hard=33%, Lethal=50%, Karl=75%)"""
    display_name = "Progression Lock Difficulty"
    option_easy = 1
    option_normal = 2
    option_hard = 3
    option_lethal = 4
    option_karl = 5
    default = 2

class StartingStats(Choice):
    """Determine how hard your starting stats are. this also affects your maximum stats reached"""
    display_name = "Starting Stats"
    option_easier_x2 = 1
    option_normal = 2
    option_harder_half = 3
    default = 2

class StartingClasses(Choice):
    """Set you starting class"""
    display_name = "Chosen Starting Class"
    option_all = 0
    option_gunner = 1
    option_driller = 2
    option_scout = 3
    option_engineer = 4
    default = 0

class ErrorCubeChecks(Range):
    """Sets the number of checks to be Error cubes (Defaults to 10)"""
    range_start = 0
    range_end   = 15
    default     = 10

class EnableMinigames(Toggle): 
    """Turns on/off Jetty Boot as a check"""
    display_name = "Enable Minigame Locations"
    default = True

class EnableMachineEvents(Toggle): 
    """Turns on/off Jetty Boot as a check"""
    display_name = "Enable Machine Event Locations"
    default = True

class EnableTraps(Toggle): 
    """Turns on/off Trap Items"""
    display_name = "Enable Traps"
    default = True

class DeathLinkAll(Toggle):
    """Sets whether deathlink will kill all palyers, or just a single dwarf at random (in multiplayer)"""
    display_name = "Should Deathlink Kill All Players?"
    default = True

class LocationsToRemove(Range):
    """Removes locations from the placer. Will make upper power cap lower, can make victory much more difficult."""
    display_name = "Locations to Remove"
    range_start = 0
    range_end   = 150
    default     = 0

class AvgCoinShopPrices(Range):
    """Set the avg coin shop price. This will determine the cost of APCoin Shop Items in game."""
    display_name = "Average Coin Shop Prices"
    range_start = 1
    range_end   = 30
    default     = 5

class CoinShopItems(Range):
    """Set the amount of items to be in the APCoin Shop."""
    display_name = "AP Coin Shop Item Count"
    range_start = 0
    range_end   = 40
    default     = 25

class GoldToCoinConversionRate(Range):
    """Set the value of Gold Gathered to APCoin Conversion Rate. For example setting this to 100 would mean 100x gathered gold gets you 1x APCoin."""
    display_name = "Gold to APCoin Conversion Rate"
    range_start = 5
    range_end   = 500
    default     = 50

class BeerMatToCoinConversionRate(Range):
    """Set the value of Beer Materials to APCoin Conversion Rate. For example setting this to 5 would mean 5x gathered beer materials gets you 1x APCoin."""
    display_name = "Beer Materials to APCoin Conversion Rate"
    range_start = 1
    range_end   = 50
    default     = 2

@dataclass
class DRGOptions(PerGameCommonOptions):
    progression_diff:       ProgressionDifficulty
    starting_stats:         StartingStats
    goal_mode:              Goal
    gold_rush_val:          GoldRushGoalValue
    death_link:             DeathLink
    death_link_all:         DeathLinkAll
    locations_to_remove:    LocationsToRemove
    avail_classes:          StartingClasses
    error_cube_checks:      ErrorCubeChecks
    traps_on:               EnableTraps
    minigames_on:           EnableMinigames
    events_on:              EnableMachineEvents
    coin_shop_prices:       AvgCoinShopPrices
    gold_to_coin_rate:      GoldToCoinConversionRate
    beermat_to_coin_rate:   BeerMatToCoinConversionRate
    shop_item_num:          CoinShopItems
    hunter_trophies:        HunterTrophyAmount
    max_hazard:             HazMax

#set option groups for the web UI
option_groups = [
    OptionGroup(
        "Goal Options",
        [Goal,HazMax,GoldRushGoalValue,HunterTrophyAmount]
    ),
    OptionGroup(
        "Difficulty Options",
        [ProgressionDifficulty,StartingStats,StartingClasses,DeathLink,DeathLinkAll]
    ),
    OptionGroup(
        "Optional Features",
        [ErrorCubeChecks,EnableTraps,EnableMinigames,EnableMachineEvents]
    ),
    OptionGroup(
        "AP Coin Shop Options",
        [AvgCoinShopPrices,CoinShopItems,GoldToCoinConversionRate,BeerMatToCoinConversionRate]
    ),
    OptionGroup(
        "Extra Options",
        [LocationsToRemove]
    ),
]

#Set presets
option_presets = {
    "goldrush standard": {
        "progression_diff": 2,
        "starting_stats": 2,
        "goal_mode": 2,
        "max_hazard": 5,
        "gold_rush_val": 15000,
        "death_link": False,
        "death_link_all": False,
        "locations_to_remove": 0,
        "avail_classes": 0,
        "error_cube_checks": 10,
        "traps_on": True,
        "minigames_on": True,
        "events_on": True,
        "coin_shop_prices": 5,
        "shop_item_num": 25,
        "gold_to_coin_rate": 50,
        "beermat_to_coin_rate": 2,
    },
    "goldrush short": {
        "progression_diff": 1,
        "starting_stats": 1,
        "goal_mode": 2,
        "max_hazard": 5,
        "gold_rush_val": 7500,
        "death_link": False,
        "death_link_all": False,
        "locations_to_remove": 0,
        "avail_classes": 0,
        "error_cube_checks": 0,
        "traps_on": False,
        "minigames_on": False,
        "events_on": False,
        "coin_shop_prices": 2,
        "shop_item_num": 25,
        "gold_to_coin_rate": 25,
        "beermat_to_coin_rate": 2,
    },
    "goldrush long": {
        "progression_diff": 3,
        "starting_stats": 3,
        "goal_mode": 2,
        "max_hazard": 5,
        "gold_rush_val": 20000,
        "death_link": False,
        "death_link_all": False,
        "locations_to_remove": 0,
        "avail_classes": 0,
        "error_cube_checks": 15,
        "traps_on": True,
        "minigames_on": True,
        "events_on": True,
        "coin_shop_prices": 10,
        "shop_item_num": 40,
        "gold_to_coin_rate": 50,
        "beermat_to_coin_rate": 3,
    },
    "haz5 kill caretaker standard": {
        "progression_diff": 2,
        "starting_stats": 2,
        "goal_mode": 1,
        "max_hazard": 5,
        "gold_rush_val": 15000,
        "death_link": False,
        "death_link_all": False,
        "locations_to_remove": 0,
        "avail_classes": 0,
        "error_cube_checks": 10,
        "traps_on": True,
        "minigames_on": True,
        "events_on": True,
        "coin_shop_prices": 5,
        "shop_item_num": 25,
        "gold_to_coin_rate": 50,
        "beermat_to_coin_rate": 2,
    },
    "haz5 kill caretaker easy": {
        "progression_diff": 1,
        "starting_stats": 1,
        "goal_mode": 1,
        "max_hazard": 3,
        "gold_rush_val": 15000,
        "death_link": False,
        "death_link_all": False,
        "locations_to_remove": 0,
        "avail_classes": 0,
        "error_cube_checks": 0,
        "traps_on": False,
        "minigames_on": False,
        "events_on": False,
        "coin_shop_prices": 2,
        "shop_item_num": 25,
        "gold_to_coin_rate": 25,
        "beermat_to_coin_rate": 2,
    },
    "haz5 kill caretaker hard": {
        "progression_diff": 3,
        "starting_stats": 3,
        "goal_mode": 1,
        "max_hazard": 5,
        "gold_rush_val": 15000,
        "death_link": True,
        "death_link_all": True,
        "locations_to_remove": 0,
        "avail_classes": 1,
        "error_cube_checks": 15,
        "traps_on": True,
        "minigames_on": True,
        "events_on": True,
        "coin_shop_prices": 10,
        "shop_item_num": 40,
        "gold_to_coin_rate": 50,
        "beermat_to_coin_rate": 3,
    },
}
from dataclasses import dataclass
from Options import Choice, Range, Toggle, ItemDict, PerGameCommonOptions, StartInventory, Visibility, DeathLink


class Goal(Choice):
    """Set The Current Run Goal [Working Options = haz5_caretaker (default), goldrush]"""
    display_name = "Goal of the Run"
    option_haz5_caretaker = 1
    option_goldrush = 2
    #option_hunter = 3
    #option_worldtour = 4
    default = 1
    #visibility = Visibility.none

class ProgressionDifficulty(Choice):
    """Determines how high the progressive check locks are for each sphere. (Completion by Diff LeafLover=10%, Normal=25%, Hard=33%, Lethal=50%, Karl=75%)"""
    display_name = "Progression Lock Difficulty"
    option_easy = 1
    option_normal = 2
    option_hard = 3
    option_lethal = 4
    option_karl = 5
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
    goal_mode:              Goal
    death_link:             DeathLink
    death_link_all:         DeathLinkAll
    locations_to_remove:    LocationsToRemove
    avail_classes:          StartingClasses
    error_cube_checks:      ErrorCubeChecks
    traps_on:               EnableTraps
    minigames_on:           EnableMinigames
    coin_shop_prices:       AvgCoinShopPrices  
    gold_to_coin_rate:      GoldToCoinConversionRate
    beermat_to_coin_rate:   BeerMatToCoinConversionRate

    
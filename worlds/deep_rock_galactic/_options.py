from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, Visibility


# # class MoneyMultiplier(Range):
    # # """Money Multiplier"""
    # # display_name = "Money Multiplier"
    # # range_start = 1
    # # range_end = 10
    # # default = 1

class MaxHazard(Choice):
    """Max Hazard Level (Not Yet Functional, Defaults to 5)"""
    display_name = "Maximum Hazard Level"
    option_hazard_1 = 1
    option_hazard_2 = 2
    option_hazard_3 = 3
    option_hazard_4 = 4
    option_hazard_5 = 5
    default = 5
    visibility = Visibility.none

#class WarningHazardMin(Choice):
    """Min Hazard Level for Warnings"""
    #display_name = "Minimum Hazard Level for Warnings"
    #option_hazard_1 = 1
    #option_hazard_2 = 2
    #option_hazard_3 = 3
    #option_hazard_4 = 4
    #option_hazard_5 = 5
    #default = 5

class StartingClasses(Choice):
    """Set you starting class (Not Yet Functional, set in starting items instead)"""
    display_name = "Available Starting Classes"
    option_all = 0
    option_gunner = 1
    option_driller = 2
    option_scout = 3
    option_engineer = 4
    default = 0

class ErrorCubeChecks(Range):
    """Sets the number of checks to be Error cubes (Not Yet Functional, Defaults to 10)"""
    range_start = 0
    range_end   = 20
    default     = 10

#class EnableMinigames(Toggle): 
    # display_name = "Enable Minigame Locations"
    # default = False

# class StartingMovementSpeed(Range):
    # """Sets the starting movement speed as a percent of base."""
    # range_start = 0.7
    # range_end   = 2.0
    # default     = 0.7
    # visibility = Visibility.none

# class StartingAmmo(Range):
    # """Sets the starting ammo as a percent of base capacity."""
    # range_start = 0.1
    # range_end   = 1.0
    # default     = 0.25
    # visibility = Visibility.none

# class StartingShield(Range):
    # """Sets the starting shield. Base is 25"""
    # range_start = 0.1
    # range_end   = 1.0
    # default     = 0.25
    # visibility = Visibility.none

# class StartingAmmo(Range):
    # """Sets the starting ammo as a percent of base capacity."""
    # range_start = 0.1
    # range_end   = 1.0
    # default     = 0.25
    # visibility = Visibility.none

class LocationsToRemove(Range):
    """Removes locations from the placer. Will make upper power cap lower, can make victory much more difficult."""
    display_name = "Locations to Remove"
    range_start = 0
    range_end   = 420
    default     = 0

class DeathLink(Toggle): ##Deathlink is enabled in DRG. If you write "Death-Link" into the "APCheckList" text document, and there is a number attached to it, it will send a deathlink. 
    ##e.g. if it said Death-Link:3 before, and you write Death-Link:4 it will send a deathlink to the game. All players will die. 
    """Death Link"""
    ## this is probably bad to implement. more for example reasons than anything else
    display_name = "Death Link Enabled"
    default = False


@dataclass
class DRGOptions(PerGameCommonOptions):
    start_inventory:        StartInventoryPool
    max_hazard:             MaxHazard
    death_link:             DeathLink
    locations_to_remove:    LocationsToRemove
    #min_warning_haz:        WarningHazardMin
    avail_classes:          StartingClasses
    error_cube_checks:      ErrorCubeChecks   
    # starting_movement_speed: StartingMovementSpeed
    # starting_ammo:      StartingAmmo
    
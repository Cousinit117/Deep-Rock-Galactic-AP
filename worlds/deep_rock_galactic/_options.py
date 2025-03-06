from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool


# class MoneyMultiplier(Range):
    # """Money Multiplier"""
    # display_name = "Money Multiplier"
    # range_start = 1
    # range_end = 10
    # default = 1


# class MaxHazard(Choice):
    # """Max Hazard Level"""
    # display_name = "Maximum Hazard Level"
    # option_hazard_1 = 1
    # option_hazard_2 = 2
    # option_hazard_3 = 3
    # option_hazard_4 = 4
    # option_hazard_5 = 5
    # default = 5

# class StartingMovementSpeed(Range):
    # """Sets the starting movement speed as a percent of base."""
    # range_start = 0.7
    # range_end   = 2.0
    # default     = 0.7

# class LocationsToRemove(Range):
    # """Removes locations from the placer. Will make upper power cap lower, can make victory much more difficult."""
    # range_start = 0
    # range_end   = 350
    # default     = 0


class DeathLink(Toggle): #Deathlink is enabled in DRG. If you write "Death-Link" into the "APCheckList" text document, and there is a number attached to it, it will send a deathlink. 
    #e.g. if it said Death-Link:3 before, and you write Death-Link:4 it will send a deathlink to the game. All players will die. 
    """Death Link"""
    # this is probably bad to implement. more for example reasons than anything else
    display_name = "Death Link Enabled"
    default = False


@dataclass
class DRGOptions(PerGameCommonOptions):
    start_inventory:    StartInventoryPool
    # max_hazard:         MaxHazard
    death_link:         DeathLink
    # locations_to_remove:LocationsToRemove   
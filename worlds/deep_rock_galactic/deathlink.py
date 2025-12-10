import random
import os

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
		from .client import DRGContext

def is_file_empty(file_path):
    """
    Checks if a file is empty using os.path.getsize().
    Returns True if the file is empty, False otherwise.
    Raises FileNotFoundError if the file does not exist.
    """
    return os.path.getsize(file_path) == 0

async def handle_receive_deathlink(ctx: 'DRGContext', message: str = "A Dwarf Died in DRG"):
	"""Resolves the effects of a deathlink received from the multiworld based on the options selected by the player"""
	#chosen_effects: List[str] = ctx.slot_data["death_link_effect"]
	#effect = random.choice(chosen_effects)
	with open(ctx.file_deathget, 'w') as f:
    		f.write(f"{message}")

async def handle_check_deathlink(ctx: 'DRGContext'):
	"""Checks if the local player should send out a deathlink to the multiworld as well as if we should respond to any pending deathlinks sent to us """
	# check if we received a death link
	if ctx.received_death_link:
		ctx.received_death_link = False
		await handle_receive_deathlink(ctx, ctx.death_link_message)

     # Check if we should send out a death link
	#result = await ctx.game_interface.get_deathlink()
	result = await ctx.is_file_empty(ctx.file_deathsend)
	if not result:
		messages = [f"Lost their beard to {result}"]

	if ctx.slot is not None:
		player = ctx.player_names[ctx.slot]
		message = random.choice(messages)
		await ctx.send_death(f"{player} {message}")
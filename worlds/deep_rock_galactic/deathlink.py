import asyncio
import os
import random

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
		from .client import DRGContext

async def handle_receive_deathlink(ctx: 'DRGContext', message: str = "Deathlink Received"):
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
	result = ""
	if not os.path.getsize(ctx.file_deathsend) == 0:
		with open(ctx.file_deathsend, 'r') as file:
			result = file.read()
		messages = [f"lost their beard to {result}"]

		if ctx.slot is not None:
			player = ctx.player_names[ctx.slot]
			message = random.choice(messages)
			await ctx.send_death(f"{player} {message}")
			open(ctx.file_deathsend, 'w') #clear deathlink send file

# import ModuleUpdate
# ModuleUpdate.update()
# not sure what this is for...

import asyncio
import json
import os
import requests
import time
import re
from NetUtils import ClientStatus
import Utils
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop

#Testing:
# import colorama
# from asyncio import Task
#

class DRGContext(CommonContext):
    game = "Deep Rock Galactic"
    items_handling = 0b111  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(DRGContext, self).__init__(server_address, password)
        # self.finished_game             = False
        self.server_state_synchronized = False
        self.loc_name_to_id            = None
        self.id_to_loc_name            = None
        self.item_name_to_id           = None
        self.id_to_item_name           = None
        self.new_locations             = set()
        self.file_items                = 'E:\SteamLibrary\steamapps\common\Deep Rock Galactic\FSD\Mods\APChecklist.txt'
        self.file_locations            = 'E:\SteamLibrary\steamapps\common\Deep Rock Galactic\FSD\Mods\APLocationlist.txt'
        self.collected_items           = []
        self.finished_game             = False

#edited 2/24/25
        # try:
            # auto_detect_root_directory = Utils.get_settings()["jakanddaxter_options"]["auto_detect_root_directory"]
            # if auto_detect_root_directory:
                # root_path = find_root_directory(ctx)
            # else:
                # root_path = Utils.get_settings()["jakanddaxter_options"]["root_directory"]
#/edited 2/24/25            
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DRGContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.server_state_synchronized = False
        await super(DRGContext, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.server_state_synchronized = False
        await super(DRGContext, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(DRGContext, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            print('roominfo received by client. Not really sure what this does yet for drg')
            pass

        if cmd in {"Connected"}:
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Deep Rock Galactic"]}]))
            self.locations_checked = set(args["checked_locations"])

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index < len(self.collected_items):
                new_items = args['items'][len(self.collected_items) - start_index:]
            else:
                new_items = args['items']
            self.collected_items += new_items
            # put all the thingies into the output file
            asyncio.create_task(self.give_items(self.collected_items))

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            if "Deep Rock Galactic" in args["data"]["games"]:
                self.data_package_DRG_cache(args)
                self.server_state_synchronized = True
            asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}])) # request new items

    def data_package_DRG_cache(self, args):
        self.loc_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["location_name_to_id"]
        self.id_to_loc_name = {v: k for k, v in self.loc_name_to_id.items()}
        self.item_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["item_name_to_id"]
        self.id_to_item_name = {v: k for k, v in self.item_name_to_id.items()}

    async def check_locations(self):

        if self.file_locations is None:
            print('error, no locations file found,  attempting to create at referenced directory')
            open(self.file_locations, "w")
            return

        with open(self.file_locations, 'r') as f:
            locations = f.readlines()
        locations = {location.replace('\n','') for location in locations}
        
        for location in locations.copy():
            if location == 'Magma Core:Industrial Sabotage:5': continue
            if location[-1].isdigit():
                hazard_lvl = int(location[-1:])
                for i in range(1, hazard_lvl):
                    locations.add(location[:-1]+str(i))
            
        locations = {self.loc_name_to_id[location] for location in locations if location in self.loc_name_to_id} #edited 2/24/25
        self.new_locations |= locations - self.locations_checked

    async def give_items(self, items, timeout=15.0):
        # sleep so we can get the datapackage and not miss any items that were sent to us while we didnt have our item id dicts
        timeout_timestamp = time.time() + timeout
        while self.id_to_item_name is None and time.time() <= timeout_timestamp:
            await asyncio.sleep(0.5)
        if timeout_timestamp > timeout_timestamp:
            print('error in give items. Could not synchronize id_to_item_name before timeout, possibly did not receive datapackage packet.')
            return
        print('RECEIVED ITEM LIST:')
        items = [self.id_to_item_name[item.item] for item in items]
        print(items)
        if self.file_items is None:
            print('error, no items file found, attempting to create at referenced directory')
            open(self.file_items, "w")
        items_counts = {}
        for item in items:
            items_counts[item] = items_counts.get(item, 0) + 1
        output_items = ','.join([f'{key}:{value}' for key, value in items_counts.items()])
        with open(self.file_items, 'w') as f:
            # nuke the txt file and shove it in. Can do so by just opening file with mode='w' (no append)
            f.write(output_items)
        
        if self.finished_game == False and 'Victory' in items:
            await self.send_msgs([{"cmd":"StatusUpdate","status":ClientStatus.CLIENT_GOAL}])
            self.finished_game=True

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class DRGManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago DRG Client"

        self.ui = DRGManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


# def finished_game(ctx):
    # '''returns boolean'''
    # # hacky win condition: is 100%?
    # if len(locations_checked) == len(loc_name_to_id):
        # return True
    # return False


async def DRG_watcher(ctx: DRGContext):
    while not ctx.exit_event.is_set():
        try:
            if ctx.server_state_synchronized:
                ctx.new_locations = set()
                await asyncio.create_task(ctx.check_locations())
                # if finishedGame(ctx) and not ctx.finished_game:
                    # await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    # ctx.finished_game = True
                if ctx.new_locations:
                    message = [{"cmd": 'LocationChecks', "locations": list(ctx.new_locations)}]
                    await ctx.send_msgs(message)
        except Exception as e:
            print(e)
        await asyncio.sleep(5.0)


def launch():
    async def main(args):
        ctx = DRGContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
                DRG_watcher(ctx), name="DRGProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="DRG Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
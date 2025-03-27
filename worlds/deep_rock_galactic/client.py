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
import settings
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop
from ._locations import location_init
from ._items import ALL_ITEMS
import Utils

class DRGContext(CommonContext):
    game = "Deep Rock Galactic"
    items_handling = 0b111  # Indicates you get items sent from other world
    options = Utils.get_options()
    APChecklist="APChecklist.txt"
    APLocationlist="APLocationlist.txt"
    APLocationsChecked="APLocationsChecked.txt"
    APLocationHelper="APLocationHelper.txt"
    #This will not run in source currently if your host.yaml does not contain a working directory
    #It will try to open a file browsers to let you select, and that part will fail if ran from source, at least for me
    try:
        BaseDirectory=settings.get_settings()["deep_rock_galactic_options"]["root_directory"]
    except:
        print("Make sure that your host.yaml has the correct directory.\nCurrently it seems to be invalid.")

    loc_name_to_id = location_init()
    id_to_loc_name = {v: k for k, v in loc_name_to_id.items()}
    item_name_to_id = ALL_ITEMS
    id_to_item_name = {v: k for k, v in item_name_to_id.items()}

    def __init__(self, server_address, password):
        super(DRGContext, self).__init__(server_address, password)

        self.server_state_synchronized = False
        # below are now defined above in self, so, should delete them
        # self.loc_name_to_id            = None
        # self.id_to_loc_name            = None
        # self.item_name_to_id           = None
        # self.id_to_item_name           = None
        self.new_locations             = set()
        self.file_items                = ""# os.path.join(self.BaseDirectory,self.APChecklist)
        self.file_locations            = ""# os.path.join(self.BaseDirectory,self.APLocationlist)
        self.file_aplocations          = ""# os.path.join(self.BaseDirectory,self.APLocationsChecked)
        self.file_locationhelper       = ""
        self.collected_items           = []
        self.finished_game             = False

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
        # print('on_package triggered')
        if cmd in {"Connected"}:
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Deep Rock Galactic"]}]))
            self.locations_checked = set(args["checked_locations"])
            SlotName=(self.slot_info[self.slot].name)#self.slot_info[self.slot].name returns the name of the slot you connected to
            SlotName=SlotName.replace(" ","_")#DRG Needs to have underscores and no spaces
            self.file_items                = os.path.join(self.BaseDirectory,SlotName,self.APChecklist)#Defines names, but they may not exist yet
            self.file_locations            = os.path.join(self.BaseDirectory,SlotName,self.APLocationlist)
            self.file_aplocations          = os.path.join(self.BaseDirectory,SlotName,self.APLocationsChecked)
            self.file_locationhelper       = os.path.join(self.BaseDirectory,SlotName,self.APLocationHelper)
            if not os.path.isdir(os.path.join(self.BaseDirectory,SlotName)):#Does slot directory/save exist? if no, make it and the files
                os.mkdir(os.path.join(self.BaseDirectory,SlotName))
                open(self.file_items, 'w')
                open(self.file_locations, 'w')
                open(self.file_aplocations, 'w')
                with open(self.file_locationhelper, 'w') as f:
                    #Make location helper here
                    all_checked=set(args["checked_locations"])
                    all_missing=set(args["missing_locations"])
                    all_locations=all_checked.union(all_missing)
                    locationhelper=set()
                    for i in all_locations:
                        locationhelper.add(self.id_to_loc_name[i])
                    f.write("\n".join(list(locationhelper)))


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
        #Runs at bottom of package, so that items can in theory be init first
        #This will let unreal see all the checked locations for in-game tracker
        #should this if statement be tabbed one more to the right, to put it in datapackage command?
        if self.file_aplocations != "":
            with open(self.file_aplocations, 'w') as file:
                file.write('')
            with open(self.file_aplocations, 'a') as file:
                for location in self.locations_checked:
                    file.write(self.location_names.lookup_in_game(location)+'\n') #Prints all checked locations by name, after getting them by ID

    #Since these are now defined in self already, do we need to do this again?
    def data_package_DRG_cache(self, args):
        self.loc_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["location_name_to_id"]
        self.id_to_loc_name = {v: k for k, v in self.loc_name_to_id.items()}
        self.item_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["item_name_to_id"]
        self.id_to_item_name = {v: k for k, v in self.item_name_to_id.items()}

    async def check_locations(self):

        if self.file_locations is None:
            print('error, no locations file found')
            return

        with open(self.file_locations, 'r') as f:
            locations = f.readlines()
        locations = {location.replace('\n','') for location in locations}
        #This for loop gives all locations of lower hazard than the mission that was completed
        #This logic works now, but if deep dives (hazard 3.5, 6.5) were added, it would not function correctly
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
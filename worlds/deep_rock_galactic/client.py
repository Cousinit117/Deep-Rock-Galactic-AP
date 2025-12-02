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
from .locations import location_init
from .items import ALL_ITEMS
import Utils
from typing import TypedDict, Optional, NamedTuple
import enum

class HintStatus(enum.IntEnum):
    HINT_UNSPECIFIED = 0  # The receiving player has not specified any status
    HINT_NO_PRIORITY = 10 # The receiving player has specified that the item is unneeded
    HINT_AVOID = 20       # The receiving player has specified that the item is detrimental
    HINT_PRIORITY = 30    # The receiving player has specified that the item is needed
    HINT_FOUND = 40       # The location has been collected. Status cannot be changed once found.

class Hint(NamedTuple):
    receiving_player: int
    finding_player: int
    location: int
    item: int
    found: bool
    entrance: str = ""
    item_flags: int = 0
    status: HintStatus = HintStatus.HINT_UNSPECIFIED

class NetworkPlayer(NamedTuple):
    team: int
    slot: int
    alias: str
    name: str

class JSONMessagePart(TypedDict):
    type: Optional[str]
    text: Optional[str]
    color: Optional[str] # only available if type is a color
    flags: Optional[int] # only available if type is an item_id or item_name
    player: Optional[int] # only available if type is either item or location
    hint_status: Optional[HintStatus] # only available if type is hint_status

class DRGContext(CommonContext):
    game = "Deep Rock Galactic"
    items_handling = 0b111  # Indicates you get items sent from other world
    #slot_data = True
    options = Utils.get_options()
    APChecklist="APChecklist.txt"
    APLocationlist="APLocationlist.txt"
    APLocationsChecked="APLocationsChecked.txt"
    APLocationHelper="APLocationHelper.txt"
    APSettings="APSettings.txt"
    APShop="APShop.txt"
    APHints="APHints.txt"
    APMsgs="APMsgs.txt"
    #This will not run in source currently if your host.yaml does not contain a working directory
    #It will try to open a file browsers to let you select, and that part will fail if ran from source, at least for me
    try:
        BaseDirectory=settings.get_settings()["deep_rock_galactic_options"]["root_directory"]
    except:
        print("Make sure that your host.yaml has the correct directory.\nCurrently it seems to be invalid.")

    #loc_name_to_id = location_init()
    #id_to_loc_name = {v: k for k, v in loc_name_to_id.items()}
    #item_name_to_id = ALL_ITEMS
    #id_to_item_name = {v: k for k, v in item_name_to_id.items()}

    datagames = {}
    hintsList = []

    def __init__(self, server_address, password):
        super(DRGContext, self).__init__(server_address, password)

        self.server_state_synchronized = False
        self.new_locations             = set()
        self.file_items                = ""# os.path.join(self.BaseDirectory,self.APChecklist)
        self.file_locations            = ""# os.path.join(self.BaseDirectory,self.APLocationlist)
        self.file_aplocations          = ""# os.path.join(self.BaseDirectory,self.APLocationsChecked)
        self.file_locationhelper       = ""
        self.file_settings             = ""
        self.collected_items           = []
        self.finished_game             = False
        self.want_slot_data            = True

    def set_location_data(self):
        self.loc_name_to_id = location_init()#int(self.slot_data["error_cube_checks"]),bool(self.slot_data["minigames_on"]))
        self.id_to_loc_name = {v: k for k, v in self.loc_name_to_id.items()}
        self.item_name_to_id = ALL_ITEMS
        self.id_to_item_name = {v: k for k, v in self.item_name_to_id.items()}

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DRGContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(slot_data = True)

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

    def updateHints(self):
        self.send_msgs([{'cmd': 'Get','keys': f'["_read_hints_{self.team}_{self.slot}"]'}])
        self.UpdateHintsTxT()

    async def getShopItems(self):
        await self.send_msgs([{'cmd': 'LocationScouts','keys': f'[]'}])

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            print('roominfo received by client. Not really sure what this does yet for drg')
            pass
        # print('on_package triggered')
        if cmd in {"Connected"}:
            #asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Deep Rock Galactic"]}]))
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage"}]))
            #print(f"{datapackage}")
            #self.updateHints()
            self.locations_checked = set(args["checked_locations"])
            self.slot_data = args["slot_data"]
            self.set_location_data()
            SlotName=(self.slot_info[self.slot].name)#self.slot_info[self.slot].name returns the name of the slot you connected to
            SlotName=SlotName.replace(" ","_")#DRG Needs to have underscores and no spaces
            self.file_items                = os.path.join(self.BaseDirectory,SlotName,self.APChecklist)#Defines names, but they may not exist yet
            self.file_locations            = os.path.join(self.BaseDirectory,SlotName,self.APLocationlist)
            self.file_aplocations          = os.path.join(self.BaseDirectory,SlotName,self.APLocationsChecked)
            self.file_locationhelper       = os.path.join(self.BaseDirectory,SlotName,self.APLocationHelper)
            self.file_settings             = os.path.join(self.BaseDirectory,SlotName,self.APSettings)
            self.file_shop                 = os.path.join(self.BaseDirectory,SlotName,self.APShop)
            #only print these files first time the save is loaded
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
            #prints and save file settings for the mod to read
            with open(self.file_settings, 'w') as f:
                maxWarnHaz = self.slot_data["max_hazard"]
                cubesNeeded = self.slot_data["error_cube_checks"]
                classStart = self.slot_data["avail_classes"]
                trapsOn = self.slot_data["traps_on"]
                deathlinkOn = self.slot_data["death_link"]
                deathlinkAll = self.slot_data["death_link_all"]
                minigameOn = self.slot_data["minigames_on"]
                APCoinCost = self.slot_data["coin_shop_prices"]
                goldToCoin = self.slot_data["gold_to_coin_rate"]
                beerToCoin = self.slot_data["beermat_to_coin_rate"]
                f.write(f"WarnHazMax:{maxWarnHaz},CubesNeeded:{cubesNeeded},StartingClass:{classStart},TrapsEnabled:{trapsOn},DeathLink:{deathlinkOn},DeathAll:{deathlinkAll},MinigamesEnabled:{minigameOn},APCoinCost:{APCoinCost},GoldToCoin:{goldToCoin},BeerToCoin:{beerToCoin}")
            #prints and saves the shop items for the mod to read
            with open(self.file_shop, 'w') as f:
                shopItemDict = self.slot_data["shop_items"]
                for shopKey in shopItemDict:
                    #print(f"{shopKey}={shopItemDict[shopKey]}")
                    sName = shopKey
                    itemDict = shopItemDict[shopKey]
                    playerN = self.slot_info[itemDict["player"]].name
                    f.write(f"{shopKey}|{playerN}={itemDict["item"]}\n")

        #handle getting new items
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index < len(self.collected_items):
                new_items = args['items'][len(self.collected_items) - start_index:]
            else:
                new_items = args['items']
            self.collected_items += new_items
            self.updateHints()
            # put all the thingies into the output file
            asyncio.create_task(self.give_items(self.collected_items))

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            self.datagames = args["data"]["games"]
            #print(f"{self.datagames}")
            self.updateHints()
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

        #used for hints and item messages
        if cmd in {"PrintJSON"}:
            SlotName=(self.slot_info[self.slot].name)#self.slot_info[self.slot].name returns the name of the slot you connected to
            SlotName=SlotName.replace(" ","_")#DRG Needs to have underscores and no spaces
            self.file_msgs = os.path.join(self.BaseDirectory,SlotName,self.APMsgs)   
            if "type" in args: #check that its a data packet
                if args["type"] == "Hint": #check that it's a hint
                    self.updateHints()
                if args["type"] == "ItemSend": #item sending message
                    thisMsg = args["data"]
                    finalMsg = ""
                    if len(thisMsg) == 6: #self find
                        slot = int(thisMsg[0]["text"])
                        player = self.slot_info[slot].name
                        item = self.getItemNameFromGame(int(thisMsg[2]["text"]),slot) #self.id_to_item_name[int(thisMsg[2]["text"])]
                        location = self.getLocNameFromGame(int(thisMsg[4]["text"]),slot) #self.id_to_loc_name[int(thisMsg[4]["text"])]
                        finalMsg = f"{player} found their {item} ({location})"
                    if len(thisMsg) == 8: #other find
                        slot_f = int(thisMsg[0]["text"])
                        slot_r = int(thisMsg[4]["text"])
                        player_f = self.slot_info[slot_f].name
                        player_r = self.slot_info[slot_r].name
                        item = self.getItemNameFromGame(int(thisMsg[2]["text"]),slot_r) #self.id_to_item_name[int(thisMsg[2]["text"])]
                        location = self.getLocNameFromGame(int(thisMsg[6]["text"]),slot_f) #self.id_to_loc_name[int(thisMsg[6]["text"])]
                        finalMsg = f"{player_f} sent {item} to {player_r} ({location})"
                    #print(f"{finalMsg}")
                    if os.path.isdir(os.path.join(self.BaseDirectory,SlotName)):
                        with open(self.file_msgs, 'w') as f:
                            f.write(f"{finalMsg}")

        #for recieving the raw hints info command
        if cmd in {"Retrieved"}:
            if "keys" in args:
                rawMsg = args["keys"]
                hintCmd = f"_read_hints_{self.team}_{self.slot}"
                #print(f"{rawMsg}") #for debugging
                if hintCmd in rawMsg:
                    self.hintsList = rawMsg[hintCmd]
                    self.UpdateHintsTxT()
              
    def UpdateHintsTxT(self):
        SlotName=(self.slot_info[self.slot].name)#self.slot_info[self.slot].name returns the name of the slot you connected to
        SlotName=SlotName.replace(" ","_")#DRG Needs to have underscores and no spaces
        self.file_hints                = os.path.join(self.BaseDirectory,SlotName,self.APHints)
        finalStr = ""
        for h in self.hintsList:
            slot_f = int(h["finding_player"])
            slot_r = int(h["receiving_player"])
            player_f = self.slot_info[slot_f].name
            player_r = self.slot_info[slot_r].name
            location = self.getLocNameFromGame(int(h["location"]),slot_f)
            item = self.getItemNameFromGame(int(h["item"]),slot_r)
            found = h["found"]
            status = h["status"]
            finalStr += f"{player_f},{player_r},{location},{item},{found},{status}\n"
            #print(f"{finalStr}")
            if os.path.isdir(os.path.join(self.BaseDirectory,SlotName)):
                with open(self.file_hints, 'w') as f:
                    f.write(f"{finalStr}")

    #Since these are now defined in self already, do we need to do this again?
    def data_package_DRG_cache(self, args):

        self.loc_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["location_name_to_id"]
        self.id_to_loc_name = {v: k for k, v in self.loc_name_to_id.items()}
        #print(f"{self.id_to_loc_name}")
        self.item_name_to_id = args["data"]["games"]["Deep Rock Galactic"]["item_name_to_id"]
        self.id_to_item_name = {v: k for k, v in self.item_name_to_id.items()}

    def getItemNameFromGame(self, itemid, playerSlot = 0):
        try:
            tempItems = self.datagames[self.slot_info[playerSlot].game]["item_name_to_id"]
            revArr = {v: k for k, v in tempItems.items()}
            return revArr[itemid]
        except Exception as e:
            return f"{self.slot_info[playerSlot].game} Item"

    def getLocNameFromGame(self, locid, playerSlot = 0):
        try:
            tempLocs = self.datagames[self.slot_info[playerSlot].game]["location_name_to_id"]
            revArr = {v: k for k, v in tempLocs.items()}
            return revArr[locid]
        except Exception as e:
            return f"{self.slot_info[playerSlot].game} Location"

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
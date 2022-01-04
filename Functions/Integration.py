"""
Adaptaion of the library "Discord Interactions" made to use the nextcord library instead of dpy
"""

from aiohttp import ClientSession
from nextcord import Client, AutoShardedClient
from nextcord.ext.commands import Bot, AutoShardedBot, BotMissingPermissions
from nextcord.http import Route
from typing import Union, Optional

from nextcord import ClientException

class InvalidChannelID(ClientException):
    """Raised when an invalid channel ID was entered."""
    pass

class InvalidActivityChoice(ClientException):
    """Raised when an invalid activity choice was entered."""
    pass

class InvalidCustomID(ClientException):
    """Raised when an invalid custom application ID was entered."""
    pass

class RangeExceeded(ClientException):
    """Raised when the allowed ranges for max_age and max_uses parameters were exceeded."""
    pass

defaultApplications = { 
    # Credits to RemyK888
    'youtube': '880218394199220334',
    'poker': '755827207812677713',
    'betrayal': '773336526917861400',
    'fishing': '814288819477020702',
    'chess': '832012774040141894',
    
    # Credits to awesomehet2124
    'letter-tile': '879863686565621790',
    'word-snack': '879863976006127627',
    'doodle-crew': '878067389634314250',

    'spellcast': '852509694341283871',
    'awkword': '879863881349087252',
    'checkers': '832013003968348200',
}

class DiscordInteraction:
    def __init__(self, client: Union[Client, Bot, AutoShardedClient, AutoShardedBot], *, debug: Optional[bool] = False):
        if isinstance(client, (Client, AutoShardedClient, Bot, AutoShardedBot)):
            self.client = client
        else:
            raise ValueError("The client/bot object parameter is not valid.")
        
        if isinstance(debug, bool):
            self.debug = debug
        else:
            self.debug = False
            print('\033[93m'+"[WARN] (discord-together) Debug parameter did not receive a bool object. Reverting to Debug = False."+'\033[0m') 
        
    
    async def new(self, voiceChannelID: Union[int,str], option: Union[int,str], *, max_age: Optional[int] = 0, max_uses: Optional[int] = 0):
        # Type checks
        if not isinstance(voiceChannelID, (str,int)):
            raise TypeError(f"'voiceChannelID' argument MUST be of type string or integer, not a \"{type(voiceChannelID).__name__}\" type.")
        if not isinstance(option, (str,int)):
            raise TypeError(f"'option' argument MUST be of type string or integer, not a \"{type(option).__name__}\" type.")
        
        # Max Range checks
        if not 0 <= max_age <= 604800:
            raise RangeExceeded(f'max_age parameter value should be an integer between 0 and 604800')
        if not 0 <= max_uses <= 100:
            raise RangeExceeded(f'max_uses parameter value should be an integer between 0 and 100')

        # Pre Defined Application ID
        if option and (str(option).lower().replace(" ", "") in defaultApplications.keys()):   

            data = {
                'max_age': max_age,
                'max_uses': max_uses,
                'target_application_id': defaultApplications[str(option).lower().replace(" ","")],
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            
            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voiceChannelID}/invites"), json = data
                )
            #Error Handling
            except Exception as e:
                if self.debug:
                    async with ClientSession() as session:  
                        async with session.post(f"https://discord.com/api/v8/channels/{voiceChannelID}/invites",
                                        json=data, 
                                        headers = {
                                            'Authorization': f'Bot {self.client.http.token}',
                                            'Content-Type': 'application/json'
                                        }
                                    ) as resp:
                            result = await resp.json()
                    print('\033[95m'+'\033[1m'+'[DEBUG] (discord-together) Response Output:\n'+'\033[0m'+str(result))

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])  
                elif e.code == 130000:
                    raise ConnectionError("API resource is currently overloaded. Try again a little later.")      
                else:
                    raise ConnectionError(f"[status: {e.status}] (code: {e.code}) : An unknown error occurred while retrieving data from Discord API.")

            if self.debug:
                print('\033[95m'+'\033[1m'+'[DEBUG] (discord-together) Response Output:\n'+'\033[0m'+str(result))
            
            return result['code']



        # User Defined Application ID
        elif option and (str(option).replace(" ", "") not in defaultApplications.keys()) and str(option).replace(" ","").isnumeric():
            
            data = {
                'max_age': max_age,
                'max_uses': max_uses,
                'target_application_id': str(option).replace(" ", ""),
                'target_type': 2,
                'temporary': False,
                'validate': None
            }

            try:
                result = await self.client.http.request(
                    Route("POST", f"/channels/{voiceChannelID}/invites"), json = data
                )
            # Error Handling
            except Exception as e:
                if self.debug:
                    async with ClientSession() as session:  
                        async with session.post(f"https://discord.com/api/v8/channels/{voiceChannelID}/invites",
                                        json=data, 
                                        headers = {
                                            'Authorization': f'Bot {self.client.http.token}',
                                            'Content-Type': 'application/json'
                                        }
                                    ) as resp:
                            result = await resp.json()
                    print('\033[95m'+'\033[1m'+'[DEBUG] (discord-together) Response Output:\n'+'\033[0m'+str(result))

                if e.code == 10003 or "channel_id: snowflake value" in e.text:
                    raise InvalidChannelID("Voice Channel ID is invalid.")
                elif "target_application_id" in e.text:
                    raise InvalidCustomID(str(option).replace(" ", "")+" is an invalid custom application ID.")
                elif e.code == 50013:
                    raise BotMissingPermissions(["CREATE_INSTANT_INVITE"])  
                elif e.code == 130000:
                    raise ConnectionError("API resource is currently overloaded. Try again a little later.")      
                else:
                    raise ConnectionError(f"[status: {e.status}] (code: {e.code}) : An unknown error occurred while retrieving data from Discord API.")

            if self.debug:
                print('\033[95m'+'\033[1m'+'[DEBUG] (discord-together) Response Output:\n'+'\033[0m'+str(result))

            return result['code']
        
        else:
            raise InvalidActivityChoice("Invalid activity option chosen. You may only choose between (\"{}\") or input a custom application ID.".format('", "'.join(defaultApplications.keys())))
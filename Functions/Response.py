import nextcord
from typing import Union

class InvalidArgument(Exception): pass

async def embed(
    type: int, 
    description: str, 
    title: str = None, 
    fields: list[tuple] = None, 
    target: nextcord.Interaction = None
    ) -> Union[nextcord.Embed, nextcord.Message]:
    """
    Send / Create an embed
    
    Params
    ------
    `type` int
        - `1`: success
        - `2`: fail
        - `3`: general
    
    `description` `title` str
        - The description & title of the embed
    
    `fields` list[tuple]
        - A list of fields you want to add 
    
    `target` TextChannel
        - Parse if you want the embed to be sent directly.
    """
    
    embed = nextcord.Embed(description = description)

    if type == 1: embed.color = nextcord.Color.green()
    elif type == 2: embed.color = nextcord.Color.red()
    elif type == 3: embed.color = nextcord.Color.blurple()
    else: raise InvalidArgument("Invalid Embed Type")

    if title: embed.set_author(name = title)
    
    if fields:
        for field in fields: embed.add_field(name = field[0], value = field[1], inline = field[2] if len(field) > 2 else False)
    
    if target: return await target.response.send_message(embed = embed)
    else: return embed
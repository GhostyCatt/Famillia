import nextcord
from nextcord import Interaction
from Functions.Config import getConfig

async def permissionCheck(user: nextcord.Member, interaction: Interaction, min_requirement: str) -> bool:
    data = getConfig()

    # Check everyone perms
    if min_requirement in data['Everyone']: return True

    # Check user id for perms
    elif str(user.id) in data['Users'].keys():
        if min_requirement in data['Users'][str(user.id)]: return True
        else: return False
    
    # Check role id for perms
    elif str(user.top_role.id) in data['Roles'].keys():
        if min_requirement in data['Roles'][str(user.top_role.id)]: return True
        else: return False
        
    # Return False
    else: return False
import nextcord
from nextcord import Interaction
from Functions.Config import getConfig

def permissionCheck(user: nextcord.Member, interaction: Interaction, min_requirement: str) -> bool:
    data = getConfig()

    # Check everyone perms
    if ( min_requirement in data['Everyone'] ) or ( "is_owner" in data['Everyone'] ): 
        print("Everyone can access it ;-;")
        return True

    # Check user id for perms
    elif ( user.id in data['Users'].keys() ):
        if min_requirement in data['Users'][user.id]: return True
        elif "is_owner" in data['Users'][user.id]: return True
    
    # Check role id for perms
    elif ( user.top_role.id in data['Roles'].keys() ):
        if min_requirement in data['Roles'][user.top_role.id]: return True
        elif "is_owner" in data['Roles'][user.top_role.id]: return True
        
    # Return False
    else: return False
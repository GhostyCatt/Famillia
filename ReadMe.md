# Familia

## Setting Up

```Coming Soon```


## Permission Hierarchy

```Note: The permissions associated with the user overwrite the permissions that users top role gives them.```

**Permission Keys**
- `is_owner`: can run all the commands and features
- `can_timeout`: can timeout users
- `can_ban`: can ban members
- `can_kick`: can kick members
- `can_purge`: can purge upto 50 messages from a channel
- `use_song`: use the song command and list songs command
- `can_add-song`: can add songs
- `can_remove-song`: can remove songs


## Running The Bot

Once you have everything set up and configured, you can open the root directory in your command promt and use the commands:

```shell
$ pip install -r Requirements.txt

$ python Main.py
```

This will install all the required libraries and launch the bot for you

```Note: You will need GIT installed for your bot to function, as the bot currently uses a branch of Nextcord for its slash commands.```
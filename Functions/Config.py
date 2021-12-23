import yaml, json

def getConfig():
    with open("Settings/Config.yaml", "r") as raw_config:
        data = yaml.load(raw_config, Loader = yaml.FullLoader)
    return data

def resetConfig():
    with open("Data/DefaultConfig.json", "r") as raw_json:
        data = json.load(raw_json)
    with open("Settings/Config.yaml", "w") as raw_config:
        yaml.dump(data, raw_config)
    return data
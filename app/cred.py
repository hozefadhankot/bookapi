import json
import os
class Cred:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            self.psql = config_data.get("psql")


# Load config from the JSON file
Cred = Cred(os.getcwd()+'/app/config.json')
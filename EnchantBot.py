import random
import json

class EnchantBot:
    def __init__(self):
        self.db = {}
        self.prob = [1.0,1.0,1.0,1.0,0.9,0.8,0.71,0.63,0.55,0.4,0.29,0.22,0.19,0.16,0.13,0.1]
        self.db_filename = "inventorydb.json"

        with open(self.db_filename, 'r') as f:
            self.db = json.load(f)

    def save(self):
    	with open(self.db_filename, 'w') as f:
    		f.write(json.dumps(self.db))

    def enchant(self, user):
        # initializing self.db[user]
        inventory = self.inventory(user)

        lv = inventory['cur']
        if lv == 0:
            inventory['trials'] += 1
        if lv == 15:
            inventory['cur'] = 0
            return ('error', 15)
        result = random.random() < self.prob[int(lv)]

        if result:
            inventory['cur'] += 1
            inventory['best'] = max(inventory['best'], lv + 1)
            return ('success', inventory['cur'])

        if lv > 8:
            inventory['cur'] = 0
            inventory[str(lv)] += 1
            return ('unstable', -1)

        self.save()
        return ('fail', lv)

    def inventory(self, user):
        if user not in self.db:
            self.db[user] = {}
        inventory = self.db[user]
        if 'best' not in inventory:
            inventory['best'] = 0
        if 'trials' not in inventory:
            inventory['trials'] = 0
        if 'cur' not in inventory:
            inventory['cur'] = 0
        for lv in range(9, 15):
            if str(lv) not in inventory:
                inventory[str(lv)] = 0

        return inventory

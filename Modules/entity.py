#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

import json
import random
from Modules.weapon import Weapon


#--------------------------------------------------------------------------------------------------------------
#   Entity
#--------------------------------------------------------------------------------------------------------------

class Entity:
    def __init__(self, max_health):
        self.health = max_health
        self.max_health = max_health
        self.dead = False

    def damage(self, damage):
        self.health -= damage
        if self.health - damage <= 0:
            self.dead = True

#--------------------------------------------------------------------------------------------------------------
#   Enemy
#--------------------------------------------------------------------------------------------------------------

# Enemy data
with open('data/enemies.json', 'r') as file:
    enemy_data = json.load(file)
ENEMIES = {
    'easy_dif':enemy_data['enemies']['easy'],
    'med_dif':enemy_data['enemies']['medium'],
    'hard_dif':enemy_data['enemies']['hard']
}  

# Enemy class
class Enemy(Entity):
    def __init__(self, difficulty=1):
        self.enemy_data = random.choice(ENEMIES[f'{difficulty}_diff'])
        super().__init__(20)

#--------------------------------------------------------------------------------------------------------------
#   Player
#--------------------------------------------------------------------------------------------------------------

class Player(Entity):
    def __init__(self):
        super().__init__(20)
        self.equipped = Weapon('Gregorator', 5)
    
    def equip(self, name, damage):
        self.equipped = Weapon(name, damage)
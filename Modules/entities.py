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
    def __init__(self, max_health:int):
        self.health = max_health
        self.max_health = max_health
        self.dead = False

    def take_damage(self, damage:int):
        "Damages the entity."
        self.health -= damage
        if self.health - damage <= 0:
            self.dead = True

    def roll_hit(self) -> bool:
        "Outputs success/failure of a hit"
        chance = random.random() * 100
        if chance > 20:
            return True
        else:
            return False

    def deal_damage(self) -> int:
        "Outputs damage for the entity to inflict"
        damage = self.max_health/10
        return damage

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
    def __init__(self, difficulty:str='easy'):
        super().__init__(20)
        self.enemy_data = random.choice(ENEMIES[f'{difficulty}_dif'])
        self.name = 'placeholder'

    def deal_damge(self) -> int:
        return super().deal_damge()

#--------------------------------------------------------------------------------------------------------------
#   Player
#--------------------------------------------------------------------------------------------------------------

class Player(Entity):
    def __init__(self):
        super().__init__(20)
        self.equipped = Weapon('Gregorator', 5)
    
    def equip(self, name:str, damage:float):
        "Equips a weapon onto the player."
        self.equipped = Weapon(name, damage)
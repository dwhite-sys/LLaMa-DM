from Modules.entities import Enemy, Player
from Modules.ai import AI
ai = AI()

def start_combat(player:Player, enemy:Enemy=Enemy()):
    while  enemy.health > 0:
        # Player Attack
        if player.health > 0:
            turn(player, enemy)
        # Enemy attack
        if enemy.health > 0:
            turn(enemy, player)

def turn(attacker=object, defender=object):
    if attacker.roll_hit():
        damage_dealt = defender.deal_damage()
        defender.take_damage(damage_dealt)
        if isinstance(attacker, Player):
            situation = f'You attacked {defender.name} for {damage_dealt} HP.'
        else:
            situation = f'{attacker.name} attacked you for {damage_dealt} HP.'
    else:
        if isinstance(attacker, Player):
            situation = f'You missed.'
        else:
            situation = f'{attacker.name} missed.'
    description = ai.describe_turn(situation)
    print(description)


#--------------------------------------------------------------------------------------------------------------
#   Dependencies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-    Outside     -
#------------------

import random
import json
import ollama
import pygame
pygame.init()

#------------------
#-   Constants     -
#------------------
SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 600)
BACKGROUND = pygame.transform.scale((pygame.image.load('Art/dungeon_wall.png')), (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font(None, 48)
#------------------
#-   Entities     -
#------------------
from Modules.entities import Entity, Enemy, Player

#------------------
#- Loading Screen -
#------------------
from Modules.loading import LoadingScreen
loading = LoadingScreen()

#------------------
#-       AI       -
#------------------
from Modules.ai import AI
ai = AI()

#------------------
#-  Simplicities  -
#------------------
from Modules.simplify import wait, clear, show_cursor, hide_cursor

#------------------
#-    Combat      -
#------------------
from Modules.combat import start_combat, turn


#--------------------------------------------------------------------------------------------------------------
#   Decision Trees
#--------------------------------------------------------------------------------------------------------------

opening_decisions = {
    'village':[
                'You approach a village.',                      # Header
                'Will you like to enter the village?'           # Question
            ],
    'door':[
                'You approach a door',                          # Header
                'Would you you like to go through the door?'    # Question
            ],
    'dungeon':[
                'You approach a dungeon entrance',              # Header
                'Step into the dungeon entrance?'               # Question
            ],
}

#--------------------------------------------------------------------------------------------------------------
#   Main Function
#--------------------------------------------------------------------------------------------------------------

# loading.start('Verifying installation')
# ollama.pull('llama3.2')

# loading.stop()

def test_AI():
    for i in range(10):
        clear()
        options = [
           'proceed',
           'turn back',
           'elaborate'
        ]
        situation = random.choice(list(opening_decisions.keys()))
        user_input = ai.ask(opening_decisions[situation][1], options)
    print("Finished testing")

def test_combat(turn_order, player: Player, enemy: Enemy):

    if turn_order == player:
        turn(player, enemy)
        return enemy
    else:
        turn(enemy, player)
        return player

    # button_image = pygame.transform.scale(pygame.image.load('Art/button.png'), (100, 60))
    # button = button_image.get_rect()


def run():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Window")
    clock = pygame.time.Clock()

    running = True

    player = Player()
    enemy = Enemy('easy')
    dm = AI()

    player_health_txt = FONT.render(f"{player.health}", True, (255, 0, 0))
    player_health_txt_rect = player_health_txt.get_rect(center = (200, 25))

    enemy_health_txt = FONT.render(f"{enemy.health}", True, (255, 0, 0))
    enemy_health_txt_rect = enemy_health_txt.get_rect(center = (800, 25))

    count = 0
    turn_order = player

    while running:

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit frame rate

        player_health_txt = FONT.render(f"{player.health}", True, (255, 0, 0))
        player_health_txt_rect = player_health_txt.get_rect(center = (200, 25))

        enemy_health_txt = FONT.render(f"{enemy.health}", True, (255, 0, 0))
        enemy_health_txt_rect = enemy_health_txt.get_rect(center = (800, 25))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            test_combat(screen, keys, player, enemy)
        
        if enemy.health <= 0:
            count += 1
            print(f"\nEnemies defeated: {count}\n")
            enemy = Enemy('easy')
        elif player.health <= 0:
            print(f"You've been defeated.\n")
            player = Player()



        button_rect = pygame.Rect(200, 400, 150, 60)

        # Handle exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Check if click is inside button
                    turn_order =test_combat(turn_order, player, enemy)

        # Draw everything
        
        screen.blit(BACKGROUND, (0, 0))       # Draw background
        screen.blit(player.image, player.rect)  # Draw player
        screen.blit(enemy.image, enemy.rect)    # Draw enemy
        screen.blit(player_health_txt, player_health_txt_rect)  # Draw player health
        screen.blit(enemy_health_txt, enemy_health_txt_rect)    # Draw enemy health
        pygame.draw.rect(screen, (225, 0, 0), button_rect)  # Button rectangle
        text_surface = FONT.render("Attack", True, (100, 100, 100))  # Button label
        text_rect = text_surface.get_rect(center=button_rect.center)  # Center text
        screen.blit(text_surface, text_rect)  # Render text on button

def start_menu():
    """"""

def main():
    run()

if __name__ == '__main__':
    main()
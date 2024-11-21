#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-    Outside     -
#------------------
import random
import json
import ollama

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
from Modules.combat import start_combat


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

loading.start('Verifying installation')
ollama.pull('llama3.2')
loading.stop()

average = 0

def main():
    player = Player()
    start_combat(player)
    # global average
    # for i in range(10):
    #     clear()
    #     options = [
    #        'proceed',
    #        'flee',
    #        'elaborate'
    #     ]
    #     situation = random.choice(list(opening_decisions.keys()))
    #     user_input = ai.ask(opening_decisions[situation][1], options, True)
    # print("Finished testing")

        
main()
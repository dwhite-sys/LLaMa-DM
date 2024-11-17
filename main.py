#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-    Outside     -
#------------------
import random
import json

#------------------
#-   Entities     -
#------------------
import Modules.entity as entity


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
from Modules.simplify import wait
from Modules.simplify import clear
from Modules.simplify import show_cursor
from Modules.simplify import hide_cursor\

#--------------------------------------------------------------------------------------------------------------
#   Decision Trees
#--------------------------------------------------------------------------------------------------------------

opening_decisions = {
    'village':[
                'You approach a village.', 
                'Will you like to enter the village?'
            ],
    'door':[
                'You approach a door', 
                'Would you you like to go through the door?'
            ],
    'dungeon':[
                'You approach a dungeon entrance',
                'Step into the dungeon entrance?'
            ],
}

#--------------------------------------------------------------------------------------------------------------
#   Main Function
#--------------------------------------------------------------------------------------------------------------

def main():
    player = entity.Player()
    while True:
        clear()
        options = [
           'begin'
        ]
        situation = random.choice(list(opening_decisions.keys()))
        
        user_input = ai.ask(opening_decisions[situation][1], options, True)
        print(f'Average: {ai.total_time/ai.tries}')
        wait(1)
        if user_input in options:
            print(f'Success: {user_input}')
        else:
            print(user_input)
        wait(1.5)
main()



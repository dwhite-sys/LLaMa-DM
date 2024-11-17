import random

npcs = {
    'Edward':'Medieval peasant.',
    'Bethany':'Wife of Edward',
    'Susan':'Child of Bethany and Susan'
}

decisions = {
    'village':{
        'opening':{
            'statement':'You approach a village.', 
            'question':'Will you like to enter the village?'},
        'web':{
            'speak':{
                    'statement':'You see a villager.',
                    'question':'Would you like to talk to them?',
                    'choices':{
                        'bethany':{
                            'statement':'You see a bethany.', 
                            'question':'Open mouth?...',
                            'result':'You spek'
                        },
                        'edward':{
                            'statement':'You see a edward.', 
                            'question':'Open mouth?...',
                            'result':'You spek'
                        }
                    }
                }
            }
    },

    'door':{
        'opening':{
            'statement':'You approach a door.', 
            'question':'Would you like to enter?'},
        'web':{
            'table':{
                'statement':'You see a table.',
                'question':'Would you like to check it out?',
                'choices':{
                    'book':{
                        'statement':'You see a book.', 
                        'question':'Would you like to read it.',
                        'result':'You find out it\'s a cook'
                        }
                    },
                    'key':{
                        'statement':'You see a key.', 
                        'question':'Would you like to read it?',
                        'result':'You find out it\'s a cookbook for chinese food.'
                    }
                }
            }
        },
}

#decision_tree = random.choice(list(decisions.keys()))
situation = random.choice(list(decisions.values()))
print(situation['opening']['statement'])
print(situation['opening']['question'])



# print(f'    {situation['web']['table']['statement']}')
# print(f'    {situation['door']['web']['table']['question']}')

web = random.choice(list(situation['web'].values()))
option = random.choice(list(web['choices'].values()))

print(f'    {option['statement']}')
print(f'    {option['question']}')
print(f'        {option['result']}')






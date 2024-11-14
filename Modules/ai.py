#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

from Modules.loading import LoadingScreen
import ollama
import time

from Modules.simplify import wait
from Modules.simplify import clear

from ui import menu

#--------------------------------------------------------------------------------------------------------------
#   Initialization
#--------------------------------------------------------------------------------------------------------------

loading = LoadingScreen()

#--------------------------------------------------------------------------------------------------------------
#   Class
#--------------------------------------------------------------------------------------------------------------

# ---------------------------------
# |      Behavior Glossary        |
# ---------------------------------
# | 1 - Ask the player a question |
# | 2 - Answer a question         |
# | 3 - Generate enemy            |
# | 4 - Intent recognition        |
# ---------------------------------

class AI():
    def __init__(self):
    #  Settings
        self.refresh = 3
        self.votes = 3
        self.basic_choices = {'check inventory'}
        self.version = 'llama3.2:latest'
        self.situation_context = []

    #  Statistics
        self.total_time = 0
        self.refreshes = 0
        self.tries = 0
#  Ask a question and get the intent
    def ask(self, query, options, testing=False):
        loading.start('Generating question')
        prompt = f'Make a forboding version of "{query}" in the absolute shortest way possible in question form. It should be in second person and not be encapsolated in quotation marks. Do not include any additional information in your output.'
        rephrase = ollama.generate(self.version, prompt)['response']
        menu.situation.config(text=rephrase)
        loading.stop()
        menu.text_entered.wait()
        if testing == False:
            return self.intent(input(rephrase + ' '), query, options)
        else:
            loading.start('Generating answer')
            answer = self.answer(rephrase)
            loading.stop()
            print(rephrase)
            print(answer)
            wait(3)
            return self.intent(answer, query, options)

#  The AI will answer a question (For automating intent delay testing)
    def answer(self, question):
        prompt = f'Create a SHORT and CONSISE answer for the following from the point of view of a user: {question}'
        return ollama.generate(self.version, prompt)['response']
    
    def elaborate_enemy(self, enemy_data):
        prompt = f"Create a SHORT description for an enemy described simply as \"{enemy_data['name']}\" in a room described as \"{enemy_data['room']}\" with a more flowery and foreboding atmosphere in just ONE sentence. INCLUDE the TYPE (wolf, golbin, robot, etc) of enemy and NAME them. Do NOT explain your reasoning."
        stream = ollama.generate(self.version, prompt, stream=True)
        clear()
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
            output = output + chunk['response']
            return output

        

#  Retrieve intent from a text.
    def intent(self, text, query, options, context=None, basic_options=False):
        refresh = 0
        start = time.time()
        self.tries += 1
        while refresh < self.refresh:
            refresh += 1
            self.refreshes += 1
            loading.start('Grabbing intent')
        
        #  Assemble the options string
            if basic_options != False:
                basic_options = ['check inventory']
                options += basic_options
            option_string = f", ".join(list(options)) + f", ".join(list(basic_options)) if basic_options else ", ".join(options)

        #  Start grabbing intent votes
            prompt = f'Get user intention from the following text: "{text}" from the following context: "{query}" out of the following options: "{option_string}". Your output must STRICTLY be from the list of options. Explain your reasoning on a new line.'
            compilation = ''
            for i in range(self.votes):
                compilation += f'{ollama.generate(self.version, prompt)['response']},/n'
            loading.stop()

        #  Tally the vote
            loading.start('Analyzing')
            prompt = f"Look at the following and ONLY output the most commonly picked choice, NOT any kind of reasoning, punctuation, or list: [\n{compilation}]."
            outcome = ollama.generate(self.version, prompt)['response']

        #  Stop loading and return the outcome of the vote
            loading.stop()
            if outcome.lower().strip(', ."') in options:
                self.total_time += time.time()-start
                return outcome.lower().strip(', ."')
            print(f'{refresh}/{self.refresh}')
        print("Intent not found.")
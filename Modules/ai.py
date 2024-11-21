#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

from Modules.loading import LoadingScreen
import ollama
import time

from Modules.simplify import wait

#--------------------------------------------------------------------------------------------------------------
#   Initialization
#--------------------------------------------------------------------------------------------------------------

loading = LoadingScreen()

#--------------------------------------------------------------------------------------------------------------
#   Class
#--------------------------------------------------------------------------------------------------------------

block = '----------------------------------------------------------------------------------------------------------------------------------------'
small_block = '-------------------------------------------------------------------------'

class AI():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AI, cls).__new__(cls)
        return cls._instance

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

    with open('data/log.txt', 'w') as file: 
        file.write(block)
#  Ask a question and get the intent
    def ask(self, query:str, options:list, testing=False) -> str:
        "Asks the player a given question and matches the intent to a set of options."
        loading.start('Generating question')
        prompt = f'You\'re a detached narrator. Rephrase "{query}" in a single sentence, keeping it in question form. Don\'t put it in quotes.'
        rephrase = ollama.generate(self.version, prompt)['response']
        loading.stop()
        if testing == False:
            return self.intent(input(rephrase + ' '), query, options)
        else:
            loading.start('Generating answer')
            answer = self.answer(rephrase)
            loading.stop()
            return self.intent(answer, query, options)
    
#  The AI will answer a question
    def answer(self, question:str) -> str:
        "Generates the answer to a question. Designed for automating the ask method."
        prompt = f'Create a simple answer for the following as if you were a user: {question}'
        return ollama.generate(self.version, prompt)['response']
    
    def describe_turn(self, text:str) -> str:
        'Describes a situation based on input.'
        output = text
        return output

    def intent(self, text:str, query:str, options:list, context=None, basic_options=False) -> str:
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
            prompt = f'Get user intention from the following text: "{text}" from the following context: "{query}" out of the following options: "{option_string}". Your output must STRICTLY be from the list of options. After that, explain your reasoning and keep it brief. Ignore hesitation.'
            compilation = ''
            for i in range(self.votes):
                compilation += f'Entry: ({ollama.generate(self.version, prompt)['response']},\n)'
            loading.stop()

        #  Tally the vote
            loading.start('Analyzing')
            prompt = f"Look at the following and ONLY output the most commonly picked choice, NOT any kind of reasoning, punctuation, or list: [\n{compilation}]."
            outcome = ollama.generate(self.version, prompt)['response']

        #  Stop loading and return the outcome of the vote
            loading.stop()
            if outcome.lower().strip(', ."') in options:
                stop = time.time()
                elapsed = stop-start
                self.total_time += elapsed

                with open('data/tracker.txt', 'w') as file:
                        average = self.total_time/self.tries
                        debug = f'Question: {query}\nOptions: {', '.join(options)}\nAnswer: {text}\nResult: {outcome}\nAverage: {average:.2f}\nAttempts:{refresh}\nTotal Tries:{self.tries}'
                        file.write(debug)
                with open('data/log.txt', 'a') as file: 
                    log = f'\nQuestion: {query}\nAnswer: {text}\nResult: {outcome}\nReasoning: [\n{compilation}]\nElapsed: {elapsed}\nAttempts:{refresh}/3\n{block}'
                    file.write(log)

                return outcome.lower().strip(', ."')
            print(f'{refresh}/{self.refresh}')
        print("Intent not found.")


            
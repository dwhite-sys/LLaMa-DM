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
        prompt = f'Make a slightly forboding version of "{query}" in an equally short question. It should be in second person and should not be in quotation marks. Don\'t obscure the original question by being too poetic.'
        rephrase = ollama.generate(self.version, prompt)['response']
        loading.stop()
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
    
#  The AI will answer a question
    def answer(self, question):
        prompt = f'Create a SHORT and CONSISE answer for the following from the point of view of a user: {question}'
        return ollama.generate(self.version, prompt)['response']

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
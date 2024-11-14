import tkinter
import threading

class Menu:
    def __init__(self):
        menu = tkinter.Tk()
        menu.title = "AI DM"

        label = tkinter.Label(menu, text='AI DM')
        label.pack(padx=10, pady=10)

        situation = tkinter.Label(menu, text = "Situation", width=400, relief=tkinter.SOLID, borderwidth=1)
        situation.pack(padx=10, pady=5)

        response = tkinter.Label(menu, text = "Response", width=400, height=35, relief=tkinter.SOLID, borderwidth=1, anchor=tkinter.NW)
        response.pack(padx=10, pady=5)

        player_input = tkinter.Entry(menu, textvariable="Input", width=400, relief=tkinter.SOLID, borderwidth=1)
        player_input.pack(padx=10, pady=5)
        menu.mainloop()

        player_input.bind('<Return>', self.enter_text())
        self.situation = situation
        self.response = response
        self.player_input = player_input
        self.text_entered = threading.Event()

    def enter_text(self):
        self.text_entered.set()
        text = self.player_input.get()
        self.text_entered.clear()
        return text
    
menu = Menu()
        


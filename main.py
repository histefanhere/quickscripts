import tkinter as tk
import subprocess, json

# Handle the parsing of the config file
links = []
with open("scripts.json", "rb") as file:
    data = json.load(file)
    for link in data:
        links.append([
            link['name'],
            link['key'],
            link['cmd'].split()
        ])

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=30, pady=30)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        text = ""
        for name, key, command in links:
            text += f"{key} -- {name}\n"
        self.text_label = tk.Label(self, text=text)
        self.text_label.pack()

        self.QUIT = tk.Button(self, text="QUIT (Or press q to quit)", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)

def parse_key(event):
    if event.char == "q":
        root.destroy()

    for name, key, command in links:
        if event.char == key:
            subprocess.Popen(command)
            root.destroy()

root.bind("<Key>", parse_key)

app.mainloop()


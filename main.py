import tkinter as tk
import subprocess, argparse, os, yaml

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
args = parser.parse_args()

def get_file(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# Gets the name of the script from config.yaml
name = None
with open(get_file('config.yaml'), 'r') as file:
    data = yaml.safe_load(file.read())
    if 'name' not in data:
        print("ERROR: Name is not specified in config.yaml!")
        exit()
    name = data['name']

# Handle the parsing of the config file
links = []
try:
    with open(get_file("scripts.yaml"), "r") as file:
        data = yaml.safe_load(file.read())
        for title, info in data.items():
            key = info['key']
            if isinstance(info['cmd'], str):
                cmd = info['cmd']
            else:
                try:
                    cmd = info['cmd'][name]
                except KeyError:
                    continue
            
            links.append([
                title,
                key,
                cmd.split()
            ])
except FileNotFoundError:
    print("ERROR: The scripts.json file is not found! Please check that it exists and try again.")
    exit()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=30, pady=30)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        text = ""
        for title, key, command in links:
            text += f"{key} -- {title}\n"
        self.text_label = tk.Label(self, text=text)
        self.text_label.pack()

        self.QUIT = tk.Button(self, text="QUIT (Or press q to quit)", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

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


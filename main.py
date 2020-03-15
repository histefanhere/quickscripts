import tkinter as tk
import subprocess, argparse, os, yaml

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
args = parser.parse_args()

class Config():
    def get_file(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def __init__(self):
        self.read_config()

        self.name = self.get_value('name')

    def read_config(self):
        with open(self.get_file('config.yaml'), 'r') as file:
            data = yaml.safe_load(file.read())
            self.data = data

    def get_value(self, value):
        if value not in self.data:
            raise ValueError(f"Value '{value}' is not defined in config.yaml!")
            exit()
        else:
            return self.data[value]

config = Config()
name = config.name

# Handle the parsing of the script file
links = []
try:
    path = config.get_file(config.get_value('scripts'))
    with open(path, "r") as file:
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

bg = '#f0f0f0'
class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, padx=20, pady=20, bg=bg)
        self.createWidgets(root)
        self.pack()

    def createWidgets(self, root):
        i = 0
        for title, key, command in links:
            tk.Label(self, text=key.upper(), font=("helvetica", 18), anchor="e", bg=bg).grid(row=i, column=0, sticky="E", pady=5)
            tk.Label(self, text=title, font=("helvetica", 12), bg=bg).grid(row=i, column=1, sticky="W", padx=5)
            i += 1

        self.QUIT = tk.Button(self, text="QUIT (Or press q to quit)", fg="red",
                                            command=root.destroy)
        self.QUIT.grid(row=i, column=0, columnspan=2)

root = tk.Tk()
app = Application(root)

def parse_key(event):
    if event.char == "q":
        root.destroy()

    for name, key, command in links:
        if event.char == key:
            subprocess.Popen(command)
            root.destroy()

root.bind("<Key>", parse_key)

root.mainloop()


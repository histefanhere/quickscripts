import tkinter as tk
import subprocess, json, argparse, os

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument("--set_name", metavar="NAME", help="Sets the name for the script")
args = parser.parse_args()

# User wants to set the name of the script
if args.set_name:
    # Open file...
    data = {}
    if os.path.exists('data.json'):
        with open('data.json', 'rb') as file:
            data = json.load(file)
    # Edit data...
    data['name'] = args.set_name
    # And save file!
    with open('data.json', 'w+') as file:
        json.dump(data, file)

    print(f"Name has successfully been set to \"{args.set_name}\"! Use this when referencing this machine in your configuration file.")
    exit()


# Handle the parsing of the config file
links = []
try:
    with open("scripts.json", "rb") as file:
        data = json.load(file)
        for link in data:
            links.append([
                link['name'],
                link['key'],
                link['cmd'].split()
            ])
except FileNotFoundError:
    print("ERROR: The scripts.json file is not found! Please check that it exists and try again.")
    exit()
except json.decoder.JSONDecodeError:
    print("ERROR: There has been an error in the JSON syntax of scripts.json! Please check this and try again.")
    exit()
except Exception as e:
    print("ERROR: There has been some sort of error in your scripts.json! Please check the example provided and try again.")
    exit()

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


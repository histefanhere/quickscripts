import tkinter as tk
import subprocess, argparse, os, yaml, time

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument("--check", action="store_true", help="Check if the config files are valid")
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

        with open(self.get_file(self.get_value('scripts')), 'r') as file:
            scripts = yaml.safe_load(file.read())
            self.scripts = {key: value for key, value in scripts.items() if key != "config"}
            
            self.data['config'] = {}
            if 'config' in scripts:
                self.data['config'] = scripts['config']

    def get_config(self, value, default):
        if value not in self.data['config']:
            return default
        else:
            return self.data['config'][value]

    def get_value(self, value):
        if value not in self.data:
            raise ValueError(f"ERROR: Value '{value}' is not defined in config.yaml!")
            exit()
        else:
            return self.data[value]

config = Config()
name = config.name

# Handle the parsing of the script file
links = []
for title, info in config.scripts.items():
    key = info['key']
    if key.lower() == "q":
        raise KeyError(f"ERROR: It is forbidden to use the key 'q' for any quickscript!")
        exit()
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

if args.check:
    print("Check passed, all config files are okay!")
    exit()

bg = '#ffffff'
class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, padx=20, pady=20, bg=bg)
        self.createWidgets(root)
        self.pack()

    def createWidgets(self, root):
        i = 0
        n = 5
        for title, key, command in links:
            tk.Label(self, text=key.upper(), font=("helvetica", 18), anchor="e", bg=bg).grid(row=(i%n), column=(i//n)*2, sticky="E", pady=5)
            tk.Label(self, text=title, font=("helvetica", 12), bg=bg).grid(row=(i%n), column=1+(i//n)*2, sticky="W", padx=5)
            i += 1

        self.quit = tk.StringVar()
        self.quit.set("QUIT (10)")
        self.start_time = time.time()
        # Quit Label and button
        tk.Label(self, text="Q", font=("helvetica", 18), anchor="e", bg=bg, fg="red").grid(row=i, column=0, sticky="E", pady=5)
        tk.Button(self, textvariable=self.quit, fg="red", font=("helvetica", 12), bg=bg,
                                            command=root.destroy).grid(row=i, column=1, sticky="W", padx=5)

        self.quit_timer(root)

    def quit_timer(self, root):
        # 20 and division by 2 so that the timer goes twice as slow - actually reduces stress!
        new_time = round((20 - time.time() + self.start_time)/2)
        if new_time == -1:
            root.destroy()
            exit()
        if f"QUIT ({new_time})" != self.quit.get():
            self.quit.set(f"QUIT ({new_time})")
        root.after(100, lambda: self.quit_timer(root))

root = tk.Tk()
root.title("quickscripts")
app = Application(root)

def parse_key(event):
    if event.char == "q":
        root.destroy()

    for name, key, command in links:
        if event.char == key:
            subprocess.Popen(command)
            root.destroy()

root.bind("<Key>", parse_key)

# WINDOWS & LINUX - forcing focus
root.wm_attributes("-topmost", 1)
root.focus_force()

borderless = config.get_config('borderless', 0)
if borderless == 1:
    # LINUX
    root.attributes('-type', 'dock')
elif borderless == 2: 
    # WINDOWS
    root.overrideredirect(True)

root.mainloop()

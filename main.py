import tkinter as tk
import subprocess, argparse, os, yaml, time

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument("--check", action="store_true", help="Check if the config files are valid")
parser.add_argument("--set", nargs="*", metavar=('option', 'value'), help="Set some options of the script")
args = parser.parse_args()

class Config():
    def get_file(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def __init__(self, arg):
        if arg != None:
            self.set_config(arg)

        self.read_config()

        self.name = self.get_value('name')

    def set_config(self, arg):
        if not os.path.exists('config.yaml'):
            with open(self.get_file('config.yaml'), 'w+') as file:
                file.write('')

        with open(self.get_file('config.yaml'), 'r+') as file:
            data = yaml.safe_load(file.read())
            if data == None:
                data = {}

        values = ["name", "scripts"]

        if len(arg) == 0:
            # User wants to check all values set
            for val in values:
                if val not in data:
                    print(f"{val}: Not set!")
                else:
                    print(f"{val} = {data[val]}")
        elif len(arg) == 1:
            # Wants to check the value of a specific setting
            if arg[0] not in values:
                print(f"{arg[0]} is not a valid value!")
            else:
                print("Please specify the value to be set")
        elif len(arg) >= 2:
            # Wants to set a setting to a value
            if arg[0] not in values:
                print(f"{arg[0]} is not a valid value!")
            else:
                data[arg[0]] = " ".join(arg[1:])

                with open(self.get_file('config.yaml'), 'w+') as file:
                    file.write(yaml.dump(data))
                print("Value `{}` was successfully set to `{}`!".format(arg[0], " ".join(arg[1:])))
        # We don't want to run the code when the user is setting an option
        exit()

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
            if self.name in self.data['config']:
                if value in self.data['config'][self.name]:
                    return self.data['config'][self.name][value]
        else:
            return self.data['config'][value]
        return default

    def get_value(self, value):
        if value not in self.data:
            raise ValueError(f"ERROR: Value '{value}' is not defined in config.yaml!")
            exit()
        else:
            return self.data[value]

config = Config(args.set)
name = config.name

# Handle the parsing of the script file
links = []
for title, info in config.scripts.items():
    str(key) = info['key']
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

    for repl, repl_string in config.get_config('replace', {}).items():
        cmd = cmd.replace(f"${repl}", repl_string)

    if key in [link[1] for link in links]:
        # Key has already been used
        raise KeyError(f"Key {key} has been used more than once!")

    links.append([
        title,
        key,
        cmd.split()
    ])

if args.check:
    print("Check passed, all config files are okay!")
    exit()

if config.get_config("darkmode", 0):
    # Dark mode
    bg = '#282828'
    fg = '#d9d9d9'
else:
    # LIGHT MODE
    bg = '#ffffff'
    fg = '#000000'

class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, padx=20, pady=20, bg=bg)
        self.root = root

        self.createWidgets(root)
        self.grid(row=0, column=0)

    def createWidgets(self, root):
        i = 0
        n = 5
        # Here we generate all the link lables. i = the ith link, and n = the number of links per column to show.
        for title, key, command in links:
            tk.Label(
                self,
                text=key.upper(),
                font=("helvetica", 18),
                anchor="e",
                bg=bg, fg=fg
            ).grid(row=(i%n)+1, column=(i//n)*2, sticky="E", pady=5)
            tk.Label(
                self,
                text=title,
                font=("helvetica", 12),
                bg=bg, fg=fg
            ).grid(row=(i%n)+1, column=1+(i//n)*2, sticky="W", padx=5)
            i += 1

        # This is the variable that stores the quit StringVar
        self.quit = tk.StringVar()
        self.quit.set("QUIT (10)")
        self.start_time = time.time()
        # Quit Label and button
        tk.Label(self,
            text="Q",
            font=("helvetica", 18),
            anchor="e",
            bg=bg, fg="red"
        ).grid(row=min(i+1, n+2), column=0, sticky="E", pady=5)
        tk.Button(self,
            textvariable=self.quit,
            fg="red",
            font=("helvetica", 12),
            bg=bg,
            highlightthickness=1,
            highlightcolor="#ffbbbb",
            highlightbackground="#ffbbbb",
            borderwidth=0,
            command=root.destroy
        ).grid(row=min(i+1, n+2), column=1, sticky="W", padx=5)
        # Call the recursive timer method which will count down
        self.quit_timer()

        self.cat_row = tk.Frame(self, bg=bg)
        self.cat_row.grid(row=0, column=0, columnspan=99, sticky="nsew")

        groups = [
            {"key": '1', "name":"first"},
            {"key": '2', "name":"second"}
        ]

        j = 0
        for group in groups:
            tk.Label(self.cat_row,
                text=group['key'],
                font=("helvetica", 18),
                fg="#909090" if not j else fg,
                bg=bg
            ).grid(row=0, column=2*j, sticky="nse")
            tk.Label(self.cat_row,
                text=group['name'] + " ",
                font=("helvetica", 12),
                fg="#909090" if not j else fg,
                bg=bg
            ).grid(row=0, column=2*j+1, sticky="nsw")
            j += 1

    def quit_timer(self):
        # 20 and division by 2 so that the timer goes twice as slow - actually reduces stress!
        new_time = round((20 - time.time() + self.start_time)/2)
        if new_time == -1:
            self.root.destroy()
            exit()
        if f"QUIT ({new_time})" != self.quit.get():
            self.quit.set(f"QUIT ({new_time})")
        self.root.after(100, self.quit_timer)

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

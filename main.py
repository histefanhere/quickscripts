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

        self.read_files()
        self.name = self.get_value('name')
        self.parse_config()

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

    def read_files(self):
        with open(self.get_file('config.yaml'), 'r') as file:
            data = yaml.safe_load(file.read())
            self.data = data

        with open(self.get_file(self.get_value('scripts')), 'r') as file:
            data = yaml.safe_load(file.read())
            self.groups_raw = {key: value for key, value in data.items() if key != "config"}

            self.data['config'] = {}
            if 'config' in data:
                self.data['config'] = data['config']

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
# TODO: Raise a different error here
            raise ValueError(f"ERROR: Value '{value}' is not defined in config.yaml!")
            exit()
        else:
            return self.data[value]

    def parse_config(self):
        """ Read and parse all the user configuration, groups and links from the scripts.yaml file. """
        self.groups = []
        for groupname, links in self.groups_raw.items():
            grouplinks = []
            for title, info in links.items():
                key = str(info['key'])
                if key.lower() == "q":
                    raise KeyError(f"ERROR: It is forbidden to use the key 'q' for any quickscript!")
                    exit()
                if isinstance(info['cmd'], str):
                    # Same command for all systems
                    cmd = info['cmd']
                else:
                    # See if there's one specific for this machine name
                    try:
                        cmd = info['cmd'][self.name]
                    except KeyError:
                        # There isn't - that's fine, just continue.
                        continue

                for repl, repl_string in self.get_config('replace', {}).items():
                    cmd = cmd.replace(f"${repl}", repl_string)

                if key in [link[1] for link in grouplinks]:
                    # Key has already been used
                    raise KeyError(f"Key {key} has been used more than once!")

                grouplinks.append([
                    title,
                    key,
                    cmd.split()
                ])

            if len(grouplinks) == 0:
                continue

            # Now that we have all the links in the group, we need to finalize the group
            self.groups.append({
                "name": groupname,
                "links": grouplinks
            })

config = Config(args.set)
name = config.name

if args.check:
    print("Check passed, all config files are okay!")
    exit()

if config.get_config("darkmode", 0):
    # Dark mode
    bg = '#282828'
    fg = '#d9d9d9'
    fg_deselect = "#5f5f5f"
else:
    # LIGHT MODE
    bg = '#ffffff'
    fg = '#000000'
    fg_deselect = "#a0a0a0"

class Application(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, padx=20, pady=20, bg=bg)
        self.root = root

        self.labels = []
        # This is the link group that is currently active
        self.active_group = 999
        self.set_active_group(1)

        self.grid(row=0, column=0)


    def set_active_group(self, n):
        if n-1 == self.active_group:
            return
        if n <= len(config.groups):
            self.active_group = n-1
            self.links = config.groups[self.active_group]['links']
            self.createWidgets()

    def createWidgets(self):
        for label in self.labels:
            label.grid_forget()
        self.labels = []
        links = self.links

        i = 0
        n = 5
        # Here we generate all the link lables. i = the ith link, and n = the number of links per column to show.
        for title, key, command in links:
            label1 = tk.Label(
                self,
                text=key.upper(),
                font=("helvetica", 18),
                anchor="e",
                bg=bg, fg=fg
            )
            label1.grid(row=(i%n)+1, column=(i//n)*2, sticky="E", pady=5)
            self.labels.append(label1)
            label2 = tk.Label(
                self,
                text=title,
                font=("helvetica", 12),
                bg=bg, fg=fg
            )
            label2.grid(row=(i%n)+1, column=1+(i//n)*2, sticky="W", padx=5)
            self.labels.append(label2)
            i += 1

        # This is the variable that stores the quit StringVar
        self.quit = tk.StringVar()
        self.quit.set("QUIT (10)")
        self.start_time = time.time()
        # Quit Label and button
        quit_label = tk.Label(self,
            text="Q",
            font=("helvetica", 18),
            anchor="e",
            bg=bg, fg="red"
        )
        quit_label.grid(row=min(i+1, n+2), column=0, sticky="E", pady=5)
        self.labels.append(quit_label)
        quit_button = tk.Button(self,
            textvariable=self.quit,
            fg="red",
            font=("helvetica", 12),
            bg=bg,
            highlightthickness=1,
            highlightcolor="#ffbbbb",
            highlightbackground="#ffbbbb",
            borderwidth=0,
            command=root.destroy
        )
        quit_button.grid(row=min(i+1, n+2), column=1, sticky="W", padx=5)
        self.labels.append(quit_button)
        # Call the recursive timer method which will count down
        self.quit_timer()

        self.cat_row = tk.Frame(self, bg=bg)
        self.cat_row.grid(row=0, column=0, columnspan=99, sticky="nsew")

        j = 0
        for group in config.groups:
            label = tk.Label(self.cat_row,
                text=str(j+1),
                padx=5,
                font=("helvetica", 18),
                fg=fg if j == self.active_group else fg_deselect,
                bg=bg
            )
            label.grid(row=0, column=2*j, sticky="nse")
            self.labels.append(label)
            label = tk.Label(self.cat_row,
                text=group['name'],
                font=("helvetica", 12),
                fg=fg if j == self.active_group else fg_deselect,
                bg=bg
            )
            label.grid(row=0, column=2*j+1, sticky="nsw")
            self.labels.append(label)
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
    char = event.char

    if char == "q":
        root.destroy()

    if char in "123456789":
        app.set_active_group(int(char))
        return

    for name, key, command in app.links:
        if char == key:
            subprocess.Popen(command)
            root.destroy()

root.bind("<Key>", parse_key)

# WINDOWS & LINUX - forcing focus
# root.wm_attributes("-topmost", 1)
# root.focus_force()

borderless = config.get_config('borderless', 0)
if borderless == 1:
    # LINUX
    root.attributes('-type', 'dock')
elif borderless == 2:
    # WINDOWS
    root.overrideredirect(True)

root.mainloop()

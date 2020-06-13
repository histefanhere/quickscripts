import tkinter as tk
import subprocess, argparse, os, yaml, time

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument("--configure", action="store_true", help="Set some options of the script")
args = parser.parse_args()

class Group:
    def __init__(self, name, key, scripts):
        self.name = name
        self.key = key
        self.scripts = scripts

class Script:
    def __init__(self, name, key, command):
        self.name = name
        self.key = key
        self.command = command

class Config():
    def get_file(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)

    def __init__(self):
        if args.configure:
            self.configuration_wizard()

        if not os.path.exists('config.yaml'):
            self.configuration_wizard()

        with open(self.get_file('config.yaml'), 'r') as file:
            data = yaml.safe_load(file.read())
            self.data = data

            self.name, self.scripts_filename = data['name'], data['scripts']
        
        with open(self.get_file(self.scripts_filename), 'r') as file:
            data = yaml.safe_load(file.read())
            groups_raw = {key: value for key, value in data.items() if key != "config"}

            self.options = {}
            if 'config' in data:
                self.options = data['config']

        self.groups = self.parse_groups(groups_raw)

    def configuration_wizard(self):
        if not os.path.exists('config.yaml'):
            with open(self.get_file('config.yaml'), 'w+') as file:
                file.write('scripts: .\scripts.yaml')

        with open(self.get_file('config.yaml'), 'r+') as file:
            # TODO: Slap a try around this
            data = yaml.safe_load(file.read())
            if data == None:
                data = {}

        print("Welcome to the quickscripts configuration wizard!")
        time.sleep(2)
        print("Here you'll be able to set some key values that the script needs to opearte.")
        time.sleep(3)

        print("\nLet's start with an easy one: What's the name of this machine?")

        prompt = "(leave blank for no name): "
        if 'name' in data:
            prompt = f"(leave blank for current value, '{data['name']}'): "
        name = input(prompt)
        if not name == "":
            data['name'] = name

        print(f"Awesome, the name of this machine is now {data['name']}!")
        time.sleep(3)

        print("\nNow you'll need to tell me where I can find the scripts file")
        time.sleep(2)
        scripts = input(f"(leave blank for current value, '{data['scripts']}'): ")
        if not scripts == "":
            data['scripts'] = scripts

        print(f"Thanks, now I know that the scripts file is located at {data['scripts']}!")
        time.sleep(3)

        print("And that's it! Try to run this script without any arguments now, and thank you for using quickscripts! :)")
        with open(self.get_file('config.yaml'), 'w+') as file:
            file.write(yaml.dump(data))

        exit()

    def get_option(self, value, default):
        """Get an option value, if it's available, from the user-defined `config` field in scripts.yaml"""
        if value in self.options:
            return self.options[value]
        else:
            if self.name in self.options:
                if value in self.options[self.name]:
                    return self.options[self.name][value]
        return default

    def parse_groups(self, groups_raw):
        """Parse the groups from the yaml configuration"""
        groups = []
        group_key = 1
        for group_name, scripts in groups_raw.items():
            group = Group(group_name, group_key, [])
            for script_name, script in scripts.items():
                key = str(script['key'])

                if key.lower() == "q":
                    raise KeyError(f"ERROR: It is forbidden to use the key 'q' for any quickscript!")
                    exit()

                if isinstance(script['cmd'], str):
                    # Same command for all systems
                    cmd = script['cmd']
                else:
                    # See if there's one specific for this machine name
                    try:
                        cmd = script['cmd'][self.name]
                    except KeyError:
                        # There isn't - that's fine, just continue.
                        continue

                for replace_keyword, replace_string in self.get_option('replace', {}).items():
                    cmd = cmd.replace(f"${replace_keyword}", replace_string)

                if key in [script.key for script in group.scripts]:
                    # Key has already been used
                    raise KeyError(f"Key {key} has been used more than once in the same script group!")

                group.scripts.append(Script(
                    script_name,
                    key,
                    cmd
                ))

            group_key += 1

            if len(group.scripts) == 0:
                continue

            groups.append(group)

        return groups

class customButton(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self, master, **kwargs)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self['borderwidth'] = 1
        self['padx'] = 0
        # self['background'] = fg_deselect
    
    def on_leave(self, event):
        self['borderwidth'] = 0
        self['padx'] = 1
        # self['background'] = bg

class MainMenu(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, padx=20, pady=20, bg=bg)
        self.root = root

        self.labels = []

        self.active_group = None
        self.set_active_group(1)

        self.grid(row=0, column=0)

    def set_active_group(self, n):
        if n == self.active_group:
            return
        for group in config.groups:
            if group.key == n:
                self.active_group = n
                self.scripts = group.scripts
                self.create_widgets()

    def create_widgets(self):
        for label in self.labels:
            label.grid_forget()
        self.labels = []

        i = 0
        n = 5
        # Here we generate all the link lables. i = the ith link, and n = the number of links per column to show.
        for script in self.scripts:
            script_letter_label = tk.Label(
                self,
                text=script.key.upper(),
                font=("helvetica", 18),
                anchor="e",
                bg=bg, fg=fg
            )
            script_letter_label.grid(row=(i%n)+1, column=(i//n)*2, sticky="E", pady=5)
            self.labels.append(script_letter_label)
            script_name_label = customButton(
                self,
                text=script.name,
                font=("helvetica", 12),
                bg=bg, fg=fg,
                borderwidth=0,
                padx=1,
                command=lambda key_=script.key: parse_key(key=key_)
            )
            script_name_label.grid(row=(i%n)+1, column=1+(i//n)*2, sticky="W", padx=5)
            self.labels.append(script_name_label)
            i += 1

        ### QUIT BUTTON
        self.quit = tk.StringVar()
        self.quit.set("QUIT (10)")
        self.start_time = time.time()
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
            borderwidth=0,
            command=root.destroy
        )
        quit_button.grid(row=min(i+1, n+2), column=1, sticky="W", padx=5)
        self.labels.append(quit_button)
        # Call the recursive timer method which will count down
        self.quit_timer()

        ### GROUPS
        self.group_row = tk.Frame(self, bg=bg)
        self.group_row.grid(row=0, column=0, columnspan=99, sticky="nsew")

        i = 0
        for group in config.groups:
            label = tk.Label(self.group_row,
                text=str(group.key),
                padx=5,
                font=("helvetica", 18),
                fg=fg if group.key == self.active_group else fg_deselect,
                bg=bg
            )
            label.grid(row=0, column=2*i, sticky="nse")
            self.labels.append(label)
            label = customButton(self.group_row,
                text=group.name,
                font=("helvetica", 12),
                fg=fg if group.key == self.active_group else fg_deselect,
                bg=bg,
                borderwidth=0,
                padx=1,
                command=lambda key_=group.key: parse_key(key=str(key_))
            )
            label.grid(row=0, column=2*i+1, sticky="nsw")
            self.labels.append(label)
            i += 1

    def quit_timer(self):
        # 20 and division by 2 so that the timer goes twice as slow - actually reduces stress!
        new_time = round((20 - time.time() + self.start_time)/2)
        if new_time == -1:
            self.root.destroy()
            exit()
        if f"QUIT ({new_time})" != self.quit.get():
            self.quit.set(f"QUIT ({new_time})")
        self.root.after(100, self.quit_timer)

config = Config()

if config.get_option("darkmode", 0):
    # Dark mode
    bg = '#282828'
    fg = '#d9d9d9'
    fg_deselect = "#5f5f5f"
else:
    # LIGHT MODE
    bg = '#ffffff'
    fg = '#000000'
    fg_deselect = "#a0a0a0"

root = tk.Tk()
root.title("quickscripts")
app = MainMenu(root)

def parse_key(event=None, key=None):
    if event is None:
        print(key)
        char = key
    else:
        char = event.char

    if char == "q":
        root.destroy()

    elif char in "123456789":
        app.set_active_group(int(char))

    else:
        for script in app.scripts:
            if char == script.key:
                subprocess.Popen(script.command.split())
                root.destroy()

root.bind("<Key>", parse_key)

# WINDOWS & LINUX - forcing focus
# root.wm_attributes("-topmost", 1)
# root.focus_force()

borderless = config.get_option('borderless', 0)
if borderless == 1:
    # LINUX
    root.attributes('-type', 'dock')
elif borderless == 2:
    # WINDOWS
    root.overrideredirect(True)

root.mainloop()

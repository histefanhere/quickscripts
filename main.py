from dataclasses import dataclass, asdict
import subprocess, argparse, os, yaml, time
import webview

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument("--configure", action="store_true", help="Set some options of the script")
args = parser.parse_args()

valid_keys = "abcdefghijklmnoprstuvwxyz,.<>/?;:'\"[]{}-_=+!@#$%^&*()`~"
invalid_keys = "q"

def error(message):
    raise Exception(message)

@dataclass
class Group:
    name: str
    key: str
    scripts: list

@dataclass
class Script:
    name: str
    key: str
    command: str


class Config():
    def get_file(self, filename):
        return os.path.join(os.path.dirname(__file__), filename)
    
    def load_yaml(self, file):
        try:
            data = yaml.safe_load(file.read())
        except Exception as e:
            file.close()
            error(f"Error in parsing YAML file {file.name}:\n\n" + str(e))
        else:
            return data

    def __init__(self):
        if args.configure:
            self.configuration_wizard()

        if not os.path.exists('config.yaml'):
            self.configuration_wizard()

        with open(self.get_file('config.yaml'), 'r') as file:
            data = self.load_yaml(file)
            self.data = data

            self.name, self.scripts_filename = data['name'], data['scripts']
        
        with open(self.get_file(self.scripts_filename), 'r') as file:
            data = self.load_yaml(file)
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
            data = self.load_yaml(file)
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
            group = Group(group_name, str(group_key), [])
            for script_name, script in scripts.items():
                key = str(script['key'])

                if key.lower() in invalid_keys:
                    error(f"It is forbidden to use the key '{key}' for any quickscript!")

                if key.lower() not in valid_keys:
                    error(f"ERROR: key '{key}' is an invalid quickscript key!")

                if key in [script.key for script in group.scripts]:
                    error(f"Key {key} has been used more than once in the same script group!")

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

                group.scripts.append(Script(
                    script_name,
                    key,
                    cmd
                ))

            group_key += 1

            if len(group.scripts) == 0:
                continue

            groups.append(group)
        
        if len(groups) > 9:
            error("You cannot have more than 9 Script Groups!")

        return groups


class Api:
    def __init__(self):
        self.config = Config()
        
    def get_rows(self):
        return self.config.get_option("rows", 5)

    def get_groups(self):
        return [asdict(x) for x in self.config.groups]

    def fit_window(self, width, height):
        webview.windows[0].resize(width, height)

    def execute(self, command):
        subprocess.Popen(command, shell=True)
        self.close()

    def close(self):
        webview.windows[0].destroy()


if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Quickscripts',
        'assets/index.html',
        js_api=api,
        min_size=(100, 100),
        frameless=True,
        on_top=True,
        x=0,
        y=0,
        transparent=True
    )
    webview.start(debug=False)

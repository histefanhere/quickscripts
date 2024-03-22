from dataclasses import dataclass, asdict
import math
import subprocess, argparse, os, yaml, time
from functools import wraps

import json
from flask import Flask, jsonify, render_template, request
import mergedeep
import webview

parser = argparse.ArgumentParser(description="Quickly Run your favourite scripts and applications.\nFor aditional help, check the README.")
parser.add_argument('--scripts', nargs="+", dest='scripts_filenames', metavar='FILENAME', help="Location of scripts config file(s). Defaults to python script directory.")
parser.add_argument('--id', dest='device_id', help="Device ID for device-specific scripts.")
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
    def __init__(self):
        self.groups = []
        self.config = {}
        self.device_id = args.device_id

        self.scripts_filenames = args.scripts_filenames
        if self.scripts_filenames is None:
            self.scripts_filenames = ['./scripts.yaml']

        data = {}
        for filename in self.scripts_filenames:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), filename)):
                error(f"File {filename} does not exist!")
    
            with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
                try:
                    filedata = yaml.safe_load(file.read())
                except Exception as e:
                    file.close()
                    error(f"Error in parsing YAML file {file.name}:\n\n" + str(e))
            
            mergedeep.merge(data, filedata)            

        groups_raw = data.get('groups', [])
        self.config = data.get('config', {})

        self.parse_groups(groups_raw)

    def get_config(self, option, default):
        """Get an option value, if it's available, from the user-defined `config` field in scripts.yaml"""
        if option in self.config:
            return self.config[option]
        else:
            if self.device_id in self.config:
                if option in self.config[self.device_id]:
                    return self.config[self.device_id][option]
        return default

    def parse_groups(self, groups_raw):
        """Parse the groups from the yaml configuration."""
        group_key = 1

        for group_raw in groups_raw:
            title = group_raw['title']
            if 'key' in group_raw.keys():
                key = str(group_raw['key'])
            else:
                if group_key > 9:
                    error("You cannot have more than 9 un-keyed Groups!")
                key = str(group_key)
                group_key += 1

            group = Group(title, key, [])
            self.groups.append(group)

            for script in group_raw['scripts']:
                name = str(script['name'])
                key = str(script['key'])

                if key.lower() in invalid_keys:
                    error(f"It is forbidden to use the key '{key}' for any quickscript!")

                if key.lower() not in valid_keys:
                    error(f"ERROR: key '{key}' is an invalid quickscript key!")

                if key in [script.key for script in group.scripts]:
                    error(f"Key {key} has been used more than once in the same script group!")

                if isinstance(script['command'], str):
                    # Same command for all systems
                    command = script['command']
                else:
                    # See if there's one specific for this machine name
                    try:
                        command = script['command'][self.device_id]
                    except KeyError:
                        # There isn't - that's fine, just continue.
                        continue                
                    
                for replace_keyword, replace_string in self.get_config('replace', {}).items():
                    command = command.replace(f"${replace_keyword}", replace_string)
                
                group.scripts.append(Script(name, key, command))


class Api:
    def __init__(self):
        self.config = Config()
        
    def get_rows(self):
        return self.config.get_config("rows", 5)

    def get_theme(self):
        return self.config.get_config('theme', 'auto')

    def get_groups(self):
        return [asdict(x) for x in self.config.groups]

    def fit_window(self, width, height):
        webview.windows[0].resize(width, height)

    def execute(self, command):
        subprocess.Popen(command, shell=True)
        self.close()

    def close(self):
        # If no windows exist, annoyingly the program stops. So one always needs to exist (and be hidden),
        # and gets destroyed when a new one is created.
        webview.windows[0].hide()


api = Api()


def create_window():
    webview.create_window(
        'Quickscripts',
        server,
        js_api=api,
        frameless=True,
        on_top=True,
        x=0,
        y=0,
        width=10,
        height=10,
        transparent=True,
        http_port=9191,
    )


assets_dir = os.path.join(os.path.dirname(__file__), 'assets')  # development path
if not os.path.exists(assets_dir):  # frozen executable path
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

server = Flask(__name__, static_folder=assets_dir, template_folder=assets_dir)

@server.route('/')
def landing():
    return render_template('index.html', token=webview.token)

@server.route('/open')
def test():
    create_window()
    webview.windows[0].destroy()
    return "<h1>Showing window</h1>"


if __name__ == '__main__':
    create_window()
    webview.start()

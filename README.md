# quickscripts
Quickly run your favourite applications and commands, from anywhere!

## What?
I started this project from a need to be able to start all my most used programs, scripts, webpages, as quickly as possible but without having to memorize dozens of hotkeys.
The solution to this is to have _one_ hotkey which starts a GUI from which I can further select options for each of my programs. To make it simpler to use and configure, it is not only slightly cross-platform but also very easy to set-up and forget, use same config files across multiple machines, and more!

## Requirements
Tested on both Windows and Linux. Requires Python 3 and the following libraries:
- `argparse`
- `PyYAML`
- `TKinter` (Installation varies on OS and Distro)

**NOTE:** The python script does _not_ handle the hotkey triggering natively (yet). So to enable this, I recommend using `AutoHotKey` for Windows or `xbindkeys` for Linux. The `hotkeys` directory includes some example scripts for these programs. **ASSIGN OTHER HOTKEYS AT YOUR OWN RISK**

## Installation & Setting up
To install this script, simply clone this repository to anywhere on your local machine:
```
git clone https://www.github.com/histefanhere/quickscripts.git
```
Once all the python dependancies have been installed as per the Requirements section, you must create two files:
- `config.yaml`
    This YAML configuration file _must be created in the same directory as the the script,_ and contains the unique "name" of the script/machine as well as the path to your `scripts.yaml` file (This can be an absolute or relative path).
- `scripts.yaml`
    This is the YAML file where all your scripts will be stored. It is recommended to be located in the same path as the script, however this is totally configurable in the `config.yaml` file if you wish for it to be located elsewhere (even the name of the file is changeable if you'd prefer a `.scripts.yaml`, for example)

Examples of _both_ these files can be found in the `examples` folder, so check these before creating your own. In these examples are also explained all the different usecases of the program, so it is highly recommended to read through them.

## Why do I need to provide a `name`?
While desigining the configuration file strucutres, I had the idea in mind that a single `scripts.yaml` file can be used across multiple different machines with different file structures, different program names and even entirely different OS's.
To be able to do this, each machine needs its own unique identifier - the `name` parameter. For examples of this in action, please refer to the `exampels/scripts.yaml` file.

## List of things I'm never going to end up doing
- Use https://github.com/boppreh/keyboard#keyboard.wait so that no external program is needed for hotkeys
- MacOS Support?
- Write good code.

## Actual TODO list of things I need to do
- [ ] Warn user about using the "q" key
- [ ] Have a command line option for testing config and scripts.yaml files
- [ ] Make UI look good
- [ ] Support for cycling through multiple screens/tabs of keys? Categories?
- [ ] Option in config for borderless window mode
- [ ] Set name and scripts path via command line?
- [ ] Dark mode config, automatic timed selection?


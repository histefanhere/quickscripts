# quickscripts
Quickly run your favourite applications and commands, from anywhere!

![Absolutely Awesome Screenshot](screenshot.png)

I started this project from a need to be able to start all my most used programs, scripts, webpages, as quickly as possible but without having to memorize dozens of hotkeys.
The solution to this is to have _one_ hotkey which starts a GUI from which I can further select options for each of my programs. To make it simpler to use and configure, it is not only slightly cross-platform but also very easy to set-up and forget, use same config files across multiple machines, and more!

## Requirements
Tested on both Windows and Linux. Requires Python 3 and the following libraries:
- `argparse`
- `PyYAML`
- `TKinter` (Installation varies on OS and Distro)

The script does not natively handle the hotkey triggering (yet). So to enable this, I recommend using [AutoHotKey](https://www.autohotkey.com/) for Windows or [xbindkeys](https://linux.die.net/man/1/xbindkeys) for Linux. The `hotkeys` directory includes some example scripts for these programs. **ASSIGN OTHER HOTKEYS AT YOUR OWN RISK**

## Installation
To install this script, simply clone this repository to anywhere on your local machine:
```
git clone https://www.github.com/histefanhere/quickscripts.git
cd quickscripts
```

## Configuration
Once all the python dependancies have been installed as per the Requirements section, run the following command and go through the configuration wizard to configure the python script:
```
python main.py --configure
```

Now you must create a `scripts.yaml` file, which is your configuration file where all your quick scripts will be stored. It is recommended to be located in the same path as the script, however this is totally configurable if you wish for it to be located elsewhere via the `--configure` flag.

An example of this file can be found in the `examples` folder, so check this before creating your own. In the examples is also explained all the different usecases of the program, so **it is highly recommended to read through it.**

### Why do I need to provide a `name`?
While desigining the configuration file strucutres, I had the idea in mind that a single `scripts.yaml` file can be used across multiple different machines with different file structures, different program names and even entirely different OS's.
To be able to do this, each machine needs its own unique identifier - the name parameter. For examples of this in action, please refer to the `examples/scripts.yaml` file.

Of course, if you only plan on using quickscripts on a single device then there's no point in specifying the `name` parameter in your scripts config file. Again, check `examples/scripts.yaml`.

### Why don't you make the script itself listen for hotkeys?
Because, no. The user can accomplish this in whatever way they so please, be it via AutoHotKey, xbindkeys, a dedicated macro button or whatever else. Packing it all into the script would make it do everything, but poorly, instead of specialized but well.

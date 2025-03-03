# krangler

Python tool to convert `.json` node pairs into a `tree.lua` file for Path of Building in the Path of Exile Krangled Passives event.

## How to Use

- Install any modern Python (e.g. [Anaconda](https://www.anaconda.com/download) - we only use Pandas and Numpy libraries which should be installed automatically)
- download this repository with `git` or just click `Code > Download ZIP` on github 
- place your node pair `.json` file(s) into `./data` (to generate these, use [krangle-viewer](https://github.com/efunn/krangle-viewer) tool)
- open your terminal of choice (e.g. Powershell) and navigate to the `krangler` folder (e.g. `cd C:/Users/yourname/Downloads/krangler`)
- run python (`ipython`)
- `from krangler import *`
- `replace_all_nodes_wrapper()`
- you will now have a new file `./data/tree_edit.lua`
- download a [portable installation of Path of Building](https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases/download/v2.34.1/PathOfBuildingCommunity-Portable.zip)
- navigate to `[...]/PathOfBuilding-Community/TreeData/3_22` and replace `tree.lua` with your file (rename `tree_edit.lua` to `tree.lua`)
- run Path of Building from the `[...]/PathOfBuilding-Community/` folder and your new krangled tree should appear!

## Features

- includes list of all nodes in `./data/all_nodes_nothingness.json` to null out the ones that haven't been scouted yet
- supports any number of `.json` files from multiple users
- duplicate nodes (same entry from multiple users) will work
- will warn you when running `replace_all_nodes_wrapper()` if there are duplicate nodes that conflict with each other (i.e. one node mapped to different new nodes by different users)

## Limitations

- skill icons are also krangled (sorry!) due to using some older tree data
- using a base `tree.lua` file from the beginning of 3.22 patch
- PoB changed the formatting of `tree.lua` in later releases and I didn't have time to fix my code
- future versions require a rewrite of `krangler.py` to properly parse nodes instead of doing hacky string editing

# Terrain-Generation
<img align="right" width="80" height="80" src="https://github.com/n1n1n1q/Terrain-Generation/blob/main/assets/.readme/logo.png?raw=true">Customizable Minecraft-inspired application that simulates procedural terrain generation using cellular automata in Python.
## Contents
- [Installation](#installation)
- [Discrete math](#discrete-mathematics-principles)
- [Back-end](#back-end)
    - [Project's architecture](#projects-architecture)
    - [Algorithm](#algorithm)
    - [UI](#ui)
- [Generation](#generation)
    - [Seeds mechanic](#seeds)
    - [Cell class](#cell-class)
    - [Global behaivours](#global-behaivours)
    - [Cells types](#cells-types-and-certain-behaviours)
- [Showcase](#showcase)
- [Credits](#developers-and-responsibilities)
- [License](#license)

## Installation
### Install via PyPi
...
### Manual install
**Prerequisites:** Python 3.11  
Clone the repo, cd into the folder, install dependencies and run main file
```
git clone https://github.com/n1n1n1q/Terrain-Generation
cd Terrain-Generation
pip install -r requirements.txt
python src/main.py
```
## Discrete mathematics principles
<img align="right" width = 200 src="https://github.com/n1n1n1q/Terrain-Generation/blob/main/assets/.readme/automata.png?raw=true">Our project's goal is to take a look at the practical usage of discrete mathematics principles, specifically the application of automata theory in procedural generation.  
Cellular automata are commonly used for simulation of different biological, physical, chemical proccessed, but another usage is procedural map or level generation in game development.  

You can see FSM's diagram on the right. State changes with some random chance and certain map conditions (More detailed description at [Cells types and certain behaivours](#cells-types-and-certain-behaviours))

## Back-end
### The architecture of the project
The project is implemented in Python 3.11.  
The external libraries used in the project are: PySide6 *(user interface and generation visualization)*, MatPlotLib *(the color submodule of the library, used for color manipulation)*, NumPy *(for optimizing operations with 2D arrays)* and their dependencies.  
The following modules are implemented:
* *Cells* module, which contains cells' info and behaivours. The module is highly customizable and is developped in such a way that makes implementing new cell types very easy and quick.
* *Grid* module, which is basically the mathematical model for cells interaction. It contains complementary functions that help to manage the intaractions between cells, as well as the main function which updates the state of the grid.
* *UI* module and its submodules, which is project's visualization. As well as the previous modules, it is designed in such a fashion that offers freedom for further interface extension. Consists of three submodules (main window, grid UI, widgets module).
### Algorithm
As it was mentioned in [Discrete math principles](#discrete-mathematics-principles), the cellular automata is the base concept of the project.  
The cells structure is organized accordingle to OOP principles. There is an abstractl cell class and real cells that inherit from it. 
Each real cell has the *infect* method, which is basically how the algorithm works. If the state of current map satisifies certain conditions (number of active cells around the chosen one, their types, whether the cell can grow and so on), the current cell infects its neighbours and they are assigned the same type.
The grid module serves as a cells handler. It sets the map up and updates it. This module includes some additional functional (such as water height distribution).
### UI
The user interface is implemented with Qt6 Framework (in our case, we used PySide6, the official Python module from the Qt for Python project).
The Ui has two main parts: the settings sidebar and the grid - the terrain generation visualization itself. 
  
![UI-on-launch](https://github.com/n1n1n1q/Terrain-Generation/blob/main/assets/.readme/ui.png?raw=true)
#### Sidebar pannel
<img align="right" width="225" src="https://github.com/n1n1n1q/Terrain-Generation/blob/main/assets/.readme/sidepanel.png?raw=true"></img>
The panel contains the following features:
* Basic inforamtion about the current map
* Settings to customize new map  
    * Seed input
    * Size input 
* Visualization control buttons:
    * Generation delay slider for adjusting the speed of the visualization
    * *'Start/Stop'* button for starting and stopping the visualization
    * *'Regenerate'* button for regenerating a random map or a map with the entered seed and size
    * *'Apply textures'* button for randomly distributing textures which can be randomly reapplied again after clicking the button again.  
    * *'Export' button for exporting the map as .png*




#### Grid
<img align="right" width="150" height="150" src="https://github.com/n1n1n1q/Terrain-Generation/blob/main/assets/.readme/generation.gif?raw=true"></img>The grid submodule of the UI module contains the grid widget which handles the visualization updates. It contains widgets that reprsent the current state of the cells, each with a size adjusted based on the number of columns and rows of the map, and a background color depending on the type of the cell and its height attribute.   
## Generation
### Seeds
Seeds are character sequences that can generate certain maps. Their purpose is to provide the possibility to save a certain pattern for later. It holds the infomration about the locations of the inital biome cells (water, desert, plains), as well as further biome subtype disctribution (mountains, swamp, forest, snow). There are no restrictions for the seed entered by the user. If no seed is entered, a random seed will be generated. A randomly generated seed is a sequence of 20 characters from the following "1234567890abcdefghABCDEFGHQWERTYqwerty".  
### Cell class
Cell is an abstraction, which represents a certain section of the map. Each cell is assigned a certain set of attributes, such as its coordinates, age, threshold age (maximum age that a cell can reach), type, the cell's submissive types (biomes that can be 'consumed' by the cell).
### Global behaivours
The generation proccess is split into 5 stages:
1) Filling the initial map with void cells.
2) Random distribution of 'starting' biome cells (water, desert, plains) and their growth. Desert and plains are assigned random height during this stage, which directly influences their color (makes it either darker or lighter than the color of the initial cell).
3) Random distribution of 'secondary' cells (mountain, forest, swamp and snow) and their growth. All of the secondary cells use the same height principle mentioned above.
4) The depth of water distribution which affects the cell color as well. The farther from the shore, the deeper the water, meaning the darker the cell color.
5) *(Optional generation stage)* Texture distribution which can be Regenerated on button click.
### Cells types and certain behaviours
* **Void**. The cells that fill up the inital map before the start of the generation and are not assigned any biome-specific type belong to the type void. Void cells do not have any submissive types meaning void does not 'infect' its neighbouring cells. Void cells are consumable only by water cells.
* **Water**. The only cell type consumable by water cells is void. It is not limited by threshold age so it spreads over the entire map. Water is consumed by the desert and plains biomes and can be randomly assigned a 'wavy' or 'ship' subtype and the corresponding textures will be applied.
* **Desert**. Desert cells can spread over water cells and, with a small chance, can be consumed by plains. Desert is part of the initial biome disctribution stage meaning its one of the first cells to be placed over a map filled with void cells. The following subtypes and texures can be applied to desert cells: 'pyramid', 'cacti' and 'wasteland'. With a certain chance can infect the plains biome cell.
* **Plains**. Plains, similarly to desert cells, can spread over water. Additionaly, plains cells can spread over the desert biome with a rate smaller than on water. Plains, like desert and water, are part of the starting biome cells. Special subtypes of plains include 'grassy' and 'house'. As well as desert, can consume its counterpart.
* **Forest**. Forest cells are part of the secondary biome distribution stage. They can spread over plains at a far smaller rate than the rate at which primary biomes spread over water. Forest cells are assigned the following texture subtypes: 'birch', 'oak' and 'pine'.
* **Mountains**. Mountains are disctributed in the secondary biome distribution stage. The only cell type consumed by the mountain biome is the plains biome. The textures and subtypes applied to the mountains cells are 'peaky' and 'steep'. 
* **Swamp**. Swamp cells spread over plains cells and water cells. The starting swamp cell placed at the start of the secondary biome distribution stage can be located on a plains cell but can also be placed on a water cell only if it has neighbouring cells of the plains cell type. Swamp cells can be randomly assigned a texture.
* **Snowy**. Snow is also distributed in the secondary generation stage and its submissive types are plains, forest and mountains. Like any other biome, snow cells are assigned a random subtype from one of the following: 'mountain' or 'snowy' if the previous subtypes were not assigned to the cell.  

## Showcase
You can see the full showcase below.  

[![Showcase](https://img.youtube.com/vi/AYHXwCpbbag/0.jpg)](https://www.youtube.com/watch?v=AYHXwCpbbag)
## Developers and responsibilities
[Oleh Basystyi](https://github.com/n1n1n1q) - research, cells module, sprites, some parts of UI and grid modules   
[Anna Stasyshyn](https://github.com/annastasyshyn) - research, UI module, report, cells fixes   
[Viktor Pakholok](https://github.com/viktorpakholok) - grid module, some optimization fixes and deployment  
[Olesya Hapyuk](https://github.com/olkaleska) - :(
## License
[MIT License, 2024](LICENSE)

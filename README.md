# Terrain-Generation
Customizable Minecraft-inspired application that simulates procedural terrain generation using cellular automata in Python.
## Contents
- [Installation](#installation)
- [Discrete math](#discrete-mathematics-principles)
- [Back-end](#back-end)
    - [Project's architecture](#projects-architecture)
    - [Algorithm](#algorithm)
    - [UI](#ui)
- [Generation](#terrain-generation)
    - [Seeds mechanic](#seeds)
    - [Cell class](#cell-class)
    - [Global behaivours](#global-behaivours)
    - [Cells types](#cells-types-and-certain-behaviours)
- [Showcase](#showcase)
- [Credits](#credits)

## Installation
### Install via Docker hub
...
### Manual install
#### via Docker
**Prerequisites:** Docker 26.1
Clone the repo, cd into the folder, run & build the image
```
docker build -t terrain-generation .
docker run terrain-generation
```
#### via Python
**Prerequisites:** Python 3.11  
Clone the repo, cd into the folder, install dependencies and run main file
```
git clone ...
cd ...
pip install -r requirements.txt
python src/main.py
```
## Discrete mathematics principles
Our project is very closely connected to discrete maths.
(cellular automata, automata theory)
## Back-end
### Project's architecture
The project is implemented in Python 3.11. Highly recommended to use docker to run it.  
These external libraries are used: PySide6 *(everything UI related)*, MatPlotLib *(color submodule, for color manipulation)*, NumPy (for better 2D arrays) and their dependencies.  
The following modules are implemented:
* *Cells* module, which contains cells' info and behaivours
* *Grid* module, which is basically the mathematical model for cells interaction
* *UI* module and its submodules, which is project's visualization
### Algorithm
(cellular automata, abstcract infect, grid)
### UI
(few screenshots + tell about ui in general)
## Generation
### Seeds
Seeds are codes that generate certain maps. They are made, so if you liked the certain pattern, you can write it down and use it later. There are no certain restrictions for seeds entered by user, so you can type whatever you want. When generating a seed, it creates a random sequence of symbols from "1234567890abcdefghABCDEFGHQWERTYqwerty" with length 20.
### Cell class
Cell is an abstraction, which represents certain part of the map.
### Global behaivours
(destination points & thresholds)
### Cells types and certain behaviours
* Void
* Water
* Desert
* Plains
* Forest
* Snowy

## Showcase
insert_youtube_link_and_some_filler_text
## Developers and responsibilities
[Oleh Basystyi](https://github.com/n1n1n1q)  
[Anna Stasyshyn](https://github.com/annastasyshyn)  
[Viktor Pakholok](https://github.com/viktorpakholok)  
[Olesya Hapyuk](https://github.com/olkaleska)
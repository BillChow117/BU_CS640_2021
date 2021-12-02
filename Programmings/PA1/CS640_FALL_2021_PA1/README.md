# CS640_FALL_2021_PA
A programming assignement for CS640 Fall 2021.

You will implement an intelligent agent for one of my pet project [SnakeClassic](https://mahir1010.github.io/SnakeClassic/).

Your grades for this assignment will depend on

1\. How well your AI performs

2\. Your report where you will briefly analyze the game environment and describe your approach.

Please install and configure SDL2 and SDL2\_Net libraries for your OS. Make sure you can compile [SnakeClassic](https://mahir1010.github.io/SnakeClassic/). You do not need an Nvidia gpu or Cuda installed for this assignment.

You do not need the Snake-AI repository for this assignment.

You can use `compile.sh 2` to add network controller support.

For the people using windows, I have cross-compiled a build that you can download from [here](https://drive.google.com/drive/folders/1W9FAYjhWH2o-oAkCzGrbc4VOz57eeSls?usp=sharing).

# Environment setup
Arch Distros:  
`sudo pacman -Syy sdl2 sdl2_net`

Debian Distros:

`sudo apt-get install libsdl2-dev libsdl2-net-dev`

MacOS:

Open `compile.sh`, search and replace `gcc` with `clang`

Setup [https://brew.sh/](https://brew.sh/)

`brew install sdl2_net`

`brew install sdl2`

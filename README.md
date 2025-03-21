# Project Penney

This repository holds all files needed to run Monte Carlo-style simulations to automate Penney's Game.

## Overview 

Penney's Game is a card game involving two players selecting sequences and attempting to match their sequences to the order of cards in the deck to acheive either the most "tricks" or the most "cards". 

[Wikipedia Game Overview](https://en.wikipedia.org/wiki/Penney%27s_game) 


## Features
* Creates randomly generated sequences of given size 
* Efficiently simulates multiple rounds of Penney's game with reshuffled decks of given size
* Computes cumulative frequencies of both players' wins for different sequence combinations
* Automatically visualizes results with heatmap 

### Files included:

* `main.py`: start here! code creating logs and running the simulations by calling augmentation function
* `generate.py`: datagen functions for decks and combinations of player sequences  
* `score.py`: functions for processing and scoring individual games and larger simulations
* `visualize.py`: function creating and storing heatmaps for both players winner frequencies
* `game.py`: additional functions and variables stored within "Game" object across other modules
* `helpers.py`: additional functions and the augmentation function to execute the simulation and create visualizations

## Quick Start

Open `main.py` and augment the defined parameters at the top. These get passed into the function `simulate_and_visualize()`, which is defined in `helpers.py`. This function will do everything except (generating, scoring, visualizing) for creating logs.

## Dependencies 

This repository uses numpy, pandas, matplotlib, seaborn, datetime, sys, and os.

## Author:

Vandana Kalithkar

Project Link: https://github.com/vkalithkar/ProjectPenney-UV.git
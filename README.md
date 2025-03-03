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

* `main.py`: start here! code running the simulations, calling generate, score, and visualize functions
* `generate.py`: datagen functions for decks and combinations of player sequences  
* `score.py`: functions for processing and scoring individual games and larger simulations
* `visualize.py`: function creating and storing heatmaps for both players winner frequencies
* `game.py`: additional functions and variables stored within "Game" object across other modules

## Dependencies 

This repository uses numpy, pandas, matplotlib, and seaborn.

## Author:

Vandana Kalithkar

Project Link: https://github.com/vkalithkar/ProjectPenney-UV.git
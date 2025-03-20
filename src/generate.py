import numpy as np
import itertools
import os

def create_game_combos(seq_len: int=3) -> list:
    '''
    Use to initialize all possible Penney's games scenarios where sequences are a given length, 
    excluding matchups between 2 equal sequence choices.

    Arguments:
        seq_len (int): The number of elements per sequence that players select
    
    Output:
        combinations (list): 3D list of (2^seq_len)^2-(2^seq_len) tuples of length 2, 
                             each tuple length seq_len 
    '''

    # use itertools module to match up all possible player sequences of seq_len with one another
    p1 = list(itertools.product([0,1], repeat=seq_len))
    p2 = list(itertools.product([0,1], repeat=seq_len))
    combinations = [(x, y) for x in p1 for y in p2 if x!=y]

    return(combinations)

# Function adapted from student Yueran Shi from Piazza
def _get_init_deck(half_deck_size: int) -> np.ndarray:
    """
    Generate an initial deck with equal 0s and 1s.
    
    Arguments:
        half_deck_size (int): half the size of each unshuffled shuffled deck, 
                              representing the number of 0s and 1s

    Output:
        decks (np.ndarray): 2D array of shape (n_decks, half_num_cards), each row is a shuffled deck.
        seeds (np.ndarray): 1D array of seeds used for shuffling.
    """
    return np.array([0] * half_deck_size + [1] * half_deck_size)

# Function adapted from student Yueran Shi from Piazza
def get_n_decks(n_decks: int, 
                half_num_cards: int
                ) -> tuple[np.ndarray, np.ndarray]:
    """
    Efficiently generate `n_decks` shuffled decks using NumPy.

    Arguments:
        n_decks (int): number of decks to generate
        half_num_cards (int): half the size of each to-be shuffled deck, 
                              representing the number of 0s and 1s
    
    Output:
        decks (np.ndarray): 2D array of shape (n_decks, half_num_cards), each row is a shuffled deck.
        seeds (np.ndarray): 1D array of seeds used for shuffling.
    """
    init_deck = _get_init_deck(half_num_cards)  # Base deck
    decks = np.tile(init_deck, (n_decks, 1))  # Create a 2D array of identical decks
    seeds = np.arange(n_decks)  # Use seed values from 0 to n_decks-1
    
    for i, seed in enumerate(seeds):
        np.random.seed(seed)
        np.random.shuffle(decks[i])  # Shuffle each row with a different seed
    
    # output as .csv in data folder (create if doesn't already exist)
    fig_dir = "data/"  
    os.makedirs(fig_dir, exist_ok=True)
    np.savetxt(os.path.join(fig_dir, "decks_output.csv"), decks, delimiter=",", fmt="%d")  
    
    return decks, seeds
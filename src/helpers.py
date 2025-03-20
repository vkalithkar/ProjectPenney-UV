import pandas as pd

from generate import create_game_combos, get_n_decks
from score import run_full_sim_and_score
from visualize import visualize_all_games_output

def split_simulation_output(all_games_output: pd.DataFrame) -> pd.DataFrame:
    '''
    Function that takes the raw dataframe from a fully-run simulation and transforms via pivoting
    into the shape of a heatmaps while switching numerical labels (0 and 1) into strings to represent
    black and red cards (B and R)

    Arguments:
        all_games_output (pd.DataFrame): the raw data from a full simulation from one player's 
                                         perspective containing columns for player one's sequences, 
                                         player two's sequences, the sequence combination's frequency 
                                         of player one's wins, and the sequence combination's 
                                         frequency of player two's wins
    
    Output: 
        all_games_output_one (pd.DataFrame): the pivoted data from a full simulation from player one's 
                                             perspective from which to directly create a heatmap, 
                                             the axes of which are the players' sequences (R/B),
                                             and data being frequency of that player's wins
        all_games_output_two (pd.DataFrame): the pivoted data from a full simulation from player two's 
                                             perspective from which to directly create a heatmap, 
                                             the axes of which are the players' sequences (R/B),
                                             and data being frequency of that player's wins
    '''
    # pivot the all_games_output into the shape of heatmaps, displaying 
    # the sequence combinations along with Player 1's win frequency as the main data                              
    all_games_output_one = all_games_output.pivot(index = 'p1 combo', 
                                                  columns = 'p2 combo', 
                                                  values = "p1 winner freq")

    # switch 1s to red (R) and 0s to black (B)
    all_games_output_one.index = all_games_output_one.index.map(lambda x: x.replace('0', 'B').replace('1', 'R'))
    all_games_output_one.columns = all_games_output_one.columns.map(lambda x: x.replace('0', 'B').replace('1', 'R'))

    # pivot the all_games_output into the shape of heatmaps, displaying 
    # the sequence combinations along with Player 2's win frequency as the main data                              
    all_games_output_two = all_games_output.pivot(index = 'p1 combo', 
                                                  columns = 'p2 combo', 
                                                  values = "p2 winner freq")

    # switch 1s to red (R) and 0s to black (B)
    all_games_output_two.index = all_games_output_two.index.map(lambda x: x.replace('0', 'B').replace('1', 'R'))
    all_games_output_two.columns = all_games_output_two.columns.map(lambda x: x.replace('0', 'B').replace('1', 'R'))
    
    return all_games_output_one, all_games_output_two

def simulate_and_visualize(current_time: str,
                           seq_len: int = 3, 
                           deck_size: int = 52, 
                           num_decks: int = 1000, 
                           scoring: str = "TRICKS") -> None:
    '''
    Augmentation function for user to modify and run the Penney's Game simulation, generating all 
    results and visualizations

    Arguments:
        current_time (str): date and time of this run to create distinct filenames for heatmaps
        seq_len (int): the number of elements in each player's chosen sequence
        deck_size (int): the number of cards in each deck
        num_decks (int): the desired number of Monte Carlo simulations to execute this simulation
        scoring (str): the desired method to score the players (see scoring methods)
    '''
    # create all of the possible sequence combinations match-ups of length seq_len between the two players
    # store in a list of tuples
    all_combos = create_game_combos(seq_len = seq_len) 

    # create a num_decks amount of randomly generated deck shuffles of deck_size number of cards
    # store in a list of lists
    master_seq_list, seeds = get_n_decks(n_decks = num_decks, half_num_cards = int(deck_size/2))

    print(f"Date and time of this run: {current_time}")

    # run the simulation with all decks and all possible shuffles and score it 
    all_games_output = run_full_sim_and_score(master_seq_list = master_seq_list, 
                                            deck_size = deck_size, 
                                            seq_len = seq_len,  
                                            num_decks=num_decks, 
                                            all_combos=all_combos, 
                                            scoring=scoring)

    all_games_output_one, all_games_output_two = split_simulation_output(all_games_output)
    print("\nVisualizing...")

    # visualize the two heatmaps, once from Player 1's perspective and again from Player 2's perspective
    visualize_all_games_output(all_games_output = all_games_output_one, 
                            current_time = current_time,
                            title = f"P1 Win Rate Over {num_decks} {deck_size}-Length Decks Scored by {scoring}, Sequence Length of {seq_len}")
    visualize_all_games_output(all_games_output = all_games_output_two,
                            current_time = current_time,
                            title = f"P2 Win Rate Over {num_decks} {deck_size}-Length Decks Scored by {scoring}, Sequence Length of {seq_len}")
    print("Done!")


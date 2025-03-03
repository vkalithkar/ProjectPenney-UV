from game import Game
import random
import pandas as pd

def _score_sim_by_tricks(win_stats: dict) -> int:
    '''
    Compare the entry in the win_stats dict to see which player won more tricks 
    (number of sequences) in this game
    
    Arguments:
        win_stats (dict): the dictionary from a processed simulation containing 
                          a list of each player's number of tricks, card counts 
                          for each player, and the number of extra cards from this game

    Output: 
        Integer representing the winner's player number based on who collected more tricks
            (return 1 for player one, 2 for player two, or 0 for instances of a tie)
    '''

    if(win_stats["tricks"][0]>win_stats["tricks"][1]):
        return(1)
    elif(win_stats["tricks"][0]<win_stats["tricks"][1]):
        return(2)
    else:
        return 0 # tie situation

def _score_sim_by_cards(win_stats: dict) -> int:
    '''
    Compare the entry in the win_stats dict to see which player won more cards 
    (total number of deck cards) in this game

    Arguments:
        win_stats (dict): the dictionary from a processed simulation containing 
                          a list of each player's number of tricks, card counts 
                          for each player, and the number of extra cards from this game
    
    Output: 
        Integer representing the winner's player number based on who collected more cards
            (return 1 for player one, 2 for player two, or 0 for instances of a tie)
    '''
    if(win_stats['p1_cards'][0]>win_stats["p2_cards"][0]):
        return(1)
    elif(win_stats['p1_cards'][0]<win_stats["p2_cards"][0]):
        return(2)
    else:
        return 0 # tie situation
    
def run_full_sim_and_score(master_seq_list: list, 
                           deck_size: int, 
                           seq_len: int, 
                           num_decks: int, 
                           all_combos: list, 
                           scoring: str = "TRICKS"
                           ) -> pd.DataFrame:
    '''
    Processes the entire simulation with the desired number of deck shuffles to cumulatively 
    calculate the frequency of both players winning

    Arguments:
        master_seq_list (list): all shuffled decks for the simulation to process against
        deck_size (int): the number of cards in each deck
        seq_len (int): the number of elements in each player's chosen sequence 
        num_decks (int): the desired number of Monte Carlo simulations to execute this simulation
        all_combos (list): all possible ways for players to match sequences 
                           while playing the game (pregenerated)
        scoring (str): the desired method to score the players (see scoring methods)
           
    Output:
        all_games_output (pd.DataFrame): the raw data from a full simulation from one player's 
                                         perspective containing columns for player one's sequences, 
                                         player two's sequences, the sequence combination's frequency 
                                         of player one's wins, and the sequence combination's 
                                         frequency of player two's wins

    '''
    # first, account for Invalid Scoring Method error
    if(scoring != "TRICKS" and scoring != "CARDS"):
        raise Exception("Invalid Scoring Method")

    # initialize all data storage objects to track of statistics for all decks and combinations
    all_games_output = pd.DataFrame(columns = ["p1 combo", "p2 combo", 
                                               "p1 winner freq", "p2 winner freq"])
    p1_seqs = []
    p2_seqs = []

    freq_wins_one = [0] * len(all_combos)
    winner_ones = [0] * len(all_combos)
    freq_wins_two = [0] * len(all_combos)
    winner_twos = [0] * len(all_combos)

    # iterate through all the deck shuffles generated
    for current_deck_idx in range(num_decks):
        master_seq = master_seq_list[current_deck_idx].tolist()
        winners = []
        count = 0

        # iterate through all combinations of player sequences for the current deck
        for this_combo in all_combos:
            count+=1

            print(f"\nshuffle {current_deck_idx + 1}")
            print(f'combo {count}')

            if(current_deck_idx == 0):
                p1_seqs.append(''.join(str(e) for e in this_combo[0]))
                p2_seqs.append(''.join(str(e) for e in this_combo[1]))

            # instantiate Game object with current deck and current player sequence combination 
            g = Game(two_player_seqs = this_combo, 
                     master_seq = master_seq, 
                     deck_size = deck_size, 
                     seq_len = seq_len)
            
            # play this Game
            win_stats = g.play_this_game_deck()

            # score this Game, Exception for Invalid Scoring Method already accounted for
            if (scoring == "TRICKS"):
                winners.append(_score_sim_by_tricks(win_stats))
            elif (scoring == "CARDS"):
                winners.append(_score_sim_by_cards(win_stats))

        print(f'Winners for this deck over all shuffles: {winners}')

        # calculate cumulative wins for each players so far across all games
        for index, item in enumerate(winners):
            winner_ones[index] += 1 if (item==1) else 0
        print(f"\nPlayer one's cumulative wins in this simulation so far: {winner_ones}")

        for index, item in enumerate(winners):
            winner_twos[index] += 1 if (item==2) else 0
        print(f"Player two's cumulative wins in this simulation so far: {winner_twos}")

        # calculate frequency of wins for each players so far across all games
        freq_wins_one=[current_deck_idx/num_decks for current_deck_idx in winner_ones]
        freq_wins_two=[current_deck_idx/num_decks for current_deck_idx in winner_twos]
    print('\n-----------------------Simulation concluded, all card decks have been run with all shuffles-----------------------')
    print(f"\nFreq wins player 1: {freq_wins_one}")
    print(f"Freq wins player 2: {freq_wins_two}")

    # save and store all the winning frequency and combination data to display after all Games concluded 
    all_games_output["p1 combo"]=p1_seqs
    all_games_output["p2 combo"]=p2_seqs
    all_games_output["p1 winner freq"]=freq_wins_one
    all_games_output["p2 winner freq"]=freq_wins_two

    return all_games_output
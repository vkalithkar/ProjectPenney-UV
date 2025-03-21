import queue

class Game:
    '''
    A Game object contains each individual instance of a single deck shuffle game, 
    meaning the chosen sequences of the two players and other general information 
    like the size of deck and length of sequences.
    '''
    def __init__(self,
                 two_player_seqs: list,
                 master_seq: list,
                 deck_size: int = 52,
                 seq_len: int = 3
                 ) -> None:
        self.two_player_seqs = two_player_seqs
        self.deck_size = deck_size
        self.master_seq = master_seq
        self.seq_len = seq_len
        return
    
    def __repr__(self) -> str:
        return f"Player's Sequences: {self.two_player_seqs} for a {self.seq_len} card-length sequence with a {self.deck_size}-card deck"
    
    def play_this_game_deck(self) -> dict:
        '''
        Assess the winner of this game given the players' chosen sequences and 
        the current shuffle by breaking down the deck sequence

        Output:
            win_stats (dict): the dictionary from a processed simulation containing 
                              a list of each player's number of tricks, card counts 
                              for each player, and the number of extra cards from this game
        '''
        print(f'Deck shuffle sequence: {self.master_seq}')
        print(f"Two players' sequences: {self.two_player_seqs}")
        
        # call function to get statistics from this deck shuffle and combination of players' sequences
        win_stats = self._recurse()
        print(f"Win stats this round:{win_stats} \n")

        return win_stats
    
    def _recurse(self, 
                 memory: queue.Queue = None, 
                 tricks: list = None, 
                 p1_cards: list = None, 
                 p2_cards: list = None, 
                 extra: list = None, 
                 num_cards: int = 0, 
                 elem_idx: int = 0
                 ) -> dict:
        '''
        Recursive method to iterate through this deck shuffle with this combination of players' 
        sequences, storing the top seq_len cards and making comparisons between this and the sequences,
        tracking statistics for tricks and cards 

        Arguments:
            memory (queue.Queue): the recursively-updated queue of length seq_len or less, putting and 
                                  getting from it as it cycles through the current combination and 
                                  shuffle, against which comparison occurs with the players' sequences, 
                                  checking for tricks
            tricks (list): the recursively-updated list of length 2 for this shuffle with this 
                           combination of sequences, tracking the number of tricks obtained by 
                           Players 1 and 2
            p1_cards (list): the recursively-updated list of length 1 for this shuffle with this 
                             combination of sequences, tracking the number of cards obtained by Player 1
            p2_cards (list): the recursively-updated list of length 1 for this shuffle with this 
                             combination of sequences, tracking the number of cards obtained by Player 2
            extra (list): the recursively-updated list of length 1 for this shuffle with this 
                          combination of sequences, tracking the number of extra cards won by 
                          neither Players
            num_cards (int): the recursively-updated int for this shuffle with this combination of 
                             sequences, tracking the number of cards in play (on the table, not in 
                             either player's hand) eventually added to p1_cards[], p2_cards[], or extra[] 
            elem_idx (int):  the recursively-updated int for this shuffle with this combination, 
                             iterating through the deck and tracking the current index, method concludes 
                             when this int reaches deck length

        Output:
            win_stats (dict): the dictionary from a processed simulation containing 
                              a list of each player's number of tricks, card counts 
                              for each player, and the number of extra cards from this game
        '''
        # add elements to the various lists if starting from the first function call on this deck
        if memory is None:
            memory = queue.Queue()
        if tricks is None:
            tricks = [0, 0]
        if p1_cards is None:
            p1_cards = [0]
        if p2_cards is None:
            p2_cards = [0]  
        if extra is None:
            extra = [0]
        
        # iterate through this deck with this combination of sequences
        if(elem_idx < len(self.master_seq)):
            
            # add one card to deck to bring num cards in queue between 1 and seq_len 
            # for upcoming sequence comparison
            memory.put(self.master_seq[elem_idx])
            num_cards+=1
            # print(f'Current sequence on the table: {tuple(memory.queue)}')
            
            # trick and cards for p1 if p1 sequence matches the top seq_len cards on the table 
            if(tuple(memory.queue) == self.two_player_seqs[0]):
                tricks[0]+=1
                p1_cards[0]+=num_cards
                num_cards = 0
                # print("-----------------------P1 trick-----------------------")

                #remove cards from memory to simulate all the in-play cards going to p1
                while not memory.empty(): 
                    memory.get()
                
                # recurse through this method to make the comparison repeatedly until end of deck 
                return self._recurse(memory, tricks, p1_cards, 
                                    p2_cards, extra, num_cards, elem_idx+1)
            
            # trick and cards for p2 if p2 sequence matches the top seq_len cards on the table 
            elif (tuple(memory.queue) == self.two_player_seqs[1]):
                tricks[1]+=1
                p2_cards[0]+=num_cards
                num_cards = 0
                # print("-----------------------P2 trick-----------------------")

                #remove cards from memory to simulate all the in-play cards going to p1
                while not memory.empty(): 
                    memory.get()
                
                # recurse through this method to make the comparison repeatedly until end of deck 
                return self._recurse(memory, tricks, p1_cards, 
                                    p2_cards, extra, num_cards, elem_idx+1)            

            # if neither sequence matches the top seq_len cards on the table, 
            # remove first added card, keeping queue length at seq_len-1 for next recursive comparison 
            else:
                if(memory.qsize()>=self.seq_len):
                    memory.get() 
                
                # recurse through this method to make the comparison repeatedly until end of deck 
                return self._recurse(memory, tricks, p1_cards, 
                                     p2_cards, extra, num_cards, elem_idx+1)        
        else: 
            # done iterating through full deck, break and return the statistics here in dict form
            extra[0]+=num_cards
            # print("-----------------------Round Over-----------------------")

            win_stats = {"tricks": tricks, "p1_cards": p1_cards, 
                         "p2_cards": p2_cards, "extra cards": extra}
            return(win_stats)
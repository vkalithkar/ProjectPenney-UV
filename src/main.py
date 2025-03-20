import datetime as dt
import sys
import os

from helpers import simulate_and_visualize

# to record all print statements in the log, create the directory if it doesn't exist
log_dir = "data/logs"
os.makedirs(log_dir, exist_ok=True)  

# get current time to identify this run
current_time = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# create a log file to identify this game and open the recording of print statements
log_file_path = os.path.join(log_dir, f"penneys_game_{current_time}.log")
old_stdout = sys.stdout

log_file = open(log_file_path,"w")
sys.stdout = log_file

# start here! modify this function's parameters to change aspects of the simulation
simulate_and_visualize(current_time, seq_len = 3, deck_size = 52, num_decks = 10000, scoring = "CARDS")

sys.stdout = old_stdout
log_file.close()

print("-----------------------Done-----------------------")
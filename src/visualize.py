import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os

def visualize_all_games_output(all_games_output: pd.DataFrame, 
                               current_time: str,
                               title: str = None
                               ) -> None:
    '''
    Visualizes and saves show both plots for frequency of player 1 wins and player 2 wins
    over all shuffles and chosen sequence combinations

    Arguments:
        all_games_output (pd.DataFrame): the pivoted data from a full simulation from one player's 
                                         perspective from which to directly create a heatmap, 
                                         the axes of which are the players' sequences,
                                         and data being frequency of that player's wins
        current_time (str): date and time of this run to create distinct filenames for heatmaps
        title (str): the title to give to this visualization (sns heatmap)
    '''

    # the directory where to save the heatmap, create if doesn't exist
    fig_dir = "heatmaps"  
    os.makedirs(fig_dir, exist_ok=True)

    time_dir = os.path.join(fig_dir, current_time)
    os.makedirs(time_dir, exist_ok=True)

    # generate and save heatmap
    ax = sns.heatmap(all_games_output, linewidth=0.5, cmap='viridis', annot=True)
    ax.set_title(title)

    fig = ax.get_figure()
    file_path = os.path.join(time_dir, f"{title}.png")
    fig.savefig(file_path, dpi=300, bbox_inches="tight")  

    plt.close(fig)

    return



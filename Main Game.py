import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def roll_dice():
    """Rolls 3 dice and returns their values."""
    return [random.randint(1, 6) for _ in range(3)]

def check_tuple_out(dice):
    """Checks if all 3 dice have the same value for a 'tuple out'."""
    return dice[0] == dice[1] == dice[2]

def check_fixed_dice(dice):
    """Determines which dice are fixed (i.e. 2 dice with the same value)."""
    if dice[0] == dice[1] or dice[0] == dice[2]:
        return [True, False, True] if dice[0] == dice[2] else [True, True, False]
    elif dice[1] == dice[2]:
        return [False, True, True]
    else:
        return [False, False, False]

def save_scores(players_df):
    """Saves the current scores of players to a file."""
    players_df.to_csv("scores.csv", index=False)

def load_scores():
    """Loads player scores from a file if it exists."""
    try:
        players_df = pd.read_csv("scores.csv")
    except FileNotFoundError:
        players_df = pd.DataFrame(columns=['name', 'score'])
    return players_df

def get_player_names():
    """Gets player names from user input."""
    num_players = int(input("Enter the number of players: "))
    players = []
    for i in range(num_players):
        name = input(f"Enter the name for player {i+1}: ")
        players.append({'name': name, 'score': 0})
    return pd.DataFrame(players)

def plot_scores(players_df):
    """Plots the final scores of the players."""
    sns.barplot(x='name', y='score', data=players_df)
    plt.title('Final Scores')
    plt.xlabel('Player')
    plt.ylabel('Score')
    plt.show()
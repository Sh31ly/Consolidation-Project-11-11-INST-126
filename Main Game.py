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
    
# Start of the game process
players_df = get_player_names()
target_score = 50

while all(players_df['score'] < target_score):
    for index, player in players_df.iterrows():
        print(f"\n{player['name']}'s turn!")
        dice = roll_dice()
        print(f"Rolled: {dice}")

        while not check_tuple_out(dice):
            fixed = check_fixed_dice(dice)
            if all(fixed):
                print("All dice are fixed. Ending turn.")
                break

            for i in range(3):
                if not fixed[i]:
                    reroll = input(f"Do you want to re-roll dice {i+1} (current value: {dice[i]})? (yes/no): ").strip().lower()
                    if reroll == 'yes':
                        dice[i] = random.randint(1, 6)

            print(f"New roll: {dice}")
            if check_tuple_out(dice):
                print("Tuple out! You scored 0 points for this turn.")
                break

            stop = input("Do you want to stop? (yes/no): ").strip().lower()
            if stop == 'yes':
                players_df.at[index, 'score'] += sum(dice)
                break

        if not check_tuple_out(dice):
            print(f"{player['name']} scored {sum(dice)} points this turn.")
        else:
            print(f"{player['name']} scored 0 points this turn.")

        save_scores(players_df)

        if players_df.at[index, 'score'] >= target_score:
            break

winner = players_df.loc[players_df['score'].idxmax()]
print(f"\nCongratulations, {winner['name']}! You won with {winner['score']} points!")
print("Final scores:")
print(players_df)

# Plot the final scores
plot_scores(players_df)
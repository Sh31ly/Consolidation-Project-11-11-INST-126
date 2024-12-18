import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Function_Land import roll_dice, check_tuple_out, check_fixed_dice, save_scores, load_scores, get_player_names, plot_scores

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
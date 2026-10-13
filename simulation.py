import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from random import choice, randint, uniform

from code_battles_cli.api import Client

maps = ["Interchange", "Yellow Brick", "Temple", "Shapes"]
modes = ["Standard", "Bananza"]

GAMES = 1
MAP = maps[int(sys.argv[1])]
MODE = modes[int(sys.argv[2])]
client = Client()


# returns num. of wins of bot1
def bot_battle(bot1, bot2, games=GAMES):
    ans = 0
    for _ in range(games):
        res = client.run_simulation({"map": MAP, "mode": MODE}, [bot1, bot2], seed=12)
        # assert res.winner_index is not None
        if res.winner_index == 0:
            ans += 1
    return ans


def check_this_const(curr_bot, const):
    temp_file_name = (
        "nabaz"
        + os.sep
        + "nabaz_"
        + "".join([choice("abcdefghijkl") for i in range(10)])
        + ".py"
    )
    with open(temp_file_name, "w") as g:
        g.write("PERCENTAGE_TO_MONKEY = " + str(const) + "\n")
        with open(curr_bot, "r") as f:
            s = "\n".join(f.read().split("\n")[1:])
            # print(s)
            g.write(s)
    # print(const)
    if bot_battle(temp_file_name, curr_bot) == 1:
        if curr_bot != "main.py":
            os.system("rm " + curr_bot)
        return True, temp_file_name
    os.system("rm " + temp_file_name)
    return False, ""


LIST_LEN = 31
TRIES = 50


def localsearch(bot_to_optimize):
    current_bot = bot_to_optimize
    current_state = [1] + [0 for i in range(1, 30)]
    # current_state = [0 for i in range(LIST_LEN)]
    for t in range(TRIES):
        new_state = current_state.copy()
        for i in range(30):
            new_state[i] += uniform(-0.5, 0.5) / (((t + 1) / 2) ** 0.5)
            new_state[i] = min(new_state[i], 1)
            new_state[i] = max(new_state[i], 0)
        swap, f = check_this_const(current_bot, new_state)
        if swap:
            current_bot = f
            current_state = new_state
        print(current_bot)
    return current_bot


print(MAP, MODE)

localsearch("main.py")

# print(bot_battle("nabzan.py", "simple.py"))

import os
import random
from concurrent.futures import ThreadPoolExecutor
from random import choice, randint, uniform

from code_battles_cli.api import Client

GAMES = 1
MAP = "Interchange"
MODE = "normal"


# returns num. of wins of bot1
def bot_battle(bot1, bot2, games=GAMES):
    client = Client()
    ans = 0
    for _ in range(games):
        print(bot1, bot2)
        res = client.run_simulation({"map": MAP, "mode": MODE}, [bot1, bot2], seed=12)
        print(res.winner_index)
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
        return True, temp_file_name
    return False, ""


LIST_LEN = 31
TRIES = 1


def localsearch(bot_to_optimize):
    current_bot = bot_to_optimize
    current_state = [1] + [0.35 + 0.65 * (1 / i) for i in range(1, 30)]
    # current_state = [0 for i in range(LIST_LEN)]
    for _ in range(TRIES):
        print(current_bot)
        new_state = current_state.copy()
        for i in range(10):
            new_state[i] += uniform(-0.1, 0.1)
            new_state[i] = min(new_state[i], 1)
            new_state[i] = max(new_state[i], 0)
        swap, f = check_this_const(current_bot, new_state)
        if swap:
            current_bot = f
    return current_bot


localsearch("main.py")

# print(bot_battle("nabzan.py", "simple.py"))

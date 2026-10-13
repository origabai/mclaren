from concurrent.futures import ThreadPoolExecutor
from random import choice

from code_battles_cli.api import Client

GAMES = 30

# returns num. of wins of bot1
def bot_battle(bot1, bot2, games = GAMES):
    client = Client()
    ans = 0
    for _ in range(games):
        res = client.run_simulation({"map":"Interchange","mode":"normal"}, [bot1, bot2], seed=12)
        print(res)
        if res.winner_index == 0:
            ans += 1
    return ans

good_consts = []

def check_this_const(bot_to_optimize, benchmark_bot, i):
    temp_file_name = "nabaz_" + "".join([choice("abcdefghijkl") for i in range(10)])  +".py"
    with open(temp_file_name, "w") as g:
        g.write("CONST_TO_OPTIMIZE = " + i + "\n")
        with open(bot_to_optimize, "r") as f:
            g.write(f.read())
    if bot_battle(temp_file_name, benchmark_bot, 1) == 1:
        good_consts.append(i)

    

    

def optimize_const(bot_to_optimize, benchmark_bot, const_range):
    with ThreadPoolExecutor(12) as executor:
        for i in const_range:
            executor.submit(check_this_const, bot_to_optimize, benchmark_bot, i)

    print(good_consts)




print(bot_battle("nabzan.py", "simple.py"))

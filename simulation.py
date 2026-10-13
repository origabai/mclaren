from concurrent.futures import ThreadPoolExecutor
from posix import write, closerange

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

def optimize_const(bot_to_optimize, benchmark_bot, const_range, temp_file_name = "temp.py"):
    working_range = []
    with open(bot_to_optimize) as f:
        code = f.read()
        close(f)
    for i in const_range:
        with open(temp_file_name) as f:
            f.write("CONST_TO_OPTIMIZE = " + i + "\n" + code)
            close(f)
        if bot_battle(temp_file_name, benchmark_bot, 1) == 1:




print(bot_battle("nabzan.py", "simple.py"))

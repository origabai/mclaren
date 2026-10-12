from concurrent.futures import ThreadPoolExecutor

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

print(bot_battle("nabzan.py", "simple.py"))

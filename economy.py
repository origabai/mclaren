import api

CURRENT_MAX_BLOON = api.EcoBloons.GROUPED_PINK

def main():
    send_latest_available_bloon()

def get_economy_budget() -> int:
    return 500

def get_round() -> int:
    return 10    

def get_player_index() -> int:
    return 0

def send_bloons():
    pass

def send_latest_available_bloon():
    available_bloons = get_available_bloons()

    if not available_bloons:
        return

    available_bloons = sorted(available_bloons.items(), key=lambda x: x[1].availability_round)
    # print(available_bloons[-1])

    self.context.send_bloons(
        get_player_index(),
        available_bloons[-1][0]
    )

def is_bloon_available(ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
    return (
        ecobloon[1].availability_round <= get_round() and \
        ecobloon[1].cost <= get_economy_budget() and \
        ecobloon[0].value <= CURRENT_MAX_BLOON.value
    )

def get_available_bloons():
    return dict(filter(is_bloon_available, api.ECO_BLOONS_INFO.items()))
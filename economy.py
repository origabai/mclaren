import api
from helpers import ECONOMY_ECONOMY

CURRENT_MAX_BLOON = api.EcoBloons.GROUPED_PINK
MIN_MOAB_CLASS = api.EcoBloons.MOAB

MAX_QUEUE_SIZE = 5

def get_economy_budget() -> int:
    return 500

def get_round() -> int:
    return 10    

def get_player_index() -> int:
    return 0

def send_bloons(strategy: ECONOMY_ECONOMY) -> int:
    """ 
    Decides according to the current strategy which bloons to send.
    
    Returns:
        Amount of budget not used.
    """
    # Prevent sending if full
    if self.context.get_eco_queue_size() >= MAX_QUEUE_SIZE:
        return get_economy_budget()

        # Get available bloons
    available_bloons = get_available_bloons(strategy)
    if not available_bloons:
        return get_economy_budget()

    # sort available bloons
    available_bloons = sorted(available_bloons.items(), key=lambda x: x[1].availability_round)

    # Send the bloon
    result = self.context.send_bloons(
        get_player_index(),
        available_bloons[-1][0]
    )

    # Return how much budget was used
    if result == api.Result.OK:
        return get_economy_budget() - available_bloons[-1][1].cost
    else:
        return get_economy_budget()

def is_available(ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
    """ Returns if a bloon is available"""
    return (
        ecobloon[1].availability_round <= get_round() and \
        ecobloon[1].cost <= get_economy_budget()
    )

def is_latest_bloon_available(ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
    """ Returns if an ecobloon is available to be sent according to round and funds. """
    return (
        is_available(ecobloon) and \
        ecobloon[0].value <= CURRENT_MAX_BLOON.value
    )

def is_latest_moab_available(ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
    """ Returns if an ecobloon is available and is a moab class. """
    return (
        is_available(ecobloon) and \
        ecobloon[0].value >= MIN_MOAB_CLASS.value
    )

def get_available_bloons(strategy: ECONOMY_ECONOMY):
    """ Returns a list of all available bloons according to the strategy. """
    filter_func = is_latest_bloon_available

    match strategy:
        case ECONOMY_ECONOMY.ECONOMY:
            filter_func = is_latest_bloon_available
        case ECONOMY_ECONOMY.DAMAGE:
            filter_func = is_latest_moab_available

    return dict(filter(filter_func, api.ECO_BLOONS_INFO.items()))
from enum import Enum

from api import ArazimWarsBot, Emote, Exceptions, Monkeys
import api

"""
the mighty main of the afek the mighty pytzov founder
author: afek the mighty pytzov founder
"""


# Only pick the cool emotes of course
EMOTES = [Emote.NONE, Emote.COOL, Emote.LAUGHING, Emote.LOVE]
STRENGTH = []
CURRENT_MAX_BLOON = api.EcoBloons.GROUPED_PINK
MIN_MOAB_CLASS = api.EcoBloons.BFB

MAX_QUEUE_SIZE = 5


class ECONOMY_ECONOMY(Enum):
    ECONOMY = 0
    DAMAGE = 1
    CUSTOM = 2
    CAMMO_LEAD = 3


class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkey_count = 0
        self.monkey_levels: list[int] = []
        self.attempted_position = 0
        self.emote_index = 0
        self.defence = False
        self.economy_saving = 0
        self.monkeys_saving = 0
        self.round = 0

    def get_round(self) -> int:
        return self.round

    def update_round(self) -> None:
        if self.context.self.get_round_times()[self.round + 1] <= self.context.get_current_steps():
            self.round += 1

    def get_economy_budget(self) -> int:
        return self.economy_badget

    def get_monkey_budget(self) -> int:
        return self.monkey_badget

    def get_player_index(self) -> int:
        return self.context.get_current_player_index()

    def run(self) -> None:
        self.handle_targets()
        self.manage_budget()
        self.monkeys_spending_roundly = 0
        self.handle_monkeys()
        self.monkeys_saving = self.monkeys_spending_roundly
        if not self.defence:
            self.economy_saving = self.send_baloons(ECONOMY_ECONOMY.ECONOMY)

    def get_board_status(self) -> tuple[int, int]:
        """calculate the cammo baloons strength and the lead baloons strength and the total baloons strength
        (total, cammo, lead)"""
        cammo = 0
        lead = 0
        total = 0
        bloons = self.context.get_bloons()
        return  # TODO
        # for bloon in bloons :

    def manage_budget(self) -> None:
        """
        manging the budget and spliting him pytzovly
        """
        if self.defence:
            self.monkey_badget = self.context.get_current_budget()
            return
        if self.round > 1:
            self.monkey_badget = self.monkeys_saving + int(self.context.get_eco() * 0.40)
            self.economy_badget = self.monkeys_saving + self.context - int(self.context.get_eco() * 0.40)
        else:
            self.monkey_badget = int(self.context.get_money() * 0.9)
            self.economy_badget = self.context.get_money() - int(self.context.get_money() * 0.9)
        return
        # total, cammo, lead= self.get_board_status()

    ############targets sections################
    def handle_targets(self):
        pass

    ############monkeys sections################
    def handle_monkeys(self):
        pass

    ############baloons sections################
    def send_bloons(self, strategy: ECONOMY_ECONOMY) -> int:
        """
        Decides according to the current strategy which bloons to send.

        Returns:
            Amount of budget not used.
        """
        # Prevent sending if full
        if self.context.get_eco_queue_size() >= MAX_QUEUE_SIZE:
            return self.get_economy_budget()

            # Get available bloons
        available_bloons = self.get_available_bloons(strategy)
        if not available_bloons:
            return self.get_economy_budget()

        # sort available bloons
        available_bloons = sorted(available_bloons.items(), key=lambda x: x[1].availability_round)

        # Send the bloon
        result = self.context.send_bloons(self.get_player_index(), available_bloons[-1][0])

        # Return how much budget was used
        if result == api.Result.OK:
            return self.get_economy_budget() - available_bloons[-1][1].cost
        else:
            return self.get_economy_budget()

    def is_available(self, ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
        """Returns if a bloon is available"""
        return ecobloon[1].availability_round <= self.get_round() and ecobloon[1].cost <= self.get_economy_budget()

    def is_latest_bloon_available(self, ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
        """Returns if an ecobloon is available to be sent according to round and funds."""
        return self.is_available(ecobloon) and ecobloon[0].value <= CURRENT_MAX_BLOON.value

    def is_latest_moab_available(self, ecobloon: tuple[api.EcoBloons, api.EcoBloonsInfo]) -> bool:
        """Returns if an ecobloon is available and is a moab class."""
        return self.is_available(ecobloon) and ecobloon[0].value >= MIN_MOAB_CLASS.value

    def get_available_bloons(self, strategy: ECONOMY_ECONOMY):
        """Returns a list of all available bloons according to the strategy."""
        filter_func = self.is_latest_bloon_available

        match strategy:
            case ECONOMY_ECONOMY.ECONOMY:
                filter_func = self.is_latest_bloon_available
            case ECONOMY_ECONOMY.DAMAGE:
                filter_func = self.is_latest_moab_available

        return dict(filter(filter_func, api.ECO_BLOONS_INFO.items()))

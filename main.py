from enum import Enum

from api import ArazimWarsBot, Emote, Exceptions, Monkeys

"""
the mighty main of the afek the mighty pytzov founder
author: afek the mighty pytzov founder
"""


# Only pick the cool emotes of course
EMOTES = [Emote.NONE, Emote.COOL, Emote.LAUGHING, Emote.LOVE]
STRENGTH = []


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
        if self.context.get_round_times()[self.round + 1] <= self.context.get_current_steps():
            self.round += 1

    def get_economy_badget(self) -> int:
        return self.economy_badget

    def get_monkey_badget(self) -> int:
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
            self.economy_saving = self.send_baloons()

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

    def handle_targets(self):
        pass

    def handle_monkeys(self):
        pass

    def send_ballons(self):
        pass

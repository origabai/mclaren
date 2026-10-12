import random
from enum import Enum

import api
from api import ArazimWarsBot, BloonInfo, Bloons, Emote, Exceptions, Maps, MonkeyInfo, Monkeys

"""
the mighty main of the afek the mighty pytzov founder
author: afek the mighty pytzov founder
"""


# Only pick the cool emotes of course
EMOTES = [
    # Emote.NONE,
    Emote.ANGRY,
    # Emote.COOL,
    # Emote.CRYING,
    Emote.FACEPALM,
    # Emote.IDEA_THOUGHT,
    # Emote.LAUGHING,
    # Emote.LOVE,
    Emote.POINTING,
    # Emote.SHOCKED,
    # Emote.SMILE,
    # Emote.THUMBS_DOWN,
    # Emote.THUMBS_UP,
]
STRENGTH = []

# targets


def can_monkey_shoot_lead(monkey: MonkeyInfo) -> bool:
    """
    check if the monkey can shoot lead
    """
    if monkey.kind == Monkeys.DART_MONKEY and monkey.top_level >= 4:
        return True

    if monkey.kind == Monkeys.SUPER_MONKEY and monkey.top_level >= 2:
        return True

    if monkey.kind == Monkeys.BOMB_TOWER:
        return True

    return monkey.kind == Monkeys.SNIPER_MONKEY and monkey.top_level >= 1


def can_monkey_see_camo(monkey: MonkeyInfo) -> bool:
    """
    check if the monkey can see camo
    """
    if monkey.kind == Monkeys.DART_MONKEY and monkey.top_level >= 2:
        return True

    if monkey.kind == Monkeys.NINJA_MONKEY:
        return True

    if monkey.kind == Monkeys.SNIPER_MONKEY and monkey.bottom_level >= 2:
        return True

    return False


def can_monkey_shoot_bloon(monkey: MonkeyInfo, bloon: BloonInfo) -> bool:
    """
    check if the monkey can shoot the bloon
    """
    can_shoot = True

    if bloon.kind == Bloons.LEAD:
        can_shoot &= can_monkey_shoot_lead(monkey)

    if bloon.is_camo:
        can_shoot &= can_monkey_see_camo(monkey)

    if bloon.kind == Bloons.ZEBRA or bloon.kind == Bloons.BLACK and monkey.kind == Monkeys.BOMB_TOWER:
        can_shoot = False

    return can_shoot


# ballons
CURRENT_MAX_BLOON = api.EcoBloons.GROUPED_PINK
MIN_MOAB_CLASS = api.EcoBloons.BFB

MAX_QUEUE_SIZE = 5

# monkeys

PLACING_ORDERS = {
    Maps.INTERCHANGE: {
        "ON_START": [[255, 31], [302, 59], [92, 28], [97, 85]],
        "STRATEGIC": [
            [381, 303],
            [53, 339],
            [394, 361],
            [32, 393],
            [398, 417],
            [383, 479],
            [32, 287],
            [33, 235],
            [28, 471],
            [408, 254],
            [42, 180],
            [48, 548],
            [91, 588],
        ],
        "ON_END": [[409, 531], [425, 588], [264, 602], [206, 611]],
    },
    Maps.SHAPES: {
        "ON_START": [[453, 335], [401, 334], [348, 334], [294, 334]],
        "STRATEGIC": [
            [201, 246],
            [125, 408],
            [123, 466],
            [204, 140],
            [95, 134],
            [333, 122],
            [316, 486],
            [308, 599],
            [122, 593],
        ],
        "ON_END": [[449, 443], [419, 497], [420, 556], [372, 595]],
    },
}


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
        self.monkeys: list[MonkeyInfo] = []
        self.monkeys_spending_roundly = 0
        self.do_next_action = self.progression_handler()
        self.emote_index = 0
        self.emote_wait = False

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
            self.economy_saving = self.send_bloons(ECONOMY_ECONOMY.ECONOMY)
        self.handle_emotes()

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
    def handle_targets(self) -> None:
        """
        1. only shoot bloons you can target
        2. prioritize camo/lead if you can shoot it
        """

        for monkey_index in range(len(self.monkeys)):
            targets: list[BloonInfo] = self.context.get_monkey_targets(monkey_index)
            monkey = self.monkeys[monkey_index]

            found_target = False

            if can_monkey_see_camo(monkey) and can_monkey_shoot_lead(monkey):
                # the monkey can shoot camo lead! prioritize them

                for bloon in targets:
                    if bloon.is_camo and bloon.kind == Bloons.LEAD and can_monkey_shoot_bloon(monkey, bloon):
                        self.context.target_bloon(monkey_index, bloon.index)
                        found_target = True
                        break

                if found_target:
                    continue

            if can_monkey_shoot_lead(monkey):
                # shoot lead if we can
                for bloon in targets:
                    if bloon.kind == Bloons.LEAD and can_monkey_shoot_bloon(monkey, bloon):
                        self.context.target_bloon(monkey_index, bloon.index)
                        found_target = True
                        break

                if found_target:
                    continue

            if can_monkey_see_camo(monkey):
                # shoot camo if we can
                for bloon in targets:
                    if bloon.is_camo and can_monkey_shoot_bloon(monkey, bloon):
                        self.context.target_bloon(monkey_index, bloon.index)
                        found_target = True
                        break

                if found_target:
                    continue

            # our monkey is an efes that cant do anything. so just shoot the first bloon

            for bloon in targets:
                if can_monkey_shoot_bloon(monkey, bloon):
                    self.context.target_bloon(monkey_index, bloon.index)
                    break

    ############monkeys sections################
    def progression_handler(self):
        """
        Makes any number of predefined moves until it runs out of money
        """
        INITIAL_ACTIONS = [
            (lambda: self.place_monkey(Monkeys.DART_MONKEY, self.get_next_coordinate("ON_START")), 200),
            (lambda: self.place_monkey(Monkeys.DART_MONKEY, self.get_next_coordinate("STRATEGIC")), 200),
            (lambda: self.upgrade_monkey(-2, False), 140),
            (lambda: self.upgrade_monkey(-1, True), 90),
            (lambda: self.upgrade_monkey(-1, True), 160),
            (lambda: self.upgrade_monkey(-1, True), 500),
            (lambda: self.place_monkey(Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")), 500),
            (lambda: self.upgrade_monkey(-1, True), 300),
            (lambda: self.upgrade_monkey(-1, True), 250),
            (lambda: self.upgrade_monkey(-1, True), 700),
            (lambda: self.upgrade_monkey(-2, True), 1900),
            (lambda: self.upgrade_monkey(-1, True), 3000),
            (lambda: self.place_monkey(Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")), 3000),
            (lambda: self.upgrade_monkey(-1, True), 3000),
            (lambda: self.upgrade_monkey(-1, True), 4000),
            (lambda: self.upgrade_monkey(-1, False), 800),
            (lambda: self.upgrade_monkey(-1, False), 1200),
            (lambda: self.place_monkey(Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")), 500),
            (lambda: self.upgrade_monkey(-1, True), 300),
            (lambda: self.upgrade_monkey(-1, True), 250),
            (lambda: self.upgrade_monkey(-1, True), 700),
            (lambda: self.upgrade_monkey(-1, True), 3000),
        ]
        REPEAT_ACTIONS = [
            (lambda: self.place_monkey(Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")), 3000),
            (lambda: self.upgrade_monkey(-1, True), 3000),
            (lambda: self.upgrade_monkey(-1, True), 4000),
            (lambda: self.upgrade_monkey(-1, False), 800),
            (lambda: self.upgrade_monkey(-1, False), 1200),
        ]

        while INITIAL_ACTIONS:
            while True:
                next_move_budget = INITIAL_ACTIONS[0][1]
                if next_move_budget + self.monkeys_spending_roundly > self.get_monkey_budget():
                    yield
                else:
                    break
            INITIAL_ACTIONS[0][0]()
            self.monkeys_spending_roundly += INITIAL_ACTIONS[0][1]
            INITIAL_ACTIONS.pop(0)
        repeat_actions_index = 0
        while True:
            while True:
                next_move_budget = REPEAT_ACTIONS[0][1]
                if next_move_budget + self.monkeys_spending_roundly > self.get_monkey_budget():
                    yield
                else:
                    break
            REPEAT_ACTIONS[repeat_actions_index][repeat_actions_index]()
            repeat_actions_index += 1
            if repeat_actions_index >= len(REPEAT_ACTIONS):
                repeat_actions_index = 0
            self.monkeys_spending_roundly += REPEAT_ACTIONS[repeat_actions_index][1]

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> None:
        result = self.context.place_monkey(monkey, position)
        if result == Exceptions.OK:
            self.monkeys.append(MonkeyInfo(monkey, position, 0, 0, 0))  # MONKEY DIRECTION NOT KNOWN FOR FIRST FRAME
            return True
        elif (
            result == Exceptions.OUT_OF_MAP
            or result == Exceptions.TOO_CLOSE_TO_BLOON_ROUTE
            or result == Exceptions.TOO_CLOSE_TO_OTHER_MONKEY
        ):
            self.context.log_warning(f"Couldn't place monkey because of: {result}")
            return result
        elif result == Exceptions.NOT_ENOUGH_MONEY:
            return False

    def upgrade_monkey(self, monkey_index: int, top_row: bool) -> bool:
        result = self.context.upgrade_monkey(monkey_index, top_row)
        if result == Exceptions.NOT_ENOUGH_MONEY:
            return False
        return True

    def get_next_coordinate(self, type: str) -> list[float, float]:
        """
        Get the next free coordinate in the placing order given a placing order
        """
        map = self.context.get_map()
        if PLACING_ORDERS[map][type]:
            return PLACING_ORDERS[map][type].pop(0)
        else:
            available_types = [k for k, v in PLACING_ORDERS[map].items() if v and k != type]
        if not available_types:
            return [0, 0]  # No positions left anywhere
        rand_type = random.choice(available_types)
        return PLACING_ORDERS[map][rand_type].pop(0)

    def handle_monkeys(self):
        next(self.do_next_action)

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

    #####EMOTE######
    def handle_emotes(self) -> None:
        """
        emote handling
        """

        self.emote_index += 1
        if random.randint(0, 60 * 4) == 0:
            self.emote_wait = True

        if self.emote_index % 120 == 0:
            self.emote_wait = False

        if self.emote_wait:
            return
        self.context.display_emote(EMOTES[(self.emote_index) % len(EMOTES)])

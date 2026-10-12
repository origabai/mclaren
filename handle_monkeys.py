import random

from api import (
    MONKEY_COSTS,
    UPGRADE_COSTS,
    ArazimWarsBot,
    Exceptions,
    Maps,
    MonkeyInfo,
    Monkeys,
)

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


PLACING_LAYOUTS = {
    Maps.TEMPLE: [
        ["Dart Monkey", 455, 109],
        *([["UPGRADE", 0, False]] * 1),
        ["Dart Monkey", 284, 161],
        ["Ninja Monkey", 350, 165],
        ["Ninja Monkey", 140, 397],
        ["Super Monkey", 241, 219],
        *([["UPGRADE", 3, True]] * 3),
        ["Super Monkey", 180, 289],
        *([["UPGRADE", 5, True]] * 2),
        *([["UPGRADE", 5, False]] * 2),
        ["Super Monkey", 84, 350],
        *([["UPGRADE", 6, True]] * 2),
        *([["UPGRADE", 6, False]] * 2),
        ["Super Monkey", 42, 426],
        ["Super Monkey", 40, 509],
        *([["UPGRADE", 7, True]] * 2),
        *([["UPGRADE", 7, False]] * 2),
        ["Super Monkey", 343, 49],
        *([["UPGRADE", 8, True]] * 2),
        *([["UPGRADE", 8, False]] * 2),
        *([["UPGRADE", 9, True]] * 3),
        *([["UPGRADE", 9, False]] * 2),
    ]
}

MONKEY_NAMES = {
    "Dart Monkey": Monkeys.DART_MONKEY,
    "Ninja Monkey": Monkeys.NINJA_MONKEY,
    "Super Monkey": Monkeys.SUPER_MONKEY,
}


class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkeys: list[MonkeyInfo] = []
        self.monkeys_spending_roundly = 0
        self.do_next_action = self.progression_handler()

    def _get_action_price(self, action: list) -> int:
        """Get the price of an action"""
        if action[0] == "UPGRADE":
            monkey_to_upgrade = self.monkeys[action[1]]
            # Get the upgrade row:
            is_upgrade_row_top = action[2]
            # Get the monkey's current level in that row:
            monkey_level_in_row = (
                monkey_to_upgrade.top_level
                if is_upgrade_row_top
                else monkey_to_upgrade.bottom_level
            )
            return UPGRADE_COSTS[monkey_to_upgrade.kind][is_upgrade_row_top][monkey_level_in_row]

        else:
            return MONKEY_COSTS[MONKEY_NAMES[action[0]]]

    def _perform_action(self, action: list) -> bool:
        if action[0] == "UPGRADE":
            return self.upgrade_monkey(action[1], action[2])
        else:
            return self.place_monkey(MONKEY_NAMES[action[0]], (action[1], action[2]))

    def progression_handler(self):
        """
        Makes any number of predefined moves until it runs out of money
        """
        INITIAL_ACTIONS = [
            (
                lambda: self.place_monkey(
                    Monkeys.DART_MONKEY, self.get_next_coordinate("ON_START")
                ),
                200,
            ),
            (
                lambda: self.place_monkey(
                    Monkeys.DART_MONKEY, self.get_next_coordinate("STRATEGIC")
                ),
                200,
            ),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 2, False), 140),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 90),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 160),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 500),
            (
                lambda: self.place_monkey(
                    Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")
                ),
                500,
            ),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 300),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 250),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 700),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 2, True), 1900),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 3000),
            (
                lambda: self.place_monkey(
                    Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")
                ),
                3000,
            ),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 3000),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 4000),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, False), 800),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, False), 1200),
            (
                lambda: self.place_monkey(
                    Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")
                ),
                500,
            ),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 300),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 250),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 700),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 3000),
        ]
        REPEAT_ACTIONS = [
            (
                lambda: self.place_monkey(
                    Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")
                ),
                3000,
            ),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 3000),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, True), 4000),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, False), 800),
            (lambda: self.upgrade_monkey(len(self.monkeys) - 1, False), 1200),
        ]

        while INITIAL_ACTIONS:
            while True:
                next_move_budget = INITIAL_ACTIONS[0][1]
                if (
                    next_move_budget + self.monkeys_spending_roundly
                    > self._get_monkey_budget()
                ):
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
                if (
                    next_move_budget + self.monkeys_spending_roundly
                    > self._get_monkey_budget()
                ):
                    yield
                else:
                    break
            REPEAT_ACTIONS[repeat_actions_index][0]()
            repeat_actions_index += 1
            if repeat_actions_index >= len(REPEAT_ACTIONS):
                repeat_actions_index = 0
            self.monkeys_spending_roundly += REPEAT_ACTIONS[repeat_actions_index][1]

    def _get_monkey_budget() -> int:
        """
        Get how much money we have to work with
        """
        raise NotImplementedError

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> None:
        result = self.context.place_monkey(monkey, position)
        if result == Exceptions.OK:
            self.monkeys.append(
                MonkeyInfo(monkey, position, 0, 0, 0)
            )  # MONKEY DIRECTION NOT KNOWN FOR FIRST FRAME
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
        return result == Exceptions.NOT_ENOUGH_MONEY

    def get_next_coordinate(self, type: str) -> list[float, float]:
        """
        Get the next free coordinate in the placing order given a placing order
        """
        map = self.context.get_map()
        if PLACING_ORDERS[map][type]:
            return PLACING_ORDERS[map][type].pop(0)
        else:
            available_types = [
                k for k, v in PLACING_ORDERS[map].items() if v and k != type
            ]
        if not available_types:
            return [0, 0]  # No positions left anywhere
        rand_type = random.choice(available_types)
        return PLACING_ORDERS[map][rand_type].pop(0)

    def run(self) -> None:

        next(self.do_next_action)

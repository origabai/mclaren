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
        self.action_index = 0
        self.map = self.context.get_map()
        self.actions_complete = False

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


    def run(self) -> None:
        if self.action_index >= len(PLACING_LAYOUTS[self.map]):
            self.actions_complete = True
            return
        budget = self._get_monkey_budget()
        used_money = 0
        next_action = PLACING_LAYOUTS[self.map][self.action_index]
        if used_money + self._get_action_price(next_action) < budget:
            self._perform_action(next_action)
            self.action_index += 1

from api import (
    MONKEY_COSTS,
    UPGRADE_COSTS,
    ArazimWarsBot,
    Exceptions,
    GameMode,
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
    ],
    Maps.YELLOW_BRICK: [
        ["Dart Monkey", 104, 95],
        ["Ninja Monkey", 205, 272],
        ["Tack Shooter", 352, 218],
        *([["UPGRADE", 0, False]] * 1),  # Give +1 dmg to dart
        *([["UPGRADE", 0, True]] * 3),  # Turn dart into spike pult
        ["Ninja Monkey", 145, 425],
        *([["UPGRADE", 2, True]] * 2),  # Max tack shooter damage
        *([["UPGRADE", 0, True]] * 1),  # Make juggernaut
        *([["UPGRADE", 2, False]] * 2),  # Max tack shooter range
        *([["UPGRADE", 1, True]] * 4),  # Max ninja 1
        ["Super Monkey", 248, 133],
        *([["UPGRADE", 3, True]] * 4),  # Max ninja 2
        *([["UPGRADE", 4, True]] * 2),  # Max super monkey top
        ["Super Monkey", 148, 235],
        *([["UPGRADE", 5, True]] * 2),
        ["Super Monkey", 88, 298],
        *([["UPGRADE", 6, True]] * 2),
        ["Super Monkey", 341, 431],
        *([["UPGRADE", 7, True]] * 2),
        ["Super Monkey", 402, 367],
        *([["UPGRADE", 8, True]] * 2),
        ["Super Monkey", 298, 277],
        *([["UPGRADE", 9, True]] * 2),
        ["Super Monkey", 242, 337],
        *([["UPGRADE", 10, True]] * 2),
        ["Super Monkey", 434, 141],
        ["Super Monkey", 374, 75],
        ["Super Monkey", 289, 61],
        ["Super Monkey", 192, 66],
        ["Super Monkey", 42, 123],
        ["Super Monkey", 199, 475],
        ["Super Monkey", 278, 496],
        ["Super Monkey", 110, 563],
        ["Super Monkey", 43, 513],
    ],
}

MONKEY_NAMES = {
    "Dart Monkey": Monkeys.DART_MONKEY,
    "Ninja Monkey": Monkeys.NINJA_MONKEY,
    "Super Monkey": Monkeys.SUPER_MONKEY,
    "Tack Shooter": Monkeys.TACK_SHOOTER,
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
            return UPGRADE_COSTS[monkey_to_upgrade.kind][is_upgrade_row_top][
                monkey_level_in_row
            ]

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
        placing_layout = PLACING_LAYOUTS[self.map]
        if isinstance(placing_layout, dict):
            placing_layout = placing_layout[
                ["STANDARD", "BANANZA"][self.context.get_mode() == GameMode.BANANZA]
            ]
        if self.action_index >= len(placing_layout):
            self.actions_complete = True
            return
        budget = self._get_monkey_budget()
        used_money = 0
        next_action = placing_layout[self.action_index]
        if used_money + self._get_action_price(next_action) < budget:
            successful_action = self._perform_action(next_action)
            if successful_action:
                self.action_index += 1

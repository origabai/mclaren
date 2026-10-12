import math
import random
from enum import Enum
from typing import Any

from api import *

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

MONKEY_NAMES = {
    "Dart Monkey": Monkeys.DART_MONKEY,
    "Ninja Monkey": Monkeys.NINJA_MONKEY,
    "Super Monkey": Monkeys.SUPER_MONKEY,
    "Tack Shooter": Monkeys.TACK_SHOOTER,
}

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

    return bool(monkey.kind == Monkeys.SNIPER_MONKEY and monkey.bottom_level >= 2)


def can_monkey_shoot_bloon(monkey: MonkeyInfo, bloon: BloonInfo) -> bool:
    """
    check if the monkey can shoot the bloon
    """
    can_shoot = True

    if bloon.kind == Bloons.LEAD:
        can_shoot &= can_monkey_shoot_lead(monkey)

    if bloon.is_camo:
        can_shoot &= can_monkey_see_camo(monkey)

    # if (
    #     bloon.kind == Bloons.ZEBRA or bloon.kind == Bloons.BLACK
    # ) and monkey.kind == Monkeys.BOMB_TOWER:
    #     can_shoot = False

    return can_shoot


# ballons
CURRENT_MAX_BLOON = EcoBloons.GROUPED_PINK
LEAD_MAX_BLOON = EcoBloons.SPACED_LEAD
MIN_MOAB_CLASS = EcoBloons.BFB

MAX_QUEUE_SIZE = 5

# monkeys


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
        ["Dart Monkey", 151, 241],
        *([["UPGRADE", 0, False]] * 1),
        ["Dart Monkey", 347, 233],
        ["Ninja Monkey", 241, 315],
        ["Ninja Monkey", 173, 455],
        *([["UPGRADE", 0, True]] * 2),
        ["Super Monkey", 246, 136],
        *([["UPGRADE", 4, True]] * 1),
        *([["UPGRADE", 0, True]] * 2),
        *([["UPGRADE", 4, True]] * 1),
        *([["UPGRADE", 2, True]] * 4),
        ["Super Monkey", 77, 302],
        *([["UPGRADE", 5, True]] * 2),
        *([["UPGRADE", 3, True]] * 4),
        ["Super Monkey", 428, 358],
        *([["UPGRADE", 6, True]] * 2),
        ["Super Monkey", 243, 509],
        *([["UPGRADE", 7, True]] * 2),
        ["Super Monkey", 61, 128],
        *([["UPGRADE", 8, True]] * 2),
        ["Super Monkey", 435, 123],
        *([["UPGRADE", 9, True]] * 2),
        ["Super Monkey", 338, 434],
        *([["UPGRADE", 10, True]] * 2),
    ],
    Maps.INTERCHANGE: [
        ["Dart Monkey", 116, 101],
        *([["UPGRADE", 0, False]] * 1),
        ["Dart Monkey", 348, 290],
        ["Tack Shooter", 173, 251],
        ["Ninja Monkey", 353, 482],
        *([["UPGRADE", 0, True]] * 4),
        ["Super Monkey", 57, 336],
        *([["UPGRADE", 4, True]] * 3),
        *([["UPGRADE", 2, True]] * 4),
        ["Super Monkey", 376, 375],
        *([["UPGRADE", 5, True]] * 2),
        *([["UPGRADE", 5, False]] * 2),
        *([["UPGRADE", 3, True]] * 4),
        ["Super Monkey", 61, 168],
        *([["UPGRADE", 6, True]] * 2),
        *([["UPGRADE", 6, False]] * 2),
        ["Super Monkey", 388, 199],
        ["Super Monkey", 332, 78],
        *([["UPGRADE", 7, True]] * 2),
        *([["UPGRADE", 7, False]] * 2),
        ["Super Monkey", 54, 480],
        ["Super Monkey", 413, 290],
        *([["UPGRADE", 8, True]] * 2),
        *([["UPGRADE", 8, False]] * 2),
        *([["UPGRADE", 9, True]] * 3),
        *([["UPGRADE", 9, False]] * 2),
        *([["UPGRADE", 10, True]] * 3),
        *([["UPGRADE", 10, False]] * 2),
    ],
}


class ECONOMY_ECONOMY(Enum):
    ECONOMY = 0
    DAMAGE = 1
    CUSTOM = 2
    LEAD = 3
    CAMO = 4
    CAMMO_LEAD = 5


class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkey_count = 0
        self.monkey_levels: list[int] = []
        self.attempted_position = 0
        self.emote_index = 0
        self.defence = self.context.get_mode() == GameMode.DEFENSE
        self.economy_saving = 0
        self.monkeys_saving = 0
        self.round = 1
        self.monkeys: list[MonkeyInfo] = []
        self.monkeys_spending_roundly = 0
        self.emote_index = 0
        self.emote_wait = False

        self.targeted_enemy_index = self.get_other_player_index()
        self.next_enemy_index = self.get_other_player_index()

        self.action_index = 0
        self.map = self.context.get_map()
        self.actions_complete = False

    def get_round(self) -> int:
        return self.round

    def update_round(self) -> None:
        if (
            self.context.get_round_times()[self.round + 1]
            <= self.context.get_current_steps()
        ):
            self.round += 1

    def get_economy_budget(self) -> int:
        return self.economy_budget

    def get_monkey_budget(self) -> int:
        return self.monkey_budget

    def get_player_index(self) -> int:
        return self.context.get_current_player_index()

    def get_other_player_index(self) -> int:
        index = 0 if self.context.get_current_player_index() != 0 else 1
        players_num = self.context.get_player_count()
        while (
            index < players_num and self.context.get_player_health(index) == 0
        ) or index == self.context.get_current_player_index():
            index += 1
        if index != players_num:
            return index
        return players_num

    def get_enemy_bloons(self) -> list[int]:
        return [x.eco_from for x in self.context.get_bloons() if x.eco_from is not None]

    def update_enemy_index(self) -> None:
        if self.context.get_player_health(self.targeted_enemy_index) <= 0:
            self.targeted_enemy_index = self.next_enemy_index

        if enemy_bloons := self.get_enemy_bloons():
            self.next_enemy_index = enemy_bloons[0]

        if self.next_enemy_index == self.targeted_enemy_index:
            self.next_enemy_index = self.get_other_player_index()

    def _get_action_price(self, action: list[Any]) -> int:
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

    def _perform_action(self, action: list[Any]) -> bool:
        if action[0] == "UPGRADE":
            return self.upgrade_monkey(action[1], action[2])
        else:
            return self.place_monkey(MONKEY_NAMES[action[0]], (action[1], action[2]))

    def run(self) -> None:
        self.update_round()
        self.update_enemy_index()
        self.handle_targets()
        self.manage_budget()
        self.monkeys_spending_roundly = 0
        self.handle_monkeys()
        self.monkeys_saving = self.monkeys_spending_roundly
        if not self.defence:
            self.economy_saving = self.send_bloons(ECONOMY_ECONOMY.ECONOMY)
        self.handle_emotes()

    # def get_board_status(self) -> tuple[int, int]:
    #     """calculate the cammo baloons strength and the lead baloons strength and the total baloons strength
    #     (total, cammo, lead)"""
    #     cammo = 0
    #     lead = 0
    #     total = 0
    #     bloons = self.context.get_bloons()
    #     return  # TODO
    # for bloon in bloons :

    def manage_budget(self) -> None:
        """
        manging the budget and spliting him pytzovly
        """
        if self.defence:
            self.monkey_budget = self.context.get_money()
            return
        self.monkeys_saving = self.context.get_money() - int(self.context.get_eco())
        monkey_add = int(
            self.context.get_eco() * (0.3 + math.sqrt(1 / self.round) * 0.7)
        )
        self.monkey_budget = self.monkeys_saving + monkey_add
        self.economy_budget = (
            self.economy_saving + int(self.context.get_eco()) - monkey_add
        )

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
                    if (
                        bloon.is_camo
                        and bloon.kind == Bloons.LEAD
                        and can_monkey_shoot_bloon(monkey, bloon)
                    ):
                        self.context.target_bloon(monkey_index, bloon.index)
                        found_target = True
                        break

                if found_target:
                    continue

            if can_monkey_shoot_lead(monkey):
                # shoot lead if we can
                for bloon in targets:
                    if bloon.kind == Bloons.LEAD and can_monkey_shoot_bloon(
                        monkey, bloon
                    ):
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

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> bool:
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
            return False
        elif result == Exceptions.NOT_ENOUGH_MONEY:
            return False
        else:
            return False

    def upgrade_monkey(self, monkey_index: int, top_row: bool) -> bool:
        result = self.context.upgrade_monkey(monkey_index, top_row)
        return result != Exceptions.NOT_ENOUGH_MONEY

    def handle_monkeys(self) -> None:
        if self.action_index >= len(PLACING_LAYOUTS[self.map]):
            self.actions_complete = True
            return
        budget = self.get_monkey_budget()
        used_money = 0
        next_action = PLACING_LAYOUTS[self.map][self.action_index]
        if used_money + self._get_action_price(next_action) < budget:
            action_result = self._perform_action(next_action)
            if action_result:
                self.action_index += 1

    ############baloons sections################
    def send_bloons(self, strategy: ECONOMY_ECONOMY) -> int:
        """
        Decides according to the current strategy which bloons to send.

        Returns:
            Amount of budget not used.
        """
        # self.context.log_info(f"round: {self.get_round()}")
        # self.context.log_info(f"budget: {self.get_economy_budget()}")
        # Prevent sending if full
        if self.context.get_eco_queue_size() >= MAX_QUEUE_SIZE:
            return self.get_economy_budget()

        # Get available bloons
        available_bloons = self.get_available_bloons(strategy)
        if not available_bloons:
            return self.get_economy_budget()
        # self.context.log_info(f"2. Available bloons: {available_bloons}")

        # sort available bloons
        sorted_bloons = sorted(
            available_bloons.items(), key=lambda x: x[1].availability_round
        )

        is_camo = self.is_camo_available() and (
            strategy == ECONOMY_ECONOMY.CAMMO_LEAD or strategy == ECONOMY_ECONOMY.CAMO
        )

        # Send the bloon
        result = self.context.send_bloons(
            self.targeted_enemy_index,
            sorted_bloons[-1][0],
            is_camo=is_camo,
        )

        # Return how much budget was used
        if result == Result.OK:
            # self.context.log_info("Successfully sent bloon")
            return self.get_economy_budget() - sorted_bloons[-1][1].cost
        else:
            return self.get_economy_budget()

    def is_camo_available(self) -> bool:
        return self.get_round() >= 8

    def is_available(self, ecobloon: tuple[EcoBloons, EcoBloonsInfo]) -> bool:
        """Returns if a bloon is available"""
        return (
            ecobloon[1].availability_round <= self.get_round()
            and ecobloon[1].cost <= self.get_economy_budget()
        )

    def is_latest_bloon_available(
        self, ecobloon: tuple[EcoBloons, EcoBloonsInfo]
    ) -> bool:
        """Returns if an ecobloon is available to be sent according to round and funds."""
        return (
            self.is_available(ecobloon) and ecobloon[0].value <= CURRENT_MAX_BLOON.value
        )

    def is_latest_lead_available(
        self, ecobloon: tuple[EcoBloons, EcoBloonsInfo]
    ) -> bool:
        """Returns if an ecobloon is available to be sent according to round and funds."""
        return self.is_available(ecobloon) and ecobloon[0].value <= LEAD_MAX_BLOON.value

    def is_latest_moab_available(
        self, ecobloon: tuple[EcoBloons, EcoBloonsInfo]
    ) -> bool:
        """Returns if an ecobloon is available and is a moab class."""
        return self.is_available(ecobloon) and ecobloon[0].value >= MIN_MOAB_CLASS.value

    def get_available_bloons(
        self, strategy: ECONOMY_ECONOMY
    ) -> dict[EcoBloons, EcoBloonsInfo]:
        """Returns a list of all available bloons according to the strategy."""
        filter_func = self.is_latest_bloon_available

        match strategy:
            case ECONOMY_ECONOMY.ECONOMY | ECONOMY_ECONOMY.CAMO:
                filter_func = self.is_latest_bloon_available
            case ECONOMY_ECONOMY.DAMAGE:
                filter_func = self.is_latest_moab_available
            case ECONOMY_ECONOMY.CAMMO_LEAD | ECONOMY_ECONOMY.LEAD:
                filter_func = self.is_latest_lead_available

        return dict(filter(filter_func, ECO_BLOONS_INFO.items()))

    def is_player_camo_lead(self, num: int) -> tuple[bool, bool, bool]:
        monkeys = self.context.get_player_monkeys(num)
        lead = False
        camo = False
        camo_lead = False
        for monkey in monkeys:
            is_camo = can_monkey_see_camo(monkey)
            is_lead = can_monkey_shoot_lead(monkey)
            lead = lead or is_lead
            camo = camo or is_camo
            camo_lead = camo_lead or (is_camo and is_lead)
        return lead, camo, camo_lead

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

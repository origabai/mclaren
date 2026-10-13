import random
import typing
from enum import Enum

from api import *

"""
the mighty main of the afek the mighty pytzov founder
author: afek the mighty pytzov founder
"""

PERCENTAGE_TO_MONKEY = [1] + [0.35 + 0.65 * (1 / i) for i in range(1, 30)]
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
    "Sniper Monkey": Monkeys.SNIPER_MONKEY,
    "Bomb Tower": Monkeys.BOMB_TOWER,
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
REGROW_RAINBOW_MAX_BLOON = EcoBloons.GROUPED_RAINBOW


MAX_QUEUE_SIZE = 5

# monkeys


PLACING_LAYOUTS = {
    Maps.TEMPLE: {
        None: [
            ["Dart Monkey", 455, 109],
            *([["UPGRADE", 0, False]] * 1),
            ["Tack Shooter", 350, 165],
            *([["UPGRADE", 1, True]] * 2),
            ["Ninja Monkey", 284, 161],
            ["Ninja Monkey", 140, 397],
            *([["UPGRADE", 3, True]] * 2),
            ["Super Monkey", 241, 219],
            *([["UPGRADE", 4, True]] * 2),
            ["Super Monkey", 180, 289],
            *([["UPGRADE", 4, False]] * 2),
            ["Super Monkey", 84, 350],
            *([["UPGRADE", 5, True]] * 2),
            *([["UPGRADE", 5, False]] * 2),
            ["Super Monkey", 42, 426],
            ["Super Monkey", 40, 509],
            *([["UPGRADE", 6, True]] * 2),
            *([["UPGRADE", 6, False]] * 2),
            ["Super Monkey", 343, 49],
            *([["UPGRADE", 7, True]] * 2),
            *([["UPGRADE", 7, False]] * 2),
            *([["UPGRADE", 8, True]] * 3),
            *([["UPGRADE", 8, False]] * 2),
        ],
        Monkeys.DART_MONKEY: [],
    },
    Maps.SHAPES: {
        None: [
            ["Dart Monkey", 103, 149],
            *([["UPGRADE", 0, False]] * 1),
            ["Tack Shooter", 192, 302],
            *([["UPGRADE", 1, True]] * 2),
            ["Ninja Monkey", 306, 340],
            ["Ninja Monkey", 190, 244],
            *([["UPGRADE", 0, True]] * 2),
            ["Super Monkey", 125, 400],
            *([["UPGRADE", 4, True]] * 1),
            *([["UPGRADE", 0, True]] * 2),
            *([["UPGRADE", 4, True]] * 1),
            *([["UPGRADE", 2, True]] * 4),
            ["Super Monkey", 133, 485],
            *([["UPGRADE", 5, True]] * 2),
            *([["UPGRADE", 3, True]] * 4),
            ["Super Monkey", 388, 333],
            *([["UPGRADE", 6, True]] * 2),
            ["Super Monkey", 243, 509],
            *([["UPGRADE", 7, True]] * 2),
            ["Super Monkey", 203, 135],
            *([["UPGRADE", 8, True]] * 2),
            ["Super Monkey", 424, 481],
            *([["UPGRADE", 9, True]] * 2),
            ["Super Monkey", 39, 131],
            *([["UPGRADE", 10, True]] * 2),
        ]
    },
    Maps.YELLOW_BRICK: {
        None: [
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
        ]
    },
    Maps.INTERCHANGE: {
        None: [
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
        ]
    },
}


class ECONOMY_ECONOMY(Enum):
    ECONOMY = 0
    DAMAGE = 1
    CUSTOM = 2
    LEAD = 3
    CAMO = 4
    CAMO_LEAD = 5
    REGROW_RAINBOW = 6


class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkey_count = 0
        self.monkey_levels: list[int] = []
        self.attempted_position = 0
        self.emote_index = 0
        self.defence = self.context.get_mode() == GameMode.DEFENSE
        self.round = 1
        self.monkeys: list[MonkeyInfo] = []
        self.monkeys_spending_roundly = 0
        self.emote_index = 0
        self.emote_wait = False
        self.prev_health = 0
        self.enemy = None
        self.prev_money = self.context.get_money()
        self.monkey_saving = self.prev_money
        self.economy_saving = 0
        self.hit_cooldown = 0
        self.monkey_boost = 3

        # Enemy targeting
        self.targeted_enemy = self.get_other_player_index()
        self.next_enemy = self.get_other_player_index()
        self.rainbows_sent = 0

        self.action_index = 0
        self.map = self.context.get_map()
        self.actions_complete = False

        self.players_alive = 0
        self.emote_timer = 0
        self.spam_timer = 0
        self.strategy = ECONOMY_ECONOMY.ECONOMY
        self.context.ban_monkey(Monkeys.SNIPER_MONKEY)

    def get_round(self) -> int:
        return self.round

    def update_round(self) -> None:
        if (
            self.context.get_round_times()[self.round]
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

    def _get_action_price(self, action: list[typing.Any]) -> int:
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
            upgrade_row = 0 if is_upgrade_row_top else 1
            return UPGRADE_COSTS[monkey_to_upgrade.kind][upgrade_row][
                monkey_level_in_row
            ]

        else:
            return MONKEY_COSTS[MONKEY_NAMES[action[0]]]

    def _perform_action(self, action: list[typing.Any]) -> bool:
        if action[0] == "UPGRADE":
            return self.upgrade_monkey(action[1], action[2])
        else:
            return self.place_monkey(MONKEY_NAMES[action[0]], (action[1], action[2]))

    def run(self) -> None:
        self.update_round()
        self.find_someone_to_bully()
        self.handle_targets()
        self.manage_budget()
        self.monkeys_spending_roundly = 0
        self.handle_monkeys()
        self.monkey_saving = self.monkeys_spending_roundly
        if not self.defence:
            self.economy_saving = self.send_bloons(self.strategy)
        self.handle_emotes()
        self.prev_money = self.context.get_money()

    def manage_budget(self) -> None:
        """
        manging the budget and spliting him pytzovly
        """
        if self.defence:
            self.monkey_budget = self.context.get_money()
            return
        my_budget = self.context.get_money()
        new_money = my_budget - self.prev_money
        if self.economy_saving > 500:
            self.economy_saving -= 500
            self.monkey_budget += 500
        self.monkey_budget = self.monkey_saving
        self.economy_budget = self.economy_saving
        adding = int(new_money * PERCENTAGE_TO_MONKEY[self.round])
        if new_money > 0:
            self.monkey_budget += adding
            self.economy_budget += new_money - adding
        curr_health = self.context.get_player_health(self.get_player_index())
        if curr_health < self.prev_health or self.hit_cooldown > 0:
            self.monkey_budget += self.economy_budget
            self.economy_budget = 0
            if curr_health < self.prev_health:
                self.hit_cooldown = 2 * 60
                if (
                    self.monkey_boost > 0
                    and self.context.get_player_remaining_tower_boost_time(self.get_player_index()) == 0
                ):
                    self.monkey_boost -= 1
                    self.context.tower_boost()
            else:
                self.hit_cooldown -= 1
        self.prev_health = curr_health
        if my_budget > self.monkey_budget + self.economy_budget:
            self.monkey_budget += my_budget - (self.monkey_budget + self.economy_budget)

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
            or result == Exceptions.MONKEY_BANNED
        ):
            self.context.log_warning(f"Couldn't place monkey because of: {result}")
            return False
        elif result == Exceptions.NOT_ENOUGH_MONEY:
            return False
        else:
            return False

    def upgrade_monkey(self, monkey_index: int, top_row: bool) -> bool:
        result = self.context.upgrade_monkey(monkey_index, top_row)
        if result == Result.OK:
            if top_row:
                self.monkeys[monkey_index].top_level += 1
            else:
                self.monkeys[monkey_index].bottom_level += 1
        return result == Exceptions.OK

    def _get_layout(self):
        layouts = PLACING_LAYOUTS[self.map]
        for banned in self.context.get_banned_monkeys():
            if banned in layouts:
                return layouts[banned]
        return layouts[None]

    def handle_monkeys(self) -> None:
        layout = self._get_layout()
        if self.action_index >= len(layout):
            self.actions_complete = True
            return
        budget = self.get_monkey_budget()
        used_money = 0
        next_action = layout[self.action_index]
        if used_money + self._get_action_price(next_action) < budget:
            if self._perform_action(next_action):
                self.action_index += 1

    ############baloons sections################
    def send_bloons(self, strategy: ECONOMY_ECONOMY) -> int:
        """
        Decides according to the current strategy which bloons to send.

        Returns:
            Amount of budget not used.
        """
        if (
            self.get_alive_player_count() <= 4
            and self.context.get_player_remaining_bloon_boost_time(
                self.context.get_current_player_index()
            )
            <= 0.0000001
            and self.get_round() >= 8
        ):
            self.context.bloon_boost()

        # Prevent sending if full
        if self.context.get_eco_queue_size() >= MAX_QUEUE_SIZE:
            return self.get_economy_budget()

        # Get available bloons
        available_bloons = self.get_available_bloons(strategy)
        if not available_bloons:
            return self.get_economy_budget()

        # sort available bloons
        sorted_bloons = sorted(
            available_bloons.items(), key=lambda x: x[1].availability_round
        )

        # Get best bloon
        best_bloon = sorted_bloons[-1][0]

        # Decides if should send camo bloons
        is_camo = (
            best_bloon.value < EcoBloons.MOAB.value
            and self.is_camo_available()
            and (
                strategy == ECONOMY_ECONOMY.CAMO_LEAD
                or strategy == ECONOMY_ECONOMY.CAMO
            )
        )

        # Decides if should send regrow bloons
        is_regrow = (
            best_bloon.value < EcoBloons.MOAB.value
            and self.is_regrow_available()
            and (strategy == ECONOMY_ECONOMY.REGROW_RAINBOW)
        )

        # Send the bloon
        result = self.context.send_bloons(
            self.targeted_enemy,
            best_bloon,
            is_camo=is_camo,
            is_regen=is_regrow,
        )

        # Return how much budget was used
        if result == Result.OK:
            if self.strategy == ECONOMY_ECONOMY.REGROW_RAINBOW:
                self.rainbows_sent += 1

            return self.get_economy_budget() - sorted_bloons[-1][1].cost
        else:
            return self.get_economy_budget()

    def is_camo_available(self) -> bool:
        """Returns if camo is available to send"""
        return self.get_round() >= 8

    def is_regrow_available(self) -> bool:
        """Returns if regrow is available to send"""
        return self.get_round() >= 12

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

    def is_latest_rainbow_available(
        self, ecobloon: tuple[EcoBloons, EcoBloonsInfo]
    ) -> bool:
        """Returns if an ecobloon is available to be sent according to round and funds."""
        return (
            self.is_available(ecobloon)
            and ecobloon[0].value <= REGROW_RAINBOW_MAX_BLOON.value
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
            case ECONOMY_ECONOMY.CAMO_LEAD | ECONOMY_ECONOMY.LEAD:
                filter_func = self.is_latest_lead_available
            case ECONOMY_ECONOMY.REGROW_RAINBOW:
                filter_func = self.is_latest_rainbow_available
        return dict(filter(filter_func, ECO_BLOONS_INFO.items()))

    def is_player_camo(self, index: int) -> bool:
        """Checks wether a player can be attacked by camo."""
        monkeys = self.context.get_player_monkeys(index)

        return len(list(filter(lambda monkey: can_monkey_see_camo(monkey), monkeys))) <= 2

    def is_player_lead(self, index: int) -> bool:
        """Checks wether a player can be attacked by lead."""
        monkeys = self.context.get_player_monkeys(index)

        return len(list(filter(lambda monkey: can_monkey_shoot_lead(monkey), monkeys))) <= 2

    def is_player_camo_lead(self, index: int) -> bool:
        """Checks wether a player can be attacked by camo_lead."""
        return self.is_player_lead(index) and self.is_player_camo(index)

    def find_someone_to_bully(self) -> None:
        """
        Calculate the targeted_enemy_index and strategy for sending bloons
        """

        SPECIAL_STRATS = [
            ECONOMY_ECONOMY.LEAD,
            ECONOMY_ECONOMY.CAMO,
            ECONOMY_ECONOMY.CAMO_LEAD,
        ]

        # Enemy fixed weakness change to next_enemy
        if (
            (
                self.strategy == ECONOMY_ECONOMY.CAMO  # Enemy fixed camo
                and not self.is_player_camo(self.targeted_enemy)
            )
            or (
                self.strategy == ECONOMY_ECONOMY.LEAD  # Enemy fixed lead
                and not self.is_player_lead(self.targeted_enemy)
            )
            or (
                self.strategy == ECONOMY_ECONOMY.CAMO_LEAD  # Enemy fixed camo lead
                and not self.is_player_camo_lead(self.targeted_enemy)
            )
        ):
            self.targeted_enemy = self.next_enemy
        if self.get_round() >= 16 and self.rainbows_sent < MAX_QUEUE_SIZE:
            self.strategy = ECONOMY_ECONOMY.REGROW_RAINBOW
        else:
            self.strategy = ECONOMY_ECONOMY.ECONOMY

        # Targeted enemy is dead move to next enemy
        if not self.context.is_player_active(self.targeted_enemy):
            self.targeted_enemy = self.next_enemy

        players_count = self.context.get_player_count()
        my_index = self.context.get_current_player_index()

        for i in range(players_count):
            if i == my_index:  # Can't send bloons to myself
                continue

            if not self.context.is_player_active(i):  # Ignore dead players
                continue

            if self.is_player_camo_lead(i) and self.strategy not in SPECIAL_STRATS:
                self.targeted_enemy = i
                self.strategy = ECONOMY_ECONOMY.CAMO_LEAD
            elif self.is_player_camo(i) and self.strategy not in SPECIAL_STRATS:
                self.targeted_enemy = i
                self.strategy = ECONOMY_ECONOMY.CAMO
            elif self.is_player_lead(i) and self.strategy not in SPECIAL_STRATS:
                self.targeted_enemy = i
                self.strategy = ECONOMY_ECONOMY.LEAD

            if (
                i == self.targeted_enemy
            ):  # Don' pick next enemy that you are already targeting
                continue

            self.next_enemy = i

    def get_alive_player_count(self) -> int:
        return sum(
            1
            for player in range(self.context.get_player_count())
            if self.context.is_player_active(player)
        )

    #####EMOTE######
    def handle_emotes(self) -> None:
        """
        emote handling
        """

        self.spam_timer -= 1

        if self.spam_timer >= 0:
            self.context.display_emote(EMOTES[self.spam_timer % len(EMOTES)])
            return

        curr_alive = 0

        for i in range(self.context.get_player_count()):
            if self.context.is_player_active(i):
                curr_alive += 1

        if self.emote_timer <= 0:
            self.context.display_emote(Emote.COOL)
        self.emote_timer -= 1

        if curr_alive < self.players_alive:
            self.context.display_emote(Emote.LAUGHING)
            self.emote_timer = 60 * 4

        self.players_alive = curr_alive

        if random.randint(0, 60 * 10) == 0:
            self.spam_timer = 60 * 4

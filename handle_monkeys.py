from api import ArazimWarsBot, Emote, Exceptions, Monkeys, MonkeyInfo, Maps
import random

PLACING_ORDERS = {
    Maps.INTERCHANGE: {
        "ON_START": [[255,31],[302,59],[92,28],[97,85]],
        "STRATEGIC": [[381,303],[53,339],[394,361],[32,393],[398,417],[383,479],[32,287],[33,235],[28,471],[408,254],[42,180],[48,548],[91,588]],
        "ON_END": [[409,531],[425,588],[264,602],[206,611]]
    },
    Maps.SHAPES: {
        "ON_START": [[453,335],[401,334],[348,334],[294,334]],
        "STRATEGIC": [[201,246],[125,408],[123,466],[204,140],[95,134],[333,122],[316,486],[308,599],[122,593]],
        "ON_END": [[449,443],[419,497],[420,556],[372,595]]
    },
    }

class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkeys: list[MonkeyInfo] = []
        self.monkeys_spending_roundly = 0

    def progression_handler(self):
        """
        Makes any number of predefined moves until it runs out of money
        """
        INITIAL_ACTIONS = [
            self.place_monkey(Monkeys.DART_MONKEY, self.get_next_coordinate("ON_START")),
            self.place_monkey(Monkeys.DART_MONKEY, self.get_next_coordinate("STRATEGIC")),
            self.upgrade_monkey(-2, False),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.place_monkey(Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-2, True),
            self.upgrade_monkey(-1, True),
            self.place_monkey(Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")),
            self.upgrade_monkey(-1, False),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, False),
            self.place_monkey(Monkeys.NINJA_MONKEY, self.get_next_coordinate("STRATEGIC")),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True)
        ]
        REPEAT_ACTIONS = [
            self.place_monkey(Monkeys.SUPER_MONKEY, self.get_next_coordinate("STRATEGIC")),
            self.upgrade_monkey(-1, False),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, True),
            self.upgrade_monkey(-1, False)
        ]

        while INITIAL_ACTIONS:
            money = self.context.get_money()
            action_success = INITIAL_ACTIONS[0]()
            self.monkeys_spending_roundly = money - self.context.get_money()
            if not action_success:
                yield
        repeat_actions_index = 0
        while True:
            money = self.context.get_money()
            action_success = REPEAT_ACTIONS[repeat_actions_index]()
            repeat_actions_index +=1
            if repeat_actions_index >= len(REPEAT_ACTIONS):
                repeat_actions_index = 0
            self.monkeys_spending_roundly = money - self.context.get_money()
            if not action_success:
                yield

    def _get_monkey_budget() -> int:
        """
        Get how much money we have to work with
        """
        raise NotImplementedError

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> None:
        result = self.context.place_monkey(monkey, position)
        if result == Exceptions.OK:
            self.monkeys.append(MonkeyInfo(Monkeys, position, 0, 0, 0)) # MONKEY DIRECTION NOT KNOWN FOR FIRST FRAME
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
        result =  self.context.upgrade_monkey(monkey_index, top_row)
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
            return [0,0]  # No positions left anywhere
        rand_type = random.choice(available_types)
        return PLACING_ORDERS[map][rand_type].pop(0)


    def run(self) -> None:
        do_next_action = self.progression_handler()
        current_money = self._get_monkey_budget()
        next(do_next_action)

    


from api import ArazimWarsBot, Emote, Exceptions, Monkeys, MonkeyInfo

def calculate_funds() -> int:
    """
    Figure out how much money we have to work with
    """
    raise NotImplementedError

class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkeys: list[MonkeyInfo] = []

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> None:
        result = self.context.place_monkey(monkey, position)
        if result == Exceptions.OK:
            self.monkeys.append(MonkeyInfo(Monkeys, position, 0, 0, 0)) # MONKEY DIRECTION NOT KNOWN FOR FIRST FRAME
        elif (
            result == Exceptions.OUT_OF_MAP
            or result == Exceptions.TOO_CLOSE_TO_BLOON_ROUTE
            or result == Exceptions.TOO_CLOSE_TO_OTHER_MONKEY
        ):
            self.context.log_warning(f"Couldn't place monkey because of: {result}")


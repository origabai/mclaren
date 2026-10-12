from api import ArazimWarsBot, Emote, Exceptions, Monkeys

def calculate_funds() -> int:
    """
    Figure out how much money we have to work with
    """
    raise NotImplementedError

class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.monkeys = [] # [
                        #       {
                        #           "type": Monkeys, 
                        #           "levels": List[int, int], 
                        #           "position": List[float, float]}
                        #       } ]

    def place_monkey(self, monkey: Monkeys, position: tuple[float, float]) -> None:
        result = self.context.place_monkey(monkey, position)
        if result == Exceptions.OK:
            self.monkeys.append({"type": monkey, "levels": [0,0], "position": position})
        elif (
            result == Exceptions.OUT_OF_MAP
            or result == Exceptions.TOO_CLOSE_TO_BLOON_ROUTE
            or result == Exceptions.TOO_CLOSE_TO_OTHER_MONKEY
        ):
            self.context.log_warning(f"Couldn't place monkey because of: {result}")


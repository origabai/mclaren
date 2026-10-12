import numpy as np
from api import *

def handle_monkey_targets_first(self) -> None:
    """
    Basic monkey targeting handling.
    Picks the first visible target for each monkey.
    """

    for monkey_index in range(self.monkey_count):
        # Target Bloons
        targets = self.context.get_monkey_targets(monkey_index)
        if len(targets) > 0:
            self.context.target_bloon(monkey_index, targets[0].index)

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

    if monkey.kind == Monkeys.SNIPER_MONKEY and monkey.top_level >= 1:
        return True

    return False

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

    


def better_handle_monkey_targets(self) -> None:
    """
    only shoot bloons you can target
    """
    for monkey_index in range(self.monkey_count):
        targets = self.context.get_monkey_targets(monkey_index)
        monkey = self.monkeys[monkey_index]

        for bloon in targets:
            if can_monkey_shoot_bloon(monkey, bloon):
                self.context.target_bloon(monkey_index, bloon.index)
                break

def even_better_handle_targets(self) -> None:
    """
    1. only shoot bloons you can target
    2. prioritize camo/lead if you can shoot it
    """

    for monkey_index in range(self.monkey_count):
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
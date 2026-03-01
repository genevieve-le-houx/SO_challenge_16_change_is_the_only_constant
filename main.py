import math
from typing import Tuple, Dict, List
from pathlib import Path
import json


def read_input(filepath: Path) -> List[Tuple[Dict[int, int], int]]:
    list_data = []

    with open(filepath, "r") as f:
        content = json.load(f)

    for line in content:
        denominations, counts, target = line

        coins_available = {}
        for denomination, count in zip(denominations, counts):
            coins_available[denomination] = count

        list_data.append((coins_available, target))

    return list_data

def adjust_available_qty(coins_available: Dict[int, int], chosen_coins: Dict[int, int], coin: int) -> None:
    coins_available[coin] -= 1

    if coins_available[coin] == 0:
        coins_available.pop(coin)

    if coin not in chosen_coins.keys():
        chosen_coins[coin] = 1
    else:
        chosen_coins[coin] += 1


def recursive_build_possibility(
    coins_available: Dict[int, int], chosen_coins: Dict[int, int], total: int, target: int,
    possibilities: List[Dict[int, int]]
):
    if chosen_coins:
        biggest_chosen = max(chosen_coins.keys())
    else:
        biggest_chosen = max(coins_available.keys())

    # Assume we can only pick smaller or equal to the biggest chosen coin,
    # cause if we could take an higher coin we would have do so earlier
    possibility_coins = sorted([x for x in coins_available.keys() if total + x <= target and x <= biggest_chosen])

    can_continue = len(possibility_coins) != 0

    chosen_coins_before_coin_choice = chosen_coins.copy()
    available_coins_before_coin_choice = coins_available.copy()
    for coin in possibility_coins:
        # Remove all denomination higher than coins
        list_denominations = list(coins_available.keys())
        for denomination in list_denominations:
            if denomination > coin:
                coins_available.pop(denomination)

        adjust_available_qty(coins_available, chosen_coins, coin)
        total = get_total(chosen_coins)

        while total < target:
            can_continue, total, chosen_coins = recursive_build_possibility(
                coins_available, chosen_coins, total, target, possibilities
            )
            if not can_continue:
                break

        if validate_solution(chosen_coins, target):
            possibilities.append(chosen_coins)

        # Put back from before coin choice
        chosen_coins = chosen_coins_before_coin_choice.copy()
        coins_available = available_coins_before_coin_choice.copy()

    return can_continue, total, chosen_coins



def get_minimum_coins(coins_available: Dict[int, int], target: int) -> Dict[int, int] | None:
    coins_available_copy = coins_available.copy()

    possibilities = []

    chosen_coins = {}
    total = 0

    recursive_build_possibility(
        coins_available_copy, chosen_coins, total, target, possibilities
    )

    # Evaluate all possibilities
    smallest_count = math.inf
    smallest_possibility = None
    for possibily in possibilities:
        count = sum(possibily.values())
        if count < smallest_count:
            smallest_count = count
            smallest_possibility = possibily

    return smallest_possibility

def get_total(chosen_coins: Dict[int, int]) -> int:
    total = 0
    for coin, count in chosen_coins.items():
        total += coin*count

    return total

def validate_solution(chosen_coins: Dict[int, int], target: int) -> bool:
    total = get_total(chosen_coins)

    return total == target

def build_answer(solution: Dict[int, int] | None) -> int:
    return -1 if solution is None else sum(solution.values())


def main():
    list_data = read_input(Path("Challenge16.txt"))

    solutions: List[Dict[int, int] | None] = []
    for i, (coins_available, target) in enumerate(list_data):
        minimum_coins = get_minimum_coins(coins_available, target)
        if minimum_coins:
            if not validate_solution(minimum_coins, target):
                print(f"Problem with index {i}")

        solutions.append(minimum_coins)

    targets = [x[1] for x in list_data]
    zipped_data = list(zip(solutions, targets))
    print(zipped_data)

    n_coins_needed = [build_answer(solution) for solution in solutions]
    print(n_coins_needed)


if __name__ == "__main__":
    main()

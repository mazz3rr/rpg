from enum import IntEnum
from math import comb


class Dice(IntEnum):
    D3  = 3
    D4  = 4
    D5  = 5
    D6  = 6
    D7  = 7
    D8  = 8
    D10 = 10
    D12 = 12
    D14 = 14
    D16 = 16
    D20 = 20
    D30 = 30


def dice_prob(
    n_dice: int, threshold: int, successes: int = 1, dice: int | Dice = Dice.D10) -> float:
    """Roll the specified dice.

    Returns probability of having AT LEAST specified number of successes (<= threshold).
    """
    dice = Dice(dice)
    if n_dice < 1:
        raise ValueError(f"n_dice must be ≥ 1, got {n_dice}")
    if not (1 <= threshold <= dice.value):
        raise ValueError(
            f"threshold must be between 1 and {dice.value} ({dice.name}), got {threshold}")
    if not (0 <= successes <= n_dice):
        raise ValueError(f"successes must be between 0 and {n_dice}, got {successes}")

    p = threshold / dice.value
    return sum(
        comb(n_dice, k) * p**k * (1 - p)**(n_dice - k)
        for k in range(successes, n_dice + 1)
    )

"""
Scoring logic for Flip 7 game.

Handles calculation of final scores based on hand contents and modifiers.
"""

from typing import List
from src.player_hand import PlayerHand
from src.card import Card, ModifierType


def calculate_score(hand: PlayerHand, has_flip_seven_bonus: bool) -> int:
    """
    Calculate the final score for a player's hand.

    Scoring order:
    1. If busted, return 0
    2. Sum unique number cards
    3. Apply X2 modifier if present
    4. Add point modifiers (+2, +4, +6, +8, +10)
    5. Add Flip 7 bonus (+15) if applicable

    Args:
        hand: The player's hand
        has_flip_seven_bonus: Whether this player gets the Flip 7 bonus

    Returns:
        Final score for the hand
    """
    if hand.has_busted:
        return 0

    base_score = sum(hand.number_cards)

    if has_times_two_modifier(hand.modifiers):
        base_score *= 2

    modifier_points = get_modifier_points(hand.modifiers)
    total = base_score + modifier_points

    if has_flip_seven_bonus:
        total += 15

    return total


def has_times_two_modifier(modifiers: List[Card]) -> bool:
    """
    Check if X2 modifier is present.

    Args:
        modifiers: List of modifier cards

    Returns:
        True if X2 modifier is present
    """
    return any(card.modifier_type == ModifierType.TIMES_2 for card in modifiers)


def get_modifier_points(modifiers: List[Card]) -> int:
    """
    Calculate total points from point modifier cards.

    Args:
        modifiers: List of modifier cards

    Returns:
        Sum of all point modifier values
    """
    total = 0
    for card in modifiers:
        if card.modifier_type != ModifierType.TIMES_2:
            total += card.modifier_value
    return total

"""
Deck management for Flip 7 game.

Handles creation, shuffling, and drawing from the 94-card deck.
"""

import random
from typing import List
from src.card import Card, CardType, ActionType, ModifierType


class Deck:
    """
    Manages the 94-card deck for Flip 7.

    The deck contains:
    - Number cards 0-12 (counts: 1,1,2,3,4,5,6,7,8,9,10,11,12)
    - Modifiers: +2, +4, +6, +8, +10, X2
    - Actions: 3x Freeze, 3x Flip Three, 3x Second Chance
    """

    def __init__(self):
        """Create a new deck with standard 94-card composition."""
        self._cards: List[Card] = self._create_standard_deck()
        self._original_cards: List[Card] = self._cards.copy()

    def _create_standard_deck(self) -> List[Card]:
        """
        Create the standard 94-card Flip 7 deck.

        Returns:
            List of 94 cards with correct composition
        """
        cards = []

        for value in range(13):
            count = 1 if value <= 1 else value
            for _ in range(count):
                cards.append(Card(type=CardType.NUMBER, value=value))

        modifier_cards = [
            (ModifierType.PLUS_2, 2),
            (ModifierType.PLUS_4, 4),
            (ModifierType.PLUS_6, 6),
            (ModifierType.PLUS_8, 8),
            (ModifierType.PLUS_10, 10),
            (ModifierType.TIMES_2, 0),
        ]
        for mod_type, mod_value in modifier_cards:
            cards.append(
                Card(
                    type=CardType.MODIFIER,
                    modifier_type=mod_type,
                    modifier_value=mod_value,
                )
            )

        action_cards = [
            (ActionType.FREEZE, 3),
            (ActionType.FLIP_THREE, 3),
            (ActionType.SECOND_CHANCE, 3),
        ]
        for action_type, count in action_cards:
            for _ in range(count):
                cards.append(Card(type=CardType.ACTION, action_type=action_type))

        return cards

    def shuffle(self) -> None:
        """Randomize the order of cards in the deck."""
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """
        Remove and return the top card from the deck.

        Returns:
            The drawn card

        Raises:
            IndexError: If the deck is empty
        """
        if not self._cards:
            raise IndexError("Cannot draw from empty deck")
        return self._cards.pop()

    def cards_remaining(self) -> int:
        """
        Get the number of cards remaining in the deck.

        Returns:
            Number of cards left
        """
        return len(self._cards)

    def reset(self) -> None:
        """Restore the full deck and shuffle it."""
        self._cards = self._original_cards.copy()
        self.shuffle()

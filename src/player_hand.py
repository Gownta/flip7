"""
Player hand management for Flip 7 game.

Tracks player state including cards held, bust status, and special abilities.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Set, List
from src.card import Card, CardType, ActionType


class AddCardResult(Enum):
    """Result of adding a card to a player's hand."""

    SUCCESS = auto()
    BUST = auto()
    DUPLICATE_WITH_SECOND_CHANCE = auto()
    FROZEN = auto()


@dataclass
class PlayerHand:
    """
    Represents a player's hand in Flip 7.

    Tracks number cards, modifiers, action cards, and special states like
    bust, freeze, and second chance availability.
    """

    number_cards: Set[int] = field(default_factory=set)
    modifiers: List[Card] = field(default_factory=list)
    action_cards: List[Card] = field(default_factory=list)
    second_chance_available: bool = False
    is_frozen: bool = False
    has_busted: bool = False

    def add_card(self, card: Card) -> AddCardResult:
        """
        Add a card to the player's hand.

        Args:
            card: The card to add

        Returns:
            Result of adding the card
        """
        if self.is_frozen:
            return AddCardResult.FROZEN

        if card.type == CardType.NUMBER:
            if card.value in self.number_cards:
                if self.second_chance_available:
                    return AddCardResult.DUPLICATE_WITH_SECOND_CHANCE
                else:
                    self.has_busted = True
                    return AddCardResult.BUST
            else:
                self.number_cards.add(card.value)
                return AddCardResult.SUCCESS

        elif card.type == CardType.MODIFIER:
            self.modifiers.append(card)
            return AddCardResult.SUCCESS

        elif card.type == CardType.ACTION:
            if card.action_type == ActionType.FREEZE:
                self.is_frozen = True
                return AddCardResult.FROZEN
            elif card.action_type == ActionType.SECOND_CHANCE:
                self.second_chance_available = True
                self.action_cards.append(card)
                return AddCardResult.SUCCESS
            else:
                self.action_cards.append(card)
                return AddCardResult.SUCCESS

        return AddCardResult.SUCCESS

    def use_second_chance(self, duplicate_card: Card) -> None:
        """
        Use Second Chance to discard a duplicate number card.

        Args:
            duplicate_card: The duplicate card to discard
        """
        if not self.second_chance_available:
            raise ValueError("No Second Chance available")

        if duplicate_card.type != CardType.NUMBER:
            raise ValueError("Can only use Second Chance on number cards")

        if duplicate_card.value not in self.number_cards:
            raise ValueError("Card is not in hand")

        self.second_chance_available = False
        for i, card in enumerate(self.action_cards):
            if card.action_type == ActionType.SECOND_CHANCE:
                self.action_cards.pop(i)
                break

    def has_flip_seven(self) -> bool:
        """
        Check if player has exactly 7 unique number cards.

        Returns:
            True if player has Flip 7
        """
        return len(self.number_cards) == 7

    def clear(self) -> None:
        """Reset the hand for a new round."""
        self.number_cards.clear()
        self.modifiers.clear()
        self.action_cards.clear()
        self.second_chance_available = False
        self.is_frozen = False
        self.has_busted = False

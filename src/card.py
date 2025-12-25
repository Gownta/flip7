"""
Card system for Flip 7 game.

Defines card types, enums, and the Card dataclass.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class CardType(Enum):
    """Type of card in the Flip 7 deck."""

    NUMBER = auto()
    MODIFIER = auto()
    ACTION = auto()


class ActionType(Enum):
    """Action card types."""

    FREEZE = auto()
    FLIP_THREE = auto()
    SECOND_CHANCE = auto()


class ModifierType(Enum):
    """Modifier card types."""

    PLUS_2 = auto()
    PLUS_4 = auto()
    PLUS_6 = auto()
    PLUS_8 = auto()
    PLUS_10 = auto()
    TIMES_2 = auto()


@dataclass(frozen=True)
class Card:
    """
    Represents a card in the Flip 7 game.

    Cards are immutable to prevent accidental modification.
    """

    type: CardType
    value: Optional[int] = None
    action_type: Optional[ActionType] = None
    modifier_type: Optional[ModifierType] = None
    modifier_value: int = 0

    def __post_init__(self):
        """Validate card creation."""
        if self.type == CardType.NUMBER:
            if self.value is None:
                raise ValueError("Number cards must have a value")
            if not (0 <= self.value <= 12):
                raise ValueError("Number card value must be 0-12")
        elif self.type == CardType.ACTION:
            if self.action_type is None:
                raise ValueError("Action cards must have an action_type")
        elif self.type == CardType.MODIFIER:
            if self.modifier_type is None:
                raise ValueError("Modifier cards must have a modifier_type")

    def __str__(self) -> str:
        """String representation of the card."""
        if self.type == CardType.NUMBER:
            return f"Number({self.value})"
        elif self.type == CardType.MODIFIER:
            if self.modifier_type == ModifierType.TIMES_2:
                return "Modifier(X2)"
            else:
                return f"Modifier(+{self.modifier_value})"
        else:
            return f"Action({self.action_type.name})"

"""Unit tests for card.py"""

import unittest
from src.card import Card, CardType, ActionType, ModifierType


class TestCard(unittest.TestCase):
    """Test Card creation and validation."""

    def test_create_number_card(self):
        """Test creating number cards."""
        for value in range(13):
            card = Card(type=CardType.NUMBER, value=value)
            self.assertEqual(card.type, CardType.NUMBER)
            self.assertEqual(card.value, value)
            self.assertIsNone(card.action_type)
            self.assertIsNone(card.modifier_type)

    def test_create_action_cards(self):
        """Test creating action cards."""
        for action in ActionType:
            card = Card(type=CardType.ACTION, action_type=action)
            self.assertEqual(card.type, CardType.ACTION)
            self.assertEqual(card.action_type, action)
            self.assertIsNone(card.value)
            self.assertIsNone(card.modifier_type)

    def test_create_modifier_cards(self):
        """Test creating modifier cards."""
        modifiers = [
            (ModifierType.PLUS_2, 2),
            (ModifierType.PLUS_4, 4),
            (ModifierType.PLUS_6, 6),
            (ModifierType.PLUS_8, 8),
            (ModifierType.PLUS_10, 10),
            (ModifierType.TIMES_2, 0),
        ]
        for mod_type, mod_value in modifiers:
            card = Card(
                type=CardType.MODIFIER, modifier_type=mod_type, modifier_value=mod_value
            )
            self.assertEqual(card.type, CardType.MODIFIER)
            self.assertEqual(card.modifier_type, mod_type)
            self.assertEqual(card.modifier_value, mod_value)
            self.assertIsNone(card.value)
            self.assertIsNone(card.action_type)

    def test_number_card_requires_value(self):
        """Test that number cards require a value."""
        with self.assertRaises(ValueError):
            Card(type=CardType.NUMBER)

    def test_number_card_value_range(self):
        """Test that number card values must be 0-12."""
        with self.assertRaises(ValueError):
            Card(type=CardType.NUMBER, value=-1)
        with self.assertRaises(ValueError):
            Card(type=CardType.NUMBER, value=13)

    def test_action_card_requires_action_type(self):
        """Test that action cards require an action_type."""
        with self.assertRaises(ValueError):
            Card(type=CardType.ACTION)

    def test_modifier_card_requires_modifier_type(self):
        """Test that modifier cards require a modifier_type."""
        with self.assertRaises(ValueError):
            Card(type=CardType.MODIFIER)

    def test_card_immutability(self):
        """Test that cards are immutable (frozen)."""
        card = Card(type=CardType.NUMBER, value=5)
        with self.assertRaises(Exception):
            card.value = 10

    def test_card_str_representation(self):
        """Test string representation of cards."""
        num_card = Card(type=CardType.NUMBER, value=7)
        self.assertEqual(str(num_card), "Number(7)")

        action_card = Card(type=CardType.ACTION, action_type=ActionType.FREEZE)
        self.assertEqual(str(action_card), "Action(FREEZE)")

        mod_card = Card(
            type=CardType.MODIFIER, modifier_type=ModifierType.PLUS_4, modifier_value=4
        )
        self.assertEqual(str(mod_card), "Modifier(+4)")

        x2_card = Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2)
        self.assertEqual(str(x2_card), "Modifier(X2)")

    def test_card_equality(self):
        """Test that identical cards are equal (important for frozen dataclass)."""
        card1 = Card(type=CardType.NUMBER, value=5)
        card2 = Card(type=CardType.NUMBER, value=5)
        self.assertEqual(card1, card2)

    def test_card_hashability(self):
        """Test that cards can be hashed (frozen dataclass)."""
        card = Card(type=CardType.NUMBER, value=5)
        card_set = {card}
        self.assertIn(card, card_set)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for player_hand.py"""

import unittest
from src.player_hand import PlayerHand, AddCardResult
from src.card import Card, CardType, ActionType, ModifierType


class TestPlayerHand(unittest.TestCase):
    """Test PlayerHand state tracking and card management."""

    def test_add_number_card_success(self):
        """Test adding unique number cards."""
        hand = PlayerHand()
        card = Card(type=CardType.NUMBER, value=5)
        result = hand.add_card(card)
        self.assertEqual(result, AddCardResult.SUCCESS)
        self.assertIn(5, hand.number_cards)
        self.assertFalse(hand.has_busted)

    def test_add_duplicate_number_card_busts(self):
        """Test that duplicate number cards cause bust."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        result = hand.add_card(Card(type=CardType.NUMBER, value=5))
        self.assertEqual(result, AddCardResult.BUST)
        self.assertTrue(hand.has_busted)

    def test_add_duplicate_with_second_chance_available(self):
        """Test duplicate detection when Second Chance is available."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.ACTION, action_type=ActionType.SECOND_CHANCE))
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        result = hand.add_card(Card(type=CardType.NUMBER, value=5))
        self.assertEqual(result, AddCardResult.DUPLICATE_WITH_SECOND_CHANCE)
        self.assertFalse(hand.has_busted)

    def test_use_second_chance(self):
        """Test using Second Chance to avoid bust."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.ACTION, action_type=ActionType.SECOND_CHANCE))
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        duplicate = Card(type=CardType.NUMBER, value=5)
        result = hand.add_card(duplicate)
        self.assertEqual(result, AddCardResult.DUPLICATE_WITH_SECOND_CHANCE)

        hand.use_second_chance(duplicate)
        self.assertFalse(hand.second_chance_available)
        self.assertFalse(hand.has_busted)

    def test_add_modifier_card(self):
        """Test adding modifier cards."""
        hand = PlayerHand()
        card = Card(
            type=CardType.MODIFIER, modifier_type=ModifierType.PLUS_4, modifier_value=4
        )
        result = hand.add_card(card)
        self.assertEqual(result, AddCardResult.SUCCESS)
        self.assertIn(card, hand.modifiers)

    def test_add_freeze_card(self):
        """Test that Freeze card freezes the hand."""
        hand = PlayerHand()
        card = Card(type=CardType.ACTION, action_type=ActionType.FREEZE)
        result = hand.add_card(card)
        self.assertEqual(result, AddCardResult.FROZEN)
        self.assertTrue(hand.is_frozen)

    def test_cannot_add_cards_when_frozen(self):
        """Test that frozen hands cannot accept more cards."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.ACTION, action_type=ActionType.FREEZE))
        result = hand.add_card(Card(type=CardType.NUMBER, value=5))
        self.assertEqual(result, AddCardResult.FROZEN)
        self.assertNotIn(5, hand.number_cards)

    def test_add_flip_three_card(self):
        """Test adding Flip Three action card."""
        hand = PlayerHand()
        card = Card(type=CardType.ACTION, action_type=ActionType.FLIP_THREE)
        result = hand.add_card(card)
        self.assertEqual(result, AddCardResult.SUCCESS)
        self.assertIn(card, hand.action_cards)

    def test_has_flip_seven(self):
        """Test Flip 7 detection with exactly 7 unique numbers."""
        hand = PlayerHand()
        for i in range(7):
            hand.add_card(Card(type=CardType.NUMBER, value=i))
        self.assertTrue(hand.has_flip_seven())

    def test_not_flip_seven_with_six_cards(self):
        """Test that 6 unique numbers is not Flip 7."""
        hand = PlayerHand()
        for i in range(6):
            hand.add_card(Card(type=CardType.NUMBER, value=i))
        self.assertFalse(hand.has_flip_seven())

    def test_not_flip_seven_with_eight_cards(self):
        """Test that 8 unique numbers is not Flip 7."""
        hand = PlayerHand()
        for i in range(8):
            hand.add_card(Card(type=CardType.NUMBER, value=i))
        self.assertFalse(hand.has_flip_seven())

    def test_clear_resets_hand(self):
        """Test that clear() resets all hand state."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        hand.add_card(Card(type=CardType.ACTION, action_type=ActionType.FREEZE))

        hand.clear()

        self.assertEqual(len(hand.number_cards), 0)
        self.assertEqual(len(hand.modifiers), 0)
        self.assertEqual(len(hand.action_cards), 0)
        self.assertFalse(hand.second_chance_available)
        self.assertFalse(hand.is_frozen)
        self.assertFalse(hand.has_busted)

    def test_use_second_chance_without_available_raises_error(self):
        """Test that using Second Chance without it raises error."""
        hand = PlayerHand()
        card = Card(type=CardType.NUMBER, value=5)
        with self.assertRaises(ValueError):
            hand.use_second_chance(card)

    def test_use_second_chance_on_non_number_card_raises_error(self):
        """Test that Second Chance can only be used on number cards."""
        hand = PlayerHand()
        hand.second_chance_available = True
        card = Card(
            type=CardType.MODIFIER, modifier_type=ModifierType.PLUS_4, modifier_value=4
        )
        with self.assertRaises(ValueError):
            hand.use_second_chance(card)

    def test_use_second_chance_on_card_not_in_hand_raises_error(self):
        """Test that Second Chance can only be used on cards in hand."""
        hand = PlayerHand()
        hand.second_chance_available = True
        card = Card(type=CardType.NUMBER, value=5)
        with self.assertRaises(ValueError):
            hand.use_second_chance(card)


if __name__ == "__main__":
    unittest.main()

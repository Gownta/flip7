"""Unit tests for deck.py"""

import unittest
from src.deck import Deck
from src.card import CardType, ActionType, ModifierType


class TestDeck(unittest.TestCase):
    """Test Deck creation and operations."""

    def test_deck_has_94_cards(self):
        """Test that deck has exactly 94 cards."""
        deck = Deck()
        self.assertEqual(deck.cards_remaining(), 94)

    def test_deck_composition(self):
        """
        Test that deck has correct card composition.

        Number cards: 0(x1), 1(x1), 2(x2), 3(x3), ..., 12(x12) = 79 cards
        Modifiers: +2, +4, +6, +8, +10, X2 = 6 cards
        Actions: 3x Freeze, 3x Flip Three, 3x Second Chance = 9 cards
        """
        deck = Deck()
        cards = deck._original_cards

        number_counts = {}
        modifier_counts = {}
        action_counts = {}

        for card in cards:
            if card.type == CardType.NUMBER:
                number_counts[card.value] = number_counts.get(card.value, 0) + 1
            elif card.type == CardType.MODIFIER:
                modifier_counts[card.modifier_type] = (
                    modifier_counts.get(card.modifier_type, 0) + 1
                )
            elif card.type == CardType.ACTION:
                action_counts[card.action_type] = (
                    action_counts.get(card.action_type, 0) + 1
                )

        for i in range(13):
            if i == 0 or i == 1:
                self.assertEqual(number_counts.get(i, 0), 1, f"Number {i} count wrong")
            else:
                self.assertEqual(number_counts.get(i, 0), i, f"Number {i} count wrong")

        self.assertEqual(modifier_counts.get(ModifierType.PLUS_2, 0), 1)
        self.assertEqual(modifier_counts.get(ModifierType.PLUS_4, 0), 1)
        self.assertEqual(modifier_counts.get(ModifierType.PLUS_6, 0), 1)
        self.assertEqual(modifier_counts.get(ModifierType.PLUS_8, 0), 1)
        self.assertEqual(modifier_counts.get(ModifierType.PLUS_10, 0), 1)
        self.assertEqual(modifier_counts.get(ModifierType.TIMES_2, 0), 1)

        self.assertEqual(action_counts.get(ActionType.FREEZE, 0), 3)
        self.assertEqual(action_counts.get(ActionType.FLIP_THREE, 0), 3)
        self.assertEqual(action_counts.get(ActionType.SECOND_CHANCE, 0), 3)

    def test_draw_reduces_deck_size(self):
        """Test that drawing cards reduces deck size."""
        deck = Deck()
        initial_count = deck.cards_remaining()
        deck.draw()
        self.assertEqual(deck.cards_remaining(), initial_count - 1)

    def test_draw_all_cards(self):
        """Test that all 94 cards can be drawn."""
        deck = Deck()
        cards_drawn = []
        for _ in range(94):
            cards_drawn.append(deck.draw())
        self.assertEqual(len(cards_drawn), 94)
        self.assertEqual(deck.cards_remaining(), 0)

    def test_draw_from_empty_deck_raises_error(self):
        """Test that drawing from empty deck raises IndexError."""
        deck = Deck()
        for _ in range(94):
            deck.draw()
        with self.assertRaises(IndexError):
            deck.draw()

    def test_shuffle_changes_order(self):
        """Test that shuffling changes card order."""
        deck1 = Deck()
        deck2 = Deck()

        cards1 = [deck1.draw() for _ in range(94)]
        deck2.shuffle()
        cards2 = [deck2.draw() for _ in range(94)]

        self.assertNotEqual(cards1, cards2)

    def test_reset_restores_deck(self):
        """Test that reset restores full deck."""
        deck = Deck()

        for _ in range(10):
            deck.draw()
        self.assertEqual(deck.cards_remaining(), 84)

        deck.reset()
        self.assertEqual(deck.cards_remaining(), 94)

    def test_reset_shuffles_deck(self):
        """Test that reset shuffles the deck."""
        deck = Deck()
        original_order = [deck.draw() for _ in range(10)]

        deck.reset()
        new_order = [deck.draw() for _ in range(10)]

        self.assertNotEqual(original_order, new_order)


if __name__ == "__main__":
    unittest.main()

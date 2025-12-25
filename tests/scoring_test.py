"""Unit tests for scoring.py"""

import unittest
from src.scoring import calculate_score, has_times_two_modifier, get_modifier_points
from src.player_hand import PlayerHand
from src.card import Card, CardType, ModifierType


class TestScoring(unittest.TestCase):
    """Test score calculation logic."""

    def test_basic_scoring(self):
        """Test basic scoring: [5, 7, 9] = 21"""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))
        hand.add_card(Card(type=CardType.NUMBER, value=9))

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 21)

    def test_scoring_with_x2_modifier(self):
        """Test X2 modifier: [5, 7, 9], X2 = 42"""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))
        hand.add_card(Card(type=CardType.NUMBER, value=9))
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 42)

    def test_scoring_with_point_modifiers(self):
        """Test point modifiers: [5, 7, 9], +4, +8 = 33"""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))
        hand.add_card(Card(type=CardType.NUMBER, value=9))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_8,
                modifier_value=8,
            )
        )

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 33)

    def test_scoring_with_x2_and_point_modifiers(self):
        """Test X2 + point modifiers: [5, 7, 9], X2, +4, +8 = 54"""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))
        hand.add_card(Card(type=CardType.NUMBER, value=9))
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_8,
                modifier_value=8,
            )
        )

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 54)

    def test_scoring_with_flip_seven_bonus(self):
        """Test Flip 7 bonus: [1,2,3,4,5,6,7], +4 = 28 + 4 + 15 = 47"""
        hand = PlayerHand()
        for i in range(1, 8):
            hand.add_card(Card(type=CardType.NUMBER, value=i))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )

        score = calculate_score(hand, has_flip_seven_bonus=True)
        self.assertEqual(score, 47)

    def test_maximum_theoretical_score(self):
        """
        Test maximum score: [6,7,8,9,10,11,12], X2, +2, +4, +6, +8, +10, Flip 7
        = ((6+7+8+9+10+11+12)*2) + (2+4+6+8+10) + 15 = 126 + 30 + 15 = 171
        """
        hand = PlayerHand()
        for i in range(6, 13):
            hand.add_card(Card(type=CardType.NUMBER, value=i))
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_2,
                modifier_value=2,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_6,
                modifier_value=6,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_8,
                modifier_value=8,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_10,
                modifier_value=10,
            )
        )

        score = calculate_score(hand, has_flip_seven_bonus=True)
        self.assertEqual(score, 171)

    def test_bust_returns_zero(self):
        """Test that busted hands score 0."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))
        hand.has_busted = True

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 0)

    def test_bust_with_modifiers_returns_zero(self):
        """Test that busted hands score 0 even with modifiers."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_10,
                modifier_value=10,
            )
        )
        hand.has_busted = True

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 0)

    def test_has_times_two_modifier_true(self):
        """Test detection of X2 modifier."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))
        self.assertTrue(has_times_two_modifier(hand.modifiers))

    def test_has_times_two_modifier_false(self):
        """Test X2 modifier detection returns false when not present."""
        hand = PlayerHand()
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        self.assertFalse(has_times_two_modifier(hand.modifiers))

    def test_get_modifier_points_with_multiple_modifiers(self):
        """Test summing all point modifiers."""
        hand = PlayerHand()
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_2,
                modifier_value=2,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_10,
                modifier_value=10,
            )
        )

        total = get_modifier_points(hand.modifiers)
        self.assertEqual(total, 16)

    def test_get_modifier_points_excludes_x2(self):
        """Test that X2 modifier is not counted in point modifiers."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.MODIFIER, modifier_type=ModifierType.TIMES_2))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_4,
                modifier_value=4,
            )
        )

        total = get_modifier_points(hand.modifiers)
        self.assertEqual(total, 4)

    def test_zero_score_with_only_zero_card(self):
        """Test scoring with only 0 number card."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=0))

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 0)

    def test_score_with_zero_and_modifiers(self):
        """Test that 0 number card with modifiers still adds modifiers."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=0))
        hand.add_card(
            Card(
                type=CardType.MODIFIER,
                modifier_type=ModifierType.PLUS_10,
                modifier_value=10,
            )
        )

        score = calculate_score(hand, has_flip_seven_bonus=False)
        self.assertEqual(score, 10)


if __name__ == "__main__":
    unittest.main()

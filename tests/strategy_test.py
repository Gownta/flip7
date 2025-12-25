"""Unit tests for strategy.py"""

import unittest
from src.strategy import Strategy
from src.game_state import GameState
from src.card import Card, CardType, ModifierType


class TestStrategy(unittest.TestCase):
    """Test strategy calculations."""

    def test_calculate_current_score_basic(self):
        """Test current score calculation."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.add_card(Card(type=CardType.NUMBER, value=7))

        score = Strategy.calculate_current_score(hand, False)
        self.assertEqual(score, 12)

    def test_count_remaining_cards(self):
        """Test counting remaining cards in deck."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        counts = Strategy.count_remaining_cards(game_state)

        self.assertIn("numbers", counts)
        self.assertIn("modifiers", counts)
        self.assertIn("actions", counts)

        total_numbers = sum(counts["numbers"].values())
        self.assertEqual(total_numbers, 79)

    def test_recommend_action_empty_hand(self):
        """Test recommendation with empty hand (should hit)."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        recommendation, details = Strategy.recommend_action(game_state, 0)

        self.assertEqual(recommendation, "HIT")
        self.assertIn("current_score", details)
        self.assertIn("ev_hit", details)

    def test_recommend_action_flip_seven(self):
        """Test recommendation with Flip 7 (should stay)."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        for i in range(7):
            hand.add_card(Card(type=CardType.NUMBER, value=i))

        recommendation, details = Strategy.recommend_action(game_state, 0)

        self.assertEqual(recommendation, "STAY")
        self.assertIn("Flip 7", details["reason"])

    def test_recommend_action_frozen(self):
        """Test recommendation when frozen (should stay)."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.is_frozen = True

        recommendation, details = Strategy.recommend_action(game_state, 0)

        self.assertEqual(recommendation, "STAY")
        self.assertIn("frozen", details["reason"])

    def test_bust_probability_no_cards(self):
        """Test bust probability with no cards (should be 0)."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        bust_prob = Strategy._calculate_bust_probability(game_state, 0)

        self.assertEqual(bust_prob, 0.0)

    def test_bust_probability_with_cards(self):
        """Test bust probability increases with more cards."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        bust_prob = Strategy._calculate_bust_probability(game_state, 0)

        self.assertGreater(bust_prob, 0.0)
        self.assertLessEqual(bust_prob, 1.0)

    def test_bust_probability_with_second_chance(self):
        """Test that Second Chance reduces bust probability to 0."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))
        hand.second_chance_available = True

        bust_prob = Strategy._calculate_bust_probability(game_state, 0)

        self.assertEqual(bust_prob, 0.0)

    def test_bust_probability_increases_with_cards(self):
        """Test that bust probability increases as more cards are collected."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)

        bust_prob_initial = Strategy._calculate_bust_probability(game_state, 0)

        for i in range(6):
            hand.add_card(Card(type=CardType.NUMBER, value=i))

        bust_prob_risky = Strategy._calculate_bust_probability(game_state, 0)

        self.assertGreater(bust_prob_risky, bust_prob_initial)

    def test_simulate_add_number(self):
        """Test simulating adding a number card."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        new_hand = Strategy._simulate_add_number(hand, 7)

        self.assertIn(5, new_hand.number_cards)
        self.assertIn(7, new_hand.number_cards)
        self.assertNotIn(7, hand.number_cards)

    def test_simulate_add_modifier(self):
        """Test simulating adding a modifier card."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        new_hand = Strategy._simulate_add_modifier(hand, ModifierType.PLUS_4)

        self.assertEqual(len(new_hand.modifiers), 1)
        self.assertEqual(len(hand.modifiers), 0)

    def test_recommendation_details_include_bust_probability(self):
        """Test that recommendation includes bust probability."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.get_player_hand(0)
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        _, details = Strategy.recommend_action(game_state, 0)

        self.assertIn("bust_probability", details)
        self.assertIsInstance(details["bust_probability"], (int, float))


if __name__ == "__main__":
    unittest.main()

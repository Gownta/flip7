"""Unit tests for game_state.py"""

import unittest
from src.game_state import GameState
from src.card import Card, CardType


class TestGameState(unittest.TestCase):
    """Test game state management."""

    def test_initialization(self):
        """Test GameState initialization."""
        game_state = GameState(num_players=2)
        self.assertEqual(len(game_state.players), 2)
        self.assertFalse(game_state.flip_seven_claimed)
        self.assertIsNone(game_state.flip_seven_player_idx)
        self.assertFalse(game_state.round_active)

    def test_start_round_resets_state(self):
        """Test that start_round resets all state."""
        game_state = GameState(num_players=2)
        game_state.flip_seven_claimed = True
        game_state.flip_seven_player_idx = 0

        game_state.start_round()

        self.assertFalse(game_state.flip_seven_claimed)
        self.assertIsNone(game_state.flip_seven_player_idx)
        self.assertTrue(game_state.round_active)
        self.assertEqual(game_state.deck.cards_remaining(), 94)

    def test_start_round_clears_player_hands(self):
        """Test that start_round clears all player hands."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        while len(game_state.players[0].number_cards) == 0:
            if game_state.deck.cards_remaining() == 0:
                break
            game_state.draw_card(0)

        while len(game_state.players[1].number_cards) == 0:
            if game_state.deck.cards_remaining() == 0:
                break
            game_state.draw_card(1)

        self.assertGreater(len(game_state.players[0].number_cards), 0)
        self.assertGreater(len(game_state.players[1].number_cards), 0)

        game_state.start_round()

        self.assertEqual(len(game_state.players[0].number_cards), 0)
        self.assertEqual(len(game_state.players[1].number_cards), 0)

    def test_draw_card_returns_card_and_result(self):
        """Test that draw_card returns both card and result."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        card, result = game_state.draw_card(0)

        self.assertIsNotNone(card)
        self.assertIsNotNone(result)

    def test_draw_card_reduces_deck(self):
        """Test that drawing cards reduces deck size."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        initial_count = game_state.deck.cards_remaining()
        game_state.draw_card(0)

        self.assertEqual(game_state.deck.cards_remaining(), initial_count - 1)

    def test_draw_card_when_frozen_raises_error(self):
        """Test that frozen players cannot draw."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        game_state.players[0].is_frozen = True

        with self.assertRaises(ValueError):
            game_state.draw_card(0)

    def test_draw_card_when_busted_raises_error(self):
        """Test that busted players cannot draw."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        game_state.players[0].has_busted = True

        with self.assertRaises(ValueError):
            game_state.draw_card(0)

    def test_draw_card_when_round_inactive_raises_error(self):
        """Test that cards cannot be drawn when round is inactive."""
        game_state = GameState(num_players=1)

        with self.assertRaises(ValueError):
            game_state.draw_card(0)

    def test_flip_seven_claims_bonus(self):
        """Test that first player to reach 7 unique numbers claims Flip 7."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        for i in range(7):
            game_state.players[0].add_card(Card(type=CardType.NUMBER, value=i))
            if (
                game_state.players[0].has_flip_seven()
                and not game_state.flip_seven_claimed
            ):
                game_state.flip_seven_claimed = True
                game_state.flip_seven_player_idx = 0
                game_state.round_active = False

        self.assertTrue(game_state.players[0].has_flip_seven())
        self.assertTrue(game_state.flip_seven_claimed)
        self.assertEqual(game_state.flip_seven_player_idx, 0)

    def test_flip_seven_ends_round(self):
        """Test that Flip 7 ends the round."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        for i in range(7):
            game_state.players[0].add_card(Card(type=CardType.NUMBER, value=i))
            if (
                game_state.players[0].has_flip_seven()
                and not game_state.flip_seven_claimed
            ):
                game_state.flip_seven_claimed = True
                game_state.flip_seven_player_idx = 0
                game_state.round_active = False

        self.assertFalse(game_state.round_active)

    def test_flip_seven_only_first_player_gets_bonus(self):
        """Test that only the first player to reach 7 gets the bonus."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        for i in range(7):
            game_state.players[0].add_card(Card(type=CardType.NUMBER, value=i))
            if (
                game_state.players[0].has_flip_seven()
                and not game_state.flip_seven_claimed
            ):
                game_state.flip_seven_claimed = True
                game_state.flip_seven_player_idx = 0
                game_state.round_active = False

        self.assertEqual(game_state.flip_seven_player_idx, 0)

        for i in range(7):
            game_state.players[1].add_card(Card(type=CardType.NUMBER, value=i))

        self.assertEqual(game_state.flip_seven_player_idx, 0)

    def test_end_round_calculates_scores(self):
        """Test that end_round calculates scores for all players."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        game_state.players[0].add_card(Card(type=CardType.NUMBER, value=5))
        game_state.players[1].add_card(Card(type=CardType.NUMBER, value=7))

        scores = game_state.end_round()

        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[0], 5)
        self.assertEqual(scores[1], 7)

    def test_end_round_gives_flip_seven_bonus(self):
        """Test that Flip 7 bonus is awarded correctly."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        for i in range(7):
            game_state.players[0].add_card(Card(type=CardType.NUMBER, value=i))

        game_state.flip_seven_player_idx = 0

        for i in range(7, 12):
            game_state.players[1].add_card(Card(type=CardType.NUMBER, value=i))

        scores = game_state.end_round()

        expected_p0 = sum(range(7)) + 15
        expected_p1 = sum(range(7, 12))

        self.assertEqual(scores[0], expected_p0)
        self.assertEqual(scores[1], expected_p1)

    def test_is_round_over_when_flip_seven_claimed(self):
        """Test that round is over when Flip 7 is claimed."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        game_state.flip_seven_claimed = True

        self.assertTrue(game_state.is_round_over())

    def test_is_round_over_when_all_players_done(self):
        """Test that round is over when all players are frozen or busted."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        game_state.players[0].is_frozen = True
        game_state.players[1].has_busted = True

        self.assertTrue(game_state.is_round_over())

    def test_is_round_not_over_when_players_active(self):
        """Test that round is not over when players can still play."""
        game_state = GameState(num_players=2)
        game_state.start_round()

        game_state.players[0].is_frozen = True

        self.assertFalse(game_state.is_round_over())

    def test_get_player_hand(self):
        """Test getting a player's hand."""
        game_state = GameState(num_players=2)
        hand = game_state.get_player_hand(0)
        self.assertIsNotNone(hand)
        self.assertIs(hand, game_state.players[0])

    def test_get_player_hand_invalid_index(self):
        """Test that invalid player index raises error."""
        game_state = GameState(num_players=2)

        with self.assertRaises(ValueError):
            game_state.get_player_hand(5)

        with self.assertRaises(ValueError):
            game_state.get_player_hand(-1)


if __name__ == "__main__":
    unittest.main()

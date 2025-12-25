"""Unit tests for action_handler.py"""

import unittest
from src.action_handler import ActionHandler
from src.game_state import GameState
from src.player_hand import PlayerHand, AddCardResult
from src.card import Card, CardType, ActionType


class TestActionHandler(unittest.TestCase):
    """Test action card handling."""

    def test_handle_freeze(self):
        """Test that Freeze action freezes the hand."""
        hand = PlayerHand()
        ActionHandler.handle_freeze(hand)
        self.assertTrue(hand.is_frozen)

    def test_handle_second_chance_success(self):
        """Test successful Second Chance usage."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.ACTION, action_type=ActionType.SECOND_CHANCE))
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        duplicate = Card(type=CardType.NUMBER, value=5)
        success = ActionHandler.handle_second_chance(hand, duplicate)

        self.assertTrue(success)
        self.assertFalse(hand.second_chance_available)

    def test_handle_second_chance_not_available(self):
        """Test Second Chance when not available."""
        hand = PlayerHand()
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        duplicate = Card(type=CardType.NUMBER, value=5)
        success = ActionHandler.handle_second_chance(hand, duplicate)

        self.assertFalse(success)

    def test_handle_flip_three_draws_three_cards(self):
        """Test that Flip Three draws exactly 3 cards when available."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        results = ActionHandler.handle_flip_three(game_state, 0)

        self.assertEqual(len(results), 3)

    def test_handle_flip_three_draws_remaining_cards(self):
        """Test Flip Three when fewer than 3 cards remain."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        for _ in range(92):
            game_state.deck.draw()

        self.assertEqual(game_state.deck.cards_remaining(), 2)

        results = ActionHandler.handle_flip_three(game_state, 0)

        self.assertEqual(len(results), 2)

    def test_handle_flip_three_stops_on_bust(self):
        """Test that Flip Three stops drawing if player busts."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        hand = game_state.players[0]
        hand.add_card(Card(type=CardType.NUMBER, value=5))

        original_deck = game_state.deck._cards.copy()
        for i in range(len(original_deck)):
            if original_deck[-(i + 1)].type == CardType.NUMBER:
                if original_deck[-(i + 1)].value == 5:
                    duplicate_idx = len(original_deck) - (i + 1)
                    if duplicate_idx > 0:
                        original_deck[-1], original_deck[duplicate_idx] = (
                            original_deck[duplicate_idx],
                            original_deck[-1],
                        )
                    break
        game_state.deck._cards = original_deck

        results = ActionHandler.handle_flip_three(game_state, 0)

        self.assertIn(AddCardResult.BUST, results)
        self.assertTrue(any(r == AddCardResult.BUST for r in results))

    def test_handle_flip_three_stops_on_freeze(self):
        """Test that Flip Three stops drawing if Freeze is drawn."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        original_deck = game_state.deck._cards.copy()
        freeze_card = Card(type=CardType.ACTION, action_type=ActionType.FREEZE)

        for i in range(len(original_deck)):
            if (
                original_deck[-(i + 1)].type == CardType.ACTION
                and original_deck[-(i + 1)].action_type == ActionType.FREEZE
            ):
                freeze_idx = len(original_deck) - (i + 1)
                if freeze_idx > 0:
                    original_deck[-1], original_deck[freeze_idx] = (
                        original_deck[freeze_idx],
                        original_deck[-1],
                    )
                break
        game_state.deck._cards = original_deck

        results = ActionHandler.handle_flip_three(game_state, 0)

        self.assertTrue(game_state.players[0].is_frozen)


if __name__ == "__main__":
    unittest.main()

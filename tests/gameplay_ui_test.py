"""Unit tests for gameplay UI functions."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from src.gameplay_ui import (
    get_hand_text,
    get_card_drawn_text,
    get_recommendation_text,
    get_bust_text,
    get_duplicate_prompt_text,
    get_second_chance_prompt,
    get_second_chance_used_text,
    get_freeze_text,
    get_flip_three_text,
    get_flip_seven_text,
    get_round_header_text,
    get_round_start_text,
    get_round_complete_text,
    get_game_welcome_text,
    get_game_complete_text,
    display_hand,
    display_card_drawn,
    display_recommendation,
    handle_draw,
    play_round,
)
from src.game_state import GameState
from src.card import Card, CardType, ModifierType, ActionType
from src.player_hand import AddCardResult


class TestGetterFunctions(unittest.TestCase):
    """Test getter functions return correct text."""

    def test_get_hand_text_with_numbers(self):
        """Test getting hand text with number cards."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards = {1, 3, 5}

        text = get_hand_text(game_state, 0)
        self.assertIn("YOUR HAND", text)
        self.assertIn("[1, 3, 5]", text)
        self.assertIn("Base score: 9", text)

    def test_get_hand_text_empty(self):
        """Test getting hand text with empty hand."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        text = get_hand_text(game_state, 0)
        self.assertIn("YOUR HAND", text)
        self.assertIn("(none)", text)

    def test_get_card_drawn_text(self):
        """Test getting card drawn text."""
        card = Card(CardType.NUMBER, value=5)
        text = get_card_drawn_text(card)
        self.assertIn("You drew:", text)
        self.assertIn("5", text)

    def test_get_recommendation_text(self):
        """Test getting recommendation text."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        text = get_recommendation_text(game_state, 0)
        self.assertIn("STRATEGY RECOMMENDATION", text)
        self.assertIn("Recommendation:", text)

    def test_get_bust_text(self):
        """Test getting bust text."""
        text = get_bust_text()
        self.assertIn("BUST", text)
        self.assertIn("duplicate", text)

    def test_get_duplicate_prompt_text(self):
        """Test getting duplicate prompt text."""
        text = get_duplicate_prompt_text()
        self.assertIn("Duplicate", text)

    def test_get_second_chance_prompt(self):
        """Test getting Second Chance prompt."""
        text = get_second_chance_prompt()
        self.assertIn("Second Chance", text)
        self.assertIn("(y/n)", text)

    def test_get_second_chance_used_text(self):
        """Test getting Second Chance used text."""
        text = get_second_chance_used_text()
        self.assertIn("Second Chance used", text)

    def test_get_freeze_text(self):
        """Test getting freeze text."""
        text = get_freeze_text()
        self.assertIn("FREEZE", text)

    def test_get_flip_three_text(self):
        """Test getting Flip Three text."""
        text = get_flip_three_text()
        self.assertIn("FLIP THREE", text)

    def test_get_flip_seven_text(self):
        """Test getting Flip 7 text."""
        text = get_flip_seven_text()
        self.assertIn("FLIP 7", text)
        self.assertIn("7 unique numbers", text)

    def test_get_round_header_text(self):
        """Test getting round header text."""
        text = get_round_header_text(5, 100)
        self.assertIn("ROUND 5", text)
        self.assertIn("100/200", text)

    def test_get_round_start_text(self):
        """Test getting round start text."""
        text = get_round_start_text()
        self.assertIn("NEW ROUND STARTING", text)

    def test_get_round_complete_text(self):
        """Test getting round complete text."""
        text = get_round_complete_text(42)
        self.assertIn("ROUND COMPLETE", text)
        self.assertIn("42", text)

    def test_get_game_welcome_text(self):
        """Test getting game welcome text."""
        text = get_game_welcome_text()
        self.assertIn("WELCOME TO FLIP 7", text)
        self.assertIn("200 points", text)

    def test_get_game_complete_text(self):
        """Test getting game complete text."""
        text = get_game_complete_text(215, 8)
        self.assertIn("CONGRATULATIONS", text)
        self.assertIn("215", text)
        self.assertIn("8 rounds", text)


class TestDisplayFunctions(unittest.TestCase):
    """Test display functions output correctly."""

    def test_display_hand_with_numbers(self):
        """Test displaying a hand with number cards."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards = [1, 3, 5]

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_hand(game_state, 0)
            output = fake_out.getvalue()
            self.assertIn("YOUR HAND", output)
            self.assertIn("[1, 3, 5]", output)
            self.assertIn("Base score: 9", output)

    def test_display_hand_empty(self):
        """Test displaying an empty hand."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_hand(game_state, 0)
            output = fake_out.getvalue()
            self.assertIn("YOUR HAND", output)
            self.assertIn("(none)", output)

    def test_display_card_drawn(self):
        """Test displaying a drawn card."""
        card = Card(CardType.NUMBER, value=5)

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_card_drawn(card)
            output = fake_out.getvalue()
            self.assertIn("You drew:", output)

    def test_display_recommendation(self):
        """Test displaying strategy recommendation."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        with patch("sys.stdout", new=StringIO()) as fake_out:
            display_recommendation(game_state, 0)
            output = fake_out.getvalue()
            self.assertIn("STRATEGY RECOMMENDATION", output)
            self.assertIn("Recommendation:", output)


class TestHandleDraw(unittest.TestCase):
    """Test handle_draw function."""

    @patch("builtins.print")
    def test_handle_draw_normal_card(self, mock_print):
        """Test drawing a normal card."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        card_to_draw = Card(CardType.NUMBER, value=3)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertTrue(result)
        hand = game_state.get_player_hand(0)
        self.assertIn(3, hand.number_cards)

    @patch("builtins.print")
    def test_handle_draw_bust(self, mock_print):
        """Test drawing a duplicate card causes bust."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards.add(5)

        card_to_draw = Card(CardType.NUMBER, value=5)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertFalse(result)

    @patch("builtins.print")
    @patch("builtins.input", return_value="y")
    def test_handle_draw_second_chance_used(self, mock_input, mock_print):
        """Test using Second Chance on duplicate."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards.add(5)
        hand.add_card(Card(CardType.ACTION, action_type=ActionType.SECOND_CHANCE))

        card_to_draw = Card(CardType.NUMBER, value=5)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertTrue(result)
        self.assertEqual(len(hand.action_cards), 0)

    @patch("builtins.print")
    @patch("builtins.input", return_value="n")
    def test_handle_draw_second_chance_declined(self, mock_input, mock_print):
        """Test declining Second Chance on duplicate."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards.add(5)
        hand.add_card(Card(CardType.ACTION, action_type=ActionType.SECOND_CHANCE))

        card_to_draw = Card(CardType.NUMBER, value=5)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertFalse(result)
        self.assertTrue(hand.has_busted)

    @patch("builtins.print")
    def test_handle_draw_frozen(self, mock_print):
        """Test drawing a freeze card."""
        game_state = GameState(num_players=1)
        game_state.start_round()

        card_to_draw = Card(CardType.ACTION, action_type=ActionType.FREEZE)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertFalse(result)

    @patch("builtins.print")
    def test_handle_draw_flip_seven(self, mock_print):
        """Test achieving Flip 7."""
        game_state = GameState(num_players=1)
        game_state.start_round()
        hand = game_state.get_player_hand(0)
        hand.number_cards = {1, 2, 3, 4, 5, 6}

        card_to_draw = Card(CardType.NUMBER, value=7)
        game_state.deck._cards = [card_to_draw]

        result = handle_draw(game_state, 0)
        self.assertFalse(result)
        self.assertTrue(hand.has_flip_seven())


class TestPlayRound(unittest.TestCase):
    """Test play_round function."""

    @patch("builtins.print")
    @patch("builtins.input", return_value="s")
    def test_play_round_immediate_stay(self, mock_input, mock_print):
        """Test playing a round and staying immediately."""
        game_state = GameState(num_players=1)
        score = play_round(game_state)
        self.assertEqual(score, 0)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["h", "s"])
    @patch("src.deck.Deck.draw")
    def test_play_round_hit_then_stay(self, mock_draw, mock_input, mock_print):
        """Test playing a round with one hit then stay."""
        game_state = GameState(num_players=1)

        card_to_draw = Card(CardType.NUMBER, value=5)
        mock_draw.return_value = card_to_draw

        score = play_round(game_state)
        self.assertEqual(score, 5)


if __name__ == "__main__":
    unittest.main()

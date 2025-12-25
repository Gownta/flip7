"""
Game state management for Flip 7.

Handles round management, turn progression, and game rules enforcement.
"""

from typing import List, Optional, Dict
from src.deck import Deck
from src.player_hand import PlayerHand, AddCardResult
from src.scoring import calculate_score
from src.card import Card


class GameState:
    """
    Manages the overall game state for a round of Flip 7.

    Tracks the deck, player hands, and round-level state like Flip 7 claiming.
    """

    def __init__(self, num_players: int = 1):
        """
        Initialize a new game state.

        Args:
            num_players: Number of players in the game
        """
        self.deck = Deck()
        self.players: List[PlayerHand] = [PlayerHand() for _ in range(num_players)]
        self.flip_seven_claimed = False
        self.flip_seven_player_idx: Optional[int] = None
        self.round_active = False

    def start_round(self) -> None:
        """
        Start a new round.

        Resets all player hands, shuffles the deck, and resets round state.
        """
        for player in self.players:
            player.clear()

        self.deck.reset()
        self.flip_seven_claimed = False
        self.flip_seven_player_idx = None
        self.round_active = True

    def draw_card(self, player_idx: int) -> tuple[Card, AddCardResult]:
        """
        Draw a card for a player.

        Args:
            player_idx: Index of the player drawing

        Returns:
            Tuple of (card drawn, result of adding the card)
        """
        if not self.round_active:
            raise ValueError("Round is not active")

        if player_idx < 0 or player_idx >= len(self.players):
            raise ValueError(f"Invalid player index: {player_idx}")

        hand = self.players[player_idx]
        if hand.is_frozen:
            raise ValueError("Player is frozen and cannot draw")

        if hand.has_busted:
            raise ValueError("Player has busted and cannot draw")

        card = self.deck.draw()
        result = hand.add_card(card)

        if hand.has_flip_seven() and not self.flip_seven_claimed:
            self.flip_seven_claimed = True
            self.flip_seven_player_idx = player_idx
            self.round_active = False

        return card, result

    def end_round(self) -> Dict[int, int]:
        """
        End the round and calculate scores for all players.

        Returns:
            Dictionary mapping player index to score
        """
        scores = {}
        for idx, hand in enumerate(self.players):
            has_flip_seven_bonus = idx == self.flip_seven_player_idx
            scores[idx] = calculate_score(hand, has_flip_seven_bonus)

        self.round_active = False
        return scores

    def is_round_over(self) -> bool:
        """
        Check if the round is over.

        Round ends when:
        - Someone claims Flip 7
        - All players are frozen or busted

        Returns:
            True if round should end
        """
        if self.flip_seven_claimed:
            return True

        all_done = all(player.is_frozen or player.has_busted for player in self.players)
        return all_done

    def get_player_hand(self, player_idx: int) -> PlayerHand:
        """
        Get a player's hand.

        Args:
            player_idx: Index of the player

        Returns:
            The player's hand
        """
        if player_idx < 0 or player_idx >= len(self.players):
            raise ValueError(f"Invalid player index: {player_idx}")
        return self.players[player_idx]

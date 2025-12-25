"""
Action card handling for Flip 7 game.

Handles special action card effects during gameplay.
"""

from typing import List, TYPE_CHECKING
from src.card import Card, ActionType
from src.player_hand import PlayerHand, AddCardResult

if TYPE_CHECKING:
    from src.game_state import GameState


class ActionHandler:
    """Handles execution of action card effects."""

    @staticmethod
    def handle_freeze(hand: PlayerHand) -> None:
        """
        Handle Freeze action card.

        Forces the player to bank their current points and stop drawing.

        Args:
            hand: The player's hand
        """
        hand.is_frozen = True

    @staticmethod
    def handle_flip_three(
        game_state: "GameState", player_idx: int
    ) -> List[AddCardResult]:
        """
        Handle Flip Three action card.

        Draws 3 cards or all remaining cards if fewer than 3 remain.

        Args:
            game_state: The current game state
            player_idx: Index of the player

        Returns:
            List of results from adding each card
        """
        results = []
        cards_to_draw = min(3, game_state.deck.cards_remaining())

        for _ in range(cards_to_draw):
            if game_state.deck.cards_remaining() > 0:
                card = game_state.deck.draw()
                hand = game_state.players[player_idx]

                if card.action_type == ActionType.FLIP_THREE:
                    results.append(
                        ActionHandler.handle_flip_three(game_state, player_idx)
                    )
                elif card.action_type == ActionType.FREEZE:
                    result = hand.add_card(card)
                    results.append(result)
                    break
                else:
                    result = hand.add_card(card)
                    results.append(result)

                    if (
                        result == AddCardResult.BUST
                        or result == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE
                    ):
                        break

        return results

    @staticmethod
    def handle_second_chance(hand: PlayerHand, duplicate_card: Card) -> bool:
        """
        Handle Second Chance action card.

        Allows player to discard a duplicate number card to avoid busting.

        Args:
            hand: The player's hand
            duplicate_card: The duplicate card that was drawn

        Returns:
            True if Second Chance was successfully used
        """
        if not hand.second_chance_available:
            return False

        try:
            hand.use_second_chance(duplicate_card)
            return True
        except ValueError:
            return False

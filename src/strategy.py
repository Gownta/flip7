"""
Optimal strategy calculator for Flip 7.

Calculates expected values to recommend hit/stay decisions.
"""

from typing import Dict, Tuple
from src.game_state import GameState
from src.card import Card, CardType, ActionType, ModifierType
from src.scoring import calculate_score
from src.player_hand import PlayerHand


class Strategy:
    """Calculates optimal play decisions based on expected value."""

    @staticmethod
    def calculate_current_score(hand: PlayerHand, has_flip_seven_bonus: bool) -> int:
        """
        Calculate what the current hand would score if we stay now.

        Args:
            hand: The player's hand
            has_flip_seven_bonus: Whether player would get Flip 7 bonus

        Returns:
            Current score if staying
        """
        return calculate_score(hand, has_flip_seven_bonus)

    @staticmethod
    def count_remaining_cards(game_state: GameState) -> Dict[str, int]:
        """
        Count remaining cards in the deck by type.

        Returns:
            Dictionary with counts of each card type/value
        """
        counts = {
            "numbers": {},
            "modifiers": {},
            "actions": {},
        }

        for card in game_state.deck._cards:
            if card.type == CardType.NUMBER:
                counts["numbers"][card.value] = counts["numbers"].get(card.value, 0) + 1
            elif card.type == CardType.MODIFIER:
                counts["modifiers"][card.modifier_type] = (
                    counts["modifiers"].get(card.modifier_type, 0) + 1
                )
            elif card.type == CardType.ACTION:
                counts["actions"][card.action_type] = (
                    counts["actions"].get(card.action_type, 0) + 1
                )

        return counts

    @staticmethod
    def calculate_expected_value_of_hit(
        game_state: GameState, player_idx: int = 0
    ) -> float:
        """
        Calculate expected value of drawing one more card.

        Uses one-step lookahead: assumes we stay after drawing.

        Args:
            game_state: Current game state
            player_idx: Player index

        Returns:
            Expected value of hitting
        """
        hand = game_state.get_player_hand(player_idx)

        if hand.is_frozen or hand.has_busted:
            return 0.0

        cards_remaining = game_state.deck.cards_remaining()
        if cards_remaining == 0:
            return 0.0

        counts = Strategy.count_remaining_cards(game_state)
        total_ev = 0.0

        for number, count in counts["numbers"].items():
            prob = count / cards_remaining

            if number in hand.number_cards:
                if hand.second_chance_available:
                    total_ev += prob * Strategy.calculate_current_score(
                        hand, hand.has_flip_seven()
                    )
                else:
                    total_ev += prob * 0
            else:
                temp_hand = Strategy._simulate_add_number(hand, number)
                score = Strategy.calculate_current_score(
                    temp_hand, temp_hand.has_flip_seven()
                )
                if temp_hand.has_flip_seven():
                    score += 15
                total_ev += prob * score

        for mod_type, count in counts["modifiers"].items():
            prob = count / cards_remaining
            temp_hand = Strategy._simulate_add_modifier(hand, mod_type)
            score = Strategy.calculate_current_score(temp_hand, hand.has_flip_seven())
            total_ev += prob * score

        for action_type, count in counts["actions"].items():
            prob = count / cards_remaining

            if action_type == ActionType.FREEZE:
                score = Strategy.calculate_current_score(hand, hand.has_flip_seven())
                total_ev += prob * score
            elif action_type == ActionType.SECOND_CHANCE:
                score = Strategy.calculate_current_score(hand, hand.has_flip_seven())
                total_ev += prob * score
            elif action_type == ActionType.FLIP_THREE:
                ev_flip_three = Strategy._estimate_flip_three_ev(game_state, player_idx)
                total_ev += prob * ev_flip_three

        return total_ev

    @staticmethod
    def _simulate_add_number(hand: PlayerHand, number: int) -> PlayerHand:
        """Create a simulated hand with an additional number card."""
        new_hand = PlayerHand()
        new_hand.number_cards = hand.number_cards.copy()
        new_hand.modifiers = hand.modifiers.copy()
        new_hand.action_cards = hand.action_cards.copy()
        new_hand.second_chance_available = hand.second_chance_available
        new_hand.is_frozen = hand.is_frozen
        new_hand.has_busted = hand.has_busted

        new_hand.number_cards.add(number)
        return new_hand

    @staticmethod
    def _simulate_add_modifier(hand: PlayerHand, mod_type: ModifierType) -> PlayerHand:
        """Create a simulated hand with an additional modifier card."""
        new_hand = PlayerHand()
        new_hand.number_cards = hand.number_cards.copy()
        new_hand.modifiers = hand.modifiers.copy()
        new_hand.action_cards = hand.action_cards.copy()
        new_hand.second_chance_available = hand.second_chance_available
        new_hand.is_frozen = hand.is_frozen
        new_hand.has_busted = hand.has_busted

        mod_value_map = {
            ModifierType.PLUS_2: 2,
            ModifierType.PLUS_4: 4,
            ModifierType.PLUS_6: 6,
            ModifierType.PLUS_8: 8,
            ModifierType.PLUS_10: 10,
            ModifierType.TIMES_2: 0,
        }

        mod_card = Card(
            type=CardType.MODIFIER,
            modifier_type=mod_type,
            modifier_value=mod_value_map.get(mod_type, 0),
        )
        new_hand.modifiers.append(mod_card)
        return new_hand

    @staticmethod
    def _estimate_flip_three_ev(game_state: GameState, player_idx: int) -> float:
        """
        Estimate expected value of Flip Three action.

        Simplified: assume average outcome of drawing 3 cards.
        """
        hand = game_state.get_player_hand(player_idx)
        cards_remaining = game_state.deck.cards_remaining()

        if cards_remaining <= 1:
            return Strategy.calculate_current_score(hand, hand.has_flip_seven())

        total_bust_prob = 0.0
        total_value = 0.0
        draws = min(3, cards_remaining)

        temp_numbers = hand.number_cards.copy()
        temp_value = sum(temp_numbers)

        for _ in range(draws):
            counts = Strategy.count_remaining_cards(game_state)
            remaining = game_state.deck.cards_remaining()

            if remaining == 0:
                break

            bust_prob_this_draw = (
                sum(
                    count
                    for num, count in counts["numbers"].items()
                    if num in temp_numbers
                )
                / remaining
            )

            if hand.second_chance_available and total_bust_prob == 0:
                bust_prob_this_draw = 0
                hand.second_chance_available = False

            total_bust_prob += bust_prob_this_draw * (1 - total_bust_prob)

            if total_bust_prob >= 1.0:
                return 0.0

            avg_number = 6.5
            temp_value += avg_number * 0.5

        if total_bust_prob >= 0.8:
            return 0.0

        return temp_value * (1 - total_bust_prob)

    @staticmethod
    def recommend_action(
        game_state: GameState, player_idx: int = 0
    ) -> Tuple[str, dict]:
        """
        Recommend whether to hit or stay.

        Args:
            game_state: Current game state
            player_idx: Player index

        Returns:
            Tuple of (recommendation, details) where:
                - recommendation is "HIT" or "STAY"
                - details is a dict with EV calculations
        """
        hand = game_state.get_player_hand(player_idx)

        if hand.is_frozen or hand.has_busted:
            return "STAY", {"reason": "Cannot continue (frozen or busted)"}

        current_score = Strategy.calculate_current_score(hand, hand.has_flip_seven())
        ev_hit = Strategy.calculate_expected_value_of_hit(game_state, player_idx)

        details = {
            "current_score": current_score,
            "ev_hit": round(ev_hit, 2),
            "ev_stay": current_score,
            "cards_remaining": game_state.deck.cards_remaining(),
        }

        bust_prob = Strategy._calculate_bust_probability(game_state, player_idx)
        details["bust_probability"] = round(bust_prob * 100, 1)

        if hand.has_flip_seven():
            return "STAY", {**details, "reason": "Flip 7 achieved - take the bonus!"}

        if ev_hit > current_score:
            recommendation = "HIT"
            details["advantage"] = round(ev_hit - current_score, 2)
        else:
            recommendation = "STAY"
            details["advantage"] = round(current_score - ev_hit, 2)

        return recommendation, details

    @staticmethod
    def _calculate_bust_probability(game_state: GameState, player_idx: int) -> float:
        """
        Calculate probability of busting on next draw.

        Args:
            game_state: Current game state
            player_idx: Player index

        Returns:
            Probability of busting (0.0 to 1.0)
        """
        hand = game_state.get_player_hand(player_idx)
        cards_remaining = game_state.deck.cards_remaining()

        if cards_remaining == 0:
            return 0.0

        counts = Strategy.count_remaining_cards(game_state)
        duplicate_count = sum(
            count
            for num, count in counts["numbers"].items()
            if num in hand.number_cards
        )

        bust_prob = duplicate_count / cards_remaining

        if hand.second_chance_available:
            bust_prob = 0.0

        return bust_prob

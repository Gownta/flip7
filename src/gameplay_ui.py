"""
Flip 7 Terminal Game UI

Terminal UI functions for playing Flip 7.
"""

from src.game_state import GameState
from src.card import CardType, ActionType
from src.action_handler import ActionHandler
from src.player_hand import AddCardResult
from src.strategy import Strategy


def get_hand_text(game_state, player_idx=0):
    """
    Get the text representation of a player's hand.

    Returns:
        String containing hand information
    """
    hand = game_state.get_player_hand(player_idx)
    lines = []

    lines.append("=" * 60)
    lines.append("YOUR HAND")
    lines.append("=" * 60)

    if hand.number_cards:
        numbers = sorted(hand.number_cards)
        lines.append(f"Number cards: {numbers}")
        lines.append(f"Base score: {sum(numbers)}")
        lines.append(f"Unique numbers: {len(numbers)}/7")
    else:
        lines.append("Number cards: (none)")

    if hand.modifiers:
        mod_strs = [str(mod) for mod in hand.modifiers]
        lines.append(f"Modifiers: {', '.join(mod_strs)}")
    else:
        lines.append("Modifiers: (none)")

    if hand.action_cards:
        action_strs = [str(action) for action in hand.action_cards]
        lines.append(f"Action cards: {', '.join(action_strs)}")

    lines.append(f"\nDeck: {game_state.deck.cards_remaining()} cards remaining")
    lines.append("=" * 60)

    return "\n".join(lines)


def get_card_drawn_text(card):
    """Get the text for a drawn card."""
    return f">>> You drew: {card}"


def get_recommendation_text(game_state, player_idx=0):
    """
    Get the strategy recommendation text.

    Returns:
        String containing recommendation details
    """
    recommendation, details = Strategy.recommend_action(game_state, player_idx)
    lines = []

    lines.append("-" * 60)
    lines.append("STRATEGY RECOMMENDATION")
    lines.append("-" * 60)

    if "reason" in details:
        lines.append(f"Recommendation: {recommendation}")
        lines.append(f"Reason: {details['reason']}")
    else:
        lines.append(f"Recommendation: {recommendation}")
        lines.append(f"Current score if staying: {details['current_score']}")
        lines.append(f"Expected value of hitting: {details['ev_hit']}")
        lines.append(f"Bust probability: {details['bust_probability']}%")

        if recommendation == "HIT":
            lines.append(
                f"Advantage: +{details['advantage']} expected points by hitting"
            )
        else:
            lines.append(f"Advantage: +{details['advantage']} points by staying")

    lines.append("-" * 60)

    return "\n".join(lines)


def get_bust_text():
    """Get the bust message text."""
    return "!!! BUST! You drew a duplicate number card!\nYour score this round: 0"


def get_duplicate_prompt_text():
    """Get the duplicate number prompt text."""
    return "! Duplicate number detected!"


def get_second_chance_prompt():
    """Get the Second Chance prompt text."""
    return "Use your Second Chance to avoid busting? (y/n): "


def get_second_chance_used_text():
    """Get the Second Chance used confirmation text."""
    return "Second Chance used! You continue playing."


def get_freeze_text():
    """Get the freeze message text."""
    return "*** FREEZE! You must bank your current score."


def get_flip_three_text():
    """Get the Flip Three message text."""
    return "*** FLIP THREE! Drawing 3 cards..."


def get_flip_seven_text():
    """Get the Flip 7 achievement text."""
    return "*** FLIP 7! You collected 7 unique numbers! ***\nRound ends. You get the +15 bonus!"


def get_round_header_text(round_num, total_score):
    """Get the round header text."""
    lines = []
    lines.append("#" * 60)
    lines.append(f"ROUND {round_num} - Current total: {total_score}/200")
    lines.append("#" * 60)
    return "\n".join(lines)


def get_round_start_text():
    """Get the round start text."""
    lines = []
    lines.append("=" * 60)
    lines.append("NEW ROUND STARTING")
    lines.append("=" * 60)
    return "\n".join(lines)


def get_round_complete_text(final_score):
    """Get the round complete text."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"ROUND COMPLETE - Your score: {final_score}")
    lines.append("=" * 60)
    return "\n".join(lines)


def get_game_welcome_text():
    """Get the game welcome text."""
    lines = []
    lines.append("=" * 60)
    lines.append("WELCOME TO FLIP 7!")
    lines.append("=" * 60)
    lines.append("\nGoal: Be the first to reach 200 points")
    lines.append("- Draw cards to build your score")
    lines.append("- BUST if you draw a duplicate number")
    lines.append("- Collect 7 unique numbers for FLIP 7 bonus (+15)")
    lines.append("\nGood luck!\n")
    return "\n".join(lines)


def get_game_complete_text(total_score, round_num):
    """Get the game completion text."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"CONGRATULATIONS! YOU REACHED {total_score} POINTS!")
    lines.append(f"Game completed in {round_num} rounds")
    lines.append("=" * 60)
    return "\n".join(lines)


def display_hand(game_state, player_idx=0):
    """Display the player's current hand."""
    print("\n" + get_hand_text(game_state, player_idx))


def display_card_drawn(card):
    """Display a card that was just drawn."""
    print("\n" + get_card_drawn_text(card))


def display_recommendation(game_state, player_idx=0):
    """Display the strategy recommendation."""
    print("\n" + get_recommendation_text(game_state, player_idx))


def handle_draw(game_state, player_idx=0):
    """
    Handle drawing a card for the player.

    Returns True if the player can continue, False if they bust or are frozen.
    """
    hand = game_state.get_player_hand(player_idx)

    try:
        card, result = game_state.draw_card(player_idx)
        display_card_drawn(card)

        if result == AddCardResult.BUST:
            print("\n" + get_bust_text())
            return False

        elif result == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE:
            print("\n" + get_duplicate_prompt_text())
            choice = input(get_second_chance_prompt()).strip().lower()
            if choice == "y":
                ActionHandler.handle_second_chance(hand, card)
                print(get_second_chance_used_text())
                return True
            else:
                hand.has_busted = True
                print("\n" + get_bust_text())
                return False

        elif result == AddCardResult.FROZEN:
            print("\n" + get_freeze_text())
            return False

        elif card.type == CardType.ACTION and card.action_type == ActionType.FLIP_THREE:
            print("\n" + get_flip_three_text())
            results = ActionHandler.handle_flip_three(game_state, player_idx)

            for i, res in enumerate(results, 1):
                if res == AddCardResult.BUST:
                    print(f"\n!!! Card {i}: BUST!")
                    return False
                elif res == AddCardResult.FROZEN:
                    print(f"\n*** Card {i}: FREEZE!")
                    return False
                elif res == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE:
                    print(f"\n! Card {i}: Duplicate detected!")
                    choice = input(get_second_chance_prompt()).strip().lower()
                    if choice == "y":
                        ActionHandler.handle_second_chance(hand, card)
                        print("Second Chance used!")
                    else:
                        hand.has_busted = True
                        print("\n!!! BUST!")
                        return False

            print(f"Drew {len(results)} cards from Flip Three")

        if hand.has_flip_seven():
            print("\n" + get_flip_seven_text())
            return False

        return True

    except ValueError as e:
        print(f"\nError: {e}")
        return False


def play_round(game_state):
    """Play a single round of Flip 7."""
    game_state.start_round()
    player_idx = 0

    print("\n" + get_round_start_text())

    can_continue = True
    while can_continue and game_state.round_active:
        display_hand(game_state, player_idx)

        hand = game_state.get_player_hand(player_idx)
        if hand.is_frozen or hand.has_busted:
            break

        display_recommendation(game_state, player_idx)

        choice = input("\n(H)it or (S)tay? ").strip().lower()

        if choice == "h" or choice == "hit":
            can_continue = handle_draw(game_state, player_idx)
        elif choice == "s" or choice == "stay":
            print("\nYou chose to STAY and bank your score.")
            break
        else:
            print("Invalid choice. Please enter 'h' or 's'.")

    scores = game_state.end_round()
    final_score = scores[player_idx]

    display_hand(game_state, player_idx)
    print("\n" + get_round_complete_text(final_score))

    return final_score


def play_game():
    """Play a full game of Flip 7 (first to 200 points)."""
    print("\n" + get_game_welcome_text())

    game_state = GameState(num_players=1)
    total_score = 0
    round_num = 0

    while total_score < 200:
        round_num += 1
        print("\n" + get_round_header_text(round_num, total_score))

        round_score = play_round(game_state)
        total_score += round_score

        print(f"\nCumulative score: {total_score}/200")

        if total_score < 200:
            input("\nPress Enter to start next round...")

    print("\n" + get_game_complete_text(total_score, round_num))


def main():
    """Main entry point with error handling."""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        raise

"""
Flip 7 Terminal Game

Single-player terminal UI for playing Flip 7.
"""

from src.game_state import GameState
from src.card import CardType, ActionType
from src.action_handler import ActionHandler
from src.player_hand import AddCardResult
from src.strategy import Strategy


def display_hand(game_state, player_idx=0):
    """Display the player's current hand."""
    hand = game_state.get_player_hand(player_idx)

    print("\n" + "=" * 60)
    print("YOUR HAND")
    print("=" * 60)

    if hand.number_cards:
        numbers = sorted(hand.number_cards)
        print(f"Number cards: {numbers}")
        print(f"Base score: {sum(numbers)}")
        print(f"Unique numbers: {len(numbers)}/7")
    else:
        print("Number cards: (none)")

    if hand.modifiers:
        mod_strs = []
        for mod in hand.modifiers:
            mod_strs.append(str(mod))
        print(f"Modifiers: {', '.join(mod_strs)}")
    else:
        print("Modifiers: (none)")

    if hand.action_cards:
        action_strs = []
        for action in hand.action_cards:
            action_strs.append(str(action))
        print(f"Action cards: {', '.join(action_strs)}")

    print(f"\nDeck: {game_state.deck.cards_remaining()} cards remaining")
    print("=" * 60)


def display_card_drawn(card):
    """Display a card that was just drawn."""
    print(f"\n>>> You drew: {card}")


def display_recommendation(game_state, player_idx=0):
    """Display the strategy recommendation."""
    recommendation, details = Strategy.recommend_action(game_state, player_idx)

    print("\n" + "-" * 60)
    print("STRATEGY RECOMMENDATION")
    print("-" * 60)

    if "reason" in details:
        print(f"Recommendation: {recommendation}")
        print(f"Reason: {details['reason']}")
    else:
        print(f"Recommendation: {recommendation}")
        print(f"Current score if staying: {details['current_score']}")
        print(f"Expected value of hitting: {details['ev_hit']}")
        print(f"Bust probability: {details['bust_probability']}%")

        if recommendation == "HIT":
            print(f"Advantage: +{details['advantage']} expected points by hitting")
        else:
            print(f"Advantage: +{details['advantage']} points by staying")

    print("-" * 60)


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
            print("\n!!! BUST! You drew a duplicate number card!")
            print("Your score this round: 0")
            return False

        elif result == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE:
            print("\n! Duplicate number detected!")
            choice = (
                input("Use your Second Chance to avoid busting? (y/n): ")
                .strip()
                .lower()
            )
            if choice == "y":
                ActionHandler.handle_second_chance(hand, card)
                print("Second Chance used! You continue playing.")
                return True
            else:
                hand.has_busted = True
                print("\n!!! BUST! Your score this round: 0")
                return False

        elif result == AddCardResult.FROZEN:
            print("\n*** FREEZE! You must bank your current score.")
            return False

        elif card.type == CardType.ACTION and card.action_type == ActionType.FLIP_THREE:
            print("\n*** FLIP THREE! Drawing 3 cards...")
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
                    choice = (
                        input("Use your Second Chance to avoid busting? (y/n): ")
                        .strip()
                        .lower()
                    )
                    if choice == "y":
                        ActionHandler.handle_second_chance(hand, card)
                        print("Second Chance used!")
                    else:
                        hand.has_busted = True
                        print("\n!!! BUST!")
                        return False

            print(f"Drew {len(results)} cards from Flip Three")

        if hand.has_flip_seven():
            print("\n*** FLIP 7! You collected 7 unique numbers! ***")
            print("Round ends. You get the +15 bonus!")
            return False

        return True

    except ValueError as e:
        print(f"\nError: {e}")
        return False


def play_round(game_state):
    """Play a single round of Flip 7."""
    game_state.start_round()
    player_idx = 0

    print("\n" + "=" * 60)
    print("NEW ROUND STARTING")
    print("=" * 60)

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
    print(f"\n{'=' * 60}")
    print(f"ROUND COMPLETE - Your score: {final_score}")
    print(f"{'=' * 60}")

    return final_score


def play_game():
    """Play a full game of Flip 7 (first to 200 points)."""
    print("\n" + "=" * 60)
    print("WELCOME TO FLIP 7!")
    print("=" * 60)
    print("\nGoal: Be the first to reach 200 points")
    print("- Draw cards to build your score")
    print("- BUST if you draw a duplicate number")
    print("- Collect 7 unique numbers for FLIP 7 bonus (+15)")
    print("\nGood luck!\n")

    game_state = GameState(num_players=1)
    total_score = 0
    round_num = 0

    while total_score < 200:
        round_num += 1
        print(f"\n{'#' * 60}")
        print(f"ROUND {round_num} - Current total: {total_score}/200")
        print(f"{'#' * 60}")

        round_score = play_round(game_state)
        total_score += round_score

        print(f"\nCumulative score: {total_score}/200")

        if total_score < 200:
            input("\nPress Enter to start next round...")

    print("\n" + "=" * 60)
    print(f"CONGRATULATIONS! YOU REACHED {total_score} POINTS!")
    print(f"Game completed in {round_num} rounds")
    print("=" * 60)


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        raise

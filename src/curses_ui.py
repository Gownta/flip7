"""
Curses-based UI for Flip 7 game.

Displays game information at fixed screen positions with real-time updates.
"""

import curses
from src.game_state import GameState
from src.card import CardType, ActionType
from src.action_handler import ActionHandler
from src.player_hand import AddCardResult
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
)


class CursesUI:
    """
    Manages curses-based UI with fixed screen positions.

    Layout:
    - Row 0-2: Game header (round/score info)
    - Row 4-12: Hand display
    - Row 14-22: Strategy recommendation
    - Row 24-30: Messages/events
    - Row 32+: Input prompt
    """

    def __init__(self, stdscr):
        """Initialize the curses UI."""
        self.stdscr = stdscr
        self.setup_colors()

        # Screen positions
        self.header_row = 0
        self.hand_row = 4
        self.recommendation_row = 15
        self.message_row = 25
        self.input_row = 33

        # Message buffer
        self.messages = []
        self.max_messages = 6

    def setup_colors(self):
        """Initialize color pairs for the UI."""
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)

    def clear_area(self, start_row, num_rows):
        """Clear a specific area of the screen."""
        for i in range(num_rows):
            self.stdscr.move(start_row + i, 0)
            self.stdscr.clrtoeol()

    def display_text_at(self, row, text, color_pair=0):
        """Display multi-line text starting at the given row."""
        lines = text.split("\n")
        max_y, max_x = self.stdscr.getmaxyx()
        for i, line in enumerate(lines):
            if row + i < max_y - 1:
                # Truncate line to fit screen width, leaving room for safe display
                display_line = line[: max_x - 2] if len(line) > max_x - 2 else line
                try:
                    self.stdscr.addstr(row + i, 0, display_line, color_pair)
                except curses.error:
                    pass

    def display_header(self, round_num, total_score):
        """Display the game header at the top."""
        self.clear_area(self.header_row, 3)
        header_text = get_round_header_text(round_num, total_score)
        self.display_text_at(self.header_row, header_text, curses.color_pair(4))

    def display_hand(self, game_state, player_idx=0):
        """Display the player's hand."""
        self.clear_area(self.hand_row, 10)
        hand_text = get_hand_text(game_state, player_idx)
        self.display_text_at(self.hand_row, hand_text, curses.color_pair(1))

    def display_recommendation(self, game_state, player_idx=0):
        """Display the strategy recommendation."""
        self.clear_area(self.recommendation_row, 8)
        rec_text = get_recommendation_text(game_state, player_idx)
        self.display_text_at(self.recommendation_row, rec_text, curses.color_pair(2))

    def add_message(self, message, color_pair=0):
        """Add a message to the message area."""
        self.messages.append((message, color_pair))
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        self.refresh_messages()

    def refresh_messages(self):
        """Refresh the message display area."""
        self.clear_area(self.message_row, self.max_messages)
        max_y, max_x = self.stdscr.getmaxyx()
        for i, (msg, color) in enumerate(self.messages):
            lines = msg.split("\n")
            for j, line in enumerate(lines):
                if i + j < self.max_messages:
                    # Truncate line to fit screen width, leaving room for safe display
                    display_line = line[: max_x - 2] if len(line) > max_x - 2 else line
                    try:
                        self.stdscr.addstr(
                            self.message_row + i + j, 0, display_line, color
                        )
                    except curses.error:
                        pass

    def get_input(self, prompt):
        """Get user input at the input row."""
        self.clear_area(self.input_row, 2)
        max_y, max_x = self.stdscr.getmaxyx()
        # Truncate prompt to fit screen width
        display_prompt = prompt[: max_x - 22] if len(prompt) > max_x - 22 else prompt
        try:
            self.stdscr.addstr(self.input_row, 0, display_prompt)
            self.stdscr.refresh()
            curses.echo()
            response = self.stdscr.getstr(
                self.input_row, len(display_prompt), 20
            ).decode("utf-8")
            curses.noecho()
            return response.strip().lower()
        except curses.error:
            curses.noecho()
            return ""

    def refresh(self):
        """Refresh the screen."""
        self.stdscr.refresh()

    def handle_draw(self, game_state, player_idx=0):
        """
        Handle drawing a card for the player.

        Returns True if the player can continue, False if they bust or are frozen.
        """
        hand = game_state.get_player_hand(player_idx)

        try:
            card, result = game_state.draw_card(player_idx)
            self.add_message(get_card_drawn_text(card), curses.color_pair(4))
            self.refresh()

            if result == AddCardResult.BUST:
                self.add_message(get_bust_text(), curses.color_pair(3))
                self.refresh()
                return False

            elif result == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE:
                self.add_message(get_duplicate_prompt_text(), curses.color_pair(2))
                self.refresh()
                choice = self.get_input(get_second_chance_prompt())
                if choice == "y":
                    ActionHandler.handle_second_chance(hand, card)
                    self.add_message(
                        get_second_chance_used_text(), curses.color_pair(1)
                    )
                    self.refresh()
                    return True
                else:
                    hand.has_busted = True
                    self.add_message(get_bust_text(), curses.color_pair(3))
                    self.refresh()
                    return False

            elif result == AddCardResult.FROZEN:
                self.add_message(get_freeze_text(), curses.color_pair(3))
                self.refresh()
                return False

            elif (
                card.type == CardType.ACTION
                and card.action_type == ActionType.FLIP_THREE
            ):
                self.add_message(get_flip_three_text(), curses.color_pair(5))
                self.refresh()
                results = ActionHandler.handle_flip_three(game_state, player_idx)

                for i, res in enumerate(results, 1):
                    if res == AddCardResult.BUST:
                        self.add_message(f"Card {i}: BUST!", curses.color_pair(3))
                        self.refresh()
                        return False
                    elif res == AddCardResult.FROZEN:
                        self.add_message(f"Card {i}: FREEZE!", curses.color_pair(3))
                        self.refresh()
                        return False
                    elif res == AddCardResult.DUPLICATE_WITH_SECOND_CHANCE:
                        self.add_message(
                            f"Card {i}: Duplicate detected!", curses.color_pair(2)
                        )
                        self.refresh()
                        choice = self.get_input(get_second_chance_prompt())
                        if choice == "y":
                            ActionHandler.handle_second_chance(hand, card)
                            self.add_message(
                                "Second Chance used!", curses.color_pair(1)
                            )
                            self.refresh()
                        else:
                            hand.has_busted = True
                            self.add_message("BUST!", curses.color_pair(3))
                            self.refresh()
                            return False

                self.add_message(
                    f"Drew {len(results)} cards from Flip Three", curses.color_pair(4)
                )
                self.refresh()

            if hand.has_flip_seven():
                self.add_message(get_flip_seven_text(), curses.color_pair(1))
                self.refresh()
                return False

            return True

        except ValueError as e:
            self.add_message(f"Error: {e}", curses.color_pair(3))
            self.refresh()
            return False

    def play_round(self, game_state, round_num, total_score):
        """Play a single round of Flip 7."""
        game_state.start_round()
        player_idx = 0

        self.stdscr.clear()
        self.display_header(round_num, total_score)
        self.add_message(get_round_start_text(), curses.color_pair(4))
        self.refresh()

        can_continue = True
        while can_continue and game_state.round_active:
            self.display_hand(game_state, player_idx)
            self.display_recommendation(game_state, player_idx)
            self.refresh()

            hand = game_state.get_player_hand(player_idx)
            if hand.is_frozen or hand.has_busted:
                break

            choice = self.get_input("(H)it or (S)tay? ")

            if choice == "h" or choice == "hit":
                can_continue = self.handle_draw(game_state, player_idx)
            elif choice == "s" or choice == "stay":
                self.add_message(
                    "You chose to STAY and bank your score.", curses.color_pair(1)
                )
                self.refresh()
                break
            else:
                self.add_message(
                    "Invalid choice. Please enter 'h' or 's'.", curses.color_pair(3)
                )
                self.refresh()

        scores = game_state.end_round()
        final_score = scores[player_idx]

        self.display_hand(game_state, player_idx)
        self.add_message(get_round_complete_text(final_score), curses.color_pair(1))
        self.refresh()

        return final_score

    def play_game(self):
        """Play a full game of Flip 7 (first to 200 points)."""
        self.stdscr.clear()
        self.display_text_at(0, get_game_welcome_text(), curses.color_pair(4))
        self.refresh()
        self.get_input("Press Enter to start...")

        game_state = GameState(num_players=1)
        total_score = 0
        round_num = 0

        while total_score < 200:
            round_num += 1

            round_score = self.play_round(game_state, round_num, total_score)
            total_score += round_score

            self.add_message(
                f"Cumulative score: {total_score}/200", curses.color_pair(4)
            )
            self.refresh()

            if total_score < 200:
                self.get_input("Press Enter to start next round...")

        self.stdscr.clear()
        self.display_text_at(
            0, get_game_complete_text(total_score, round_num), curses.color_pair(1)
        )
        self.refresh()
        self.get_input("Press Enter to exit...")


def main_curses(stdscr):
    """Main curses entry point."""
    curses.curs_set(0)
    stdscr.clear()

    ui = CursesUI(stdscr)
    ui.play_game()


def main():
    """Main entry point with curses wrapper and error handling."""
    try:
        curses.wrapper(main_curses)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        raise

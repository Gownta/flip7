"""
Flip 7 Terminal Game

Entry point for playing Flip 7.
"""

from src.gameplay_ui import play_game


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        raise

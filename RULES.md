# Flip 7 Game Rules

## Overview
Flip 7 is a push-your-luck card game where players draw cards to build the highest-scoring hand without going bust. The first player to reach 200 points across multiple rounds wins the game.

## The Deck
The game uses a deck of **94 cards**:

### Number Cards (79 cards)
- **0**: 1 card
- **1**: 1 card
- **2**: 2 cards
- **3**: 3 cards
- **4**: 4 cards
- **5**: 5 cards
- **6**: 6 cards
- **7**: 7 cards
- **8**: 8 cards
- **9**: 9 cards
- **10**: 10 cards
- **11**: 11 cards
- **12**: 12 cards

### Modifier Cards (6 cards)
- **+2**: 1 card (adds 2 points to final score)
- **+4**: 1 card (adds 4 points to final score)
- **+6**: 1 card (adds 6 points to final score)
- **+8**: 1 card (adds 8 points to final score)
- **+10**: 1 card (adds 10 points to final score)
- **X2**: 1 card (doubles the sum of number cards)

### Action Cards (9 cards)
- **Freeze**: 3 cards (forces player to bank their points and stop)
- **Flip Three**: 3 cards (player must draw 3 cards)
- **Second Chance**: 3 cards (allows discarding a duplicate to avoid busting)

## Setup
1. Shuffle all 94 cards to form a central draw pile
2. Choose a dealer (rotates clockwise each round)
3. Deal one card face-up to each player to start the round

## Gameplay

### Turn Structure
On each turn, the dealer asks each player: **Hit or Stay?**

- **Hit**: Draw another card from the deck
- **Stay**: Bank your current score and sit out the rest of the round

### Going Bust
**You bust if you draw a duplicate number card.** When you bust:
- You score **0 points** for the round
- You sit out the rest of the round
- All your cards (including modifiers) are lost

**Exception**: If you have a **Second Chance** card, you can discard the duplicate along with the Second Chance to continue playing.

### Action Cards

#### Freeze
- You **must** bank your current score
- You cannot draw any more cards this round
- Your score is calculated immediately

#### Flip Three
- You **must** draw 3 cards from the top of the deck
- If fewer than 3 cards remain, draw all remaining cards
- Normal rules apply (busting, action cards, etc.)

#### Second Chance
- Saved for later use
- When you draw a duplicate number, you can:
  - Discard the duplicate card
  - Discard the Second Chance card
  - Continue playing without busting
- Can only be used once

## The Flip 7 Bonus

**If you collect 7 different number cards without busting:**
- The round **immediately ends** for all players
- You earn a **+15 point bonus** when scoring
- Only the **first** player to achieve Flip 7 gets the bonus

## Scoring

At the end of the round, calculate scores in this order:

1. **If busted**: Score = 0
2. **Sum number cards**: Add the values of all unique number cards
3. **Apply X2 modifier**: If you have the X2 card, double the sum from step 2
4. **Add point modifiers**: Add values from +2, +4, +6, +8, +10 cards
5. **Add Flip 7 bonus**: If you achieved Flip 7, add +15 points

### Scoring Examples

**Example 1: Basic**
- Cards: 5, 7, 9
- Score: 5 + 7 + 9 = **21 points**

**Example 2: With X2 Modifier**
- Cards: 5, 7, 9, X2
- Score: (5 + 7 + 9) × 2 = **42 points**

**Example 3: With Point Modifiers**
- Cards: 5, 7, 9, +4, +8
- Score: (5 + 7 + 9) + 4 + 8 = **33 points**

**Example 4: X2 + Point Modifiers**
- Cards: 5, 7, 9, X2, +4, +8
- Score: ((5 + 7 + 9) × 2) + 4 + 8 = 42 + 12 = **54 points**

**Example 5: Flip 7 Bonus**
- Cards: 1, 2, 3, 4, 5, 6, 7, +4
- Score: (1+2+3+4+5+6+7) + 4 + 15 = **47 points**

**Example 6: Maximum Theoretical Score**
- Cards: 6, 7, 8, 9, 10, 11, 12, X2, +2, +4, +6, +8, +10
- Score: ((6+7+8+9+10+11+12) × 2) + (2+4+6+8+10) + 15 = 126 + 30 + 15 = **171 points**

## Round End Conditions

A round ends when:
1. A player achieves **Flip 7** (7 unique numbers), OR
2. All players are either **frozen** or **busted**

## Winning the Game

- After each round, add your score to your cumulative total
- The game continues until at least one player reaches **200 points**
- The player with the **highest total score** wins

## Strategy Considerations

### Risk vs. Reward
- More cards = higher potential score, but greater bust risk
- Probability of busting increases as you collect more numbers

### Modifier Management
- X2 is most valuable with high number cards
- Point modifiers are added after X2, so they're not doubled
- Collecting modifiers doesn't increase bust risk

### Flip 7 Decision
- Pursuing Flip 7 gives +15 bonus but requires 7 unique numbers
- High risk of busting with 7 cards
- Ends the round immediately (good if you're ahead, bad if others need more cards)

### Card Counting
- Track which number cards have been played
- Calculate remaining deck composition
- Estimate bust probability before each draw

# ♟️ Lichess Bot – Custom Chess Engine (Python)

## 📖 Overview

This repository contains a **Lichess chess bot** powered by a **custom Python chess engine**.

Unlike random bots, this engine **thinks**. It evaluates future positions and chooses the best move, assuming the opponent also plays optimally.

### 🔍 What Makes It Smart?

- 📘 **Opening Book**: Starts with solid, fast-known openings
- ♟️ **Minimax / Negamax**: Thinks ahead, assuming best responses
- ✂️ **Alpha–Beta Pruning**: Skips pointless calculations
- 🧠 **Evaluation Function**: Scores each position by material & basic strategy
- 🔁 **Iterative Deepening**: Searches layer by layer, always has a backup move

---

## ✨ Key Features

| Feature               | Description |
|----------------------|-------------|
| ♟️ **Negamax Search** | Clean implementation of the classic Minimax strategy |
| ✂️ **Alpha–Beta Pruning** | Improves speed by cutting unneeded branches |
| ⏳ **Iterative Deepening** | Searches move depths progressively (1 → 2 → 3…) |
| 🧠 **Evaluation Function** | Simple but smart scoring: material + positional value |
| 📘 **Opening Book** | Loads opening moves from `openings.csv` |
| 💾 **Transposition Table** | Caches previously seen board positions |
| 💥 **Quiescence Search** | Extends search in "noisy" situations (captures/checks) |

---

## 🏗️ Project Structure

```text
lichess-bot/
│
├── engines/
│   └── bot/
│       ├── main.py         # Top-level search logic & move selection
│       ├── minimax.py      # Negamax + Alpha-Beta + search utilities
│       ├── evaluation.py   # How positions are scored
│       ├── material.py     # Piece values (queen, rook, etc.)
│       ├── positions.py    # Piece-square tables (positional strategy)
│       ├── opening.py      # Opening book loader
│       └── openings.csv    # Opening moves database
│
├── homemade.py            # Connects lichess bot to engine (glue code)
└── lichess-bot.py         # Starts the bot & connects to Lichess
```

---

## 🧩 How the Engine Works 

When it is the bot's turn, it does this:

### 1) Opening Book (first moves)

If the position is still in the opening, the engine tries to play a move from `openings.csv`.

**Why?**
- It is instant  
- Openings are usually good and safe  
- It saves time for later (middlegame tactics)

---

### 2) Time + Depth Decision

In `homemade.py`, the bot calculates a **time budget** and a **search depth**.  
This depends on:
- The time given by Lichess
- The game phase (how many pieces are on the board)

So the bot tries to search deeper when it has more time.

---

### 3) Iterative Deepening (search in layers)

The engine does not jump directly to depth 11.

It searches like this:

- depth 1 → best move so far  
- depth 2 → update best move  
- depth 3 → update best move  
- ...  

If time ends, it still has a good move from the last completed depth.

---

### 4) Negamax (Minimax idea) + Alpha–Beta pruning

Chess is a two-player game:
- On your turn, you want the best score  
- On the opponent's turn, they want the worst score for you

That is exactly the **Minimax** idea.

This engine uses **Negamax**, which is the same logic but written in a simpler way:
- Always "maximize"
- Use a sign change to represent the opponent's point of view

**Alpha–Beta pruning** speeds things up:

- `alpha` = best score **you** can guarantee so far  
- `beta` = best score the **opponent** can guarantee so far

If a branch cannot beat `alpha`/`beta`, the engine stops searching that branch.

---

### 5) Evaluation (how a position is scored)

When the search reaches a depth limit, the engine **evaluates** the board.

In `evaluation.py`, the score is mainly based on:

- **Material** (queen > rook > bishop/knight > pawn)
- **Piece-square tables** (some squares are better for certain pieces)
- **Simple extras** (like development / activity depending on your implementation)

A **higher score means better for the bot**.

---

## 🔎 Example "Thinking Flow" (one move)

1. Lichess sends the current position (moves played so far)  
2. Engine checks the opening book  
   - If found → play book move  
   - If not found:
     - Compute time budget + depth
     - Run iterative deepening
     - Inside each depth: run Negamax + alpha–beta
3. Return the best move found

---

## ✅ What You Can See in the Logs

When running, you will see lines like:

- `budget=20.00s depth=11` → time and depth chosen  
- `depth 1: ... nodes=...` → iterative deepening progress  
- `mate found at depth ...` → checkmate discovered  
- `eval=... pruned=...` → final evaluation and pruning info  

This is useful to show that the bot is:
- Actually searching  
- Using pruning  
- Finding tactics (like mates)

---
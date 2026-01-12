"""
Chess Bot Engine
================
A chess engine using minimax search with alpha-beta pruning.

Algorithm (Course Lesson 4):
    Minimax finds the best move by searching the game tree.
    Alpha-beta pruning skips branches that can't affect the result.
    We use the negamax variant which simplifies the code.

Evaluation:
    Material counting (pawns=100, knights=320, etc.)
    Piece-square tables tell pieces where to go
    Bonuses for things like bishop pairs, open files, passed pawns

Search enhancements:
    - Iterative deepening: search depth 1, then 2, then 3...
    - Transposition table: don't re-search positions we've seen
    - Null move pruning: if skipping our turn still wins, prune
    - Late move reductions: search "boring" moves less deeply
    - Killer/history heuristics: remember good moves
    - Quiescence search: don't stop mid-capture

Opening book:
    CSV file with 3000+ positions from known openings
    Cached in memory on first use
"""

from .main import get_move, get_evaluation
from .minimax import negamax, clear_tt, get_search_stats

__all__ = ['get_move', 'get_evaluation', 'negamax', 'clear_tt', 'get_search_stats']

__version__ = '2.0.0'
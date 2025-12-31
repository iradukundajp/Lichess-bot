"""
CHAMPION CHESS BOT ENGINE
=============================================
An AI-powered chess engine combining ALL algorithms from AI course.

COURSE ALGORITHMS IMPLEMENTED:
- Lesson 1: Randomness (opening variety, genetic mutations)
- Lesson 3: Decision Trees (play style selection, game phase detection)
- Lesson 4: Minimax with Alpha-Beta Pruning (core search)
- Lesson 5: KNN (opening book similarity matching)
- Lesson 9: Neural Networks (weighted evaluation function)
- Lesson 11: Genetic Algorithms (weight optimization concept)

ADVANCED TECHNIQUES ADDED:
- Late Move Reductions (LMR) - Search unpromising moves less deeply
- Null Move Pruning - Detect winning positions faster
- Killer Moves - Remember moves that caused cutoffs (KNN-inspired)
- History Heuristic - Learn from experience (Neural Network concept)
- Aspiration Windows - Narrow search window for efficiency
- Principal Variation Search (PVS) - Optimal alpha-beta variant
- Game Phase Detection - Different evaluation for opening/middle/endgame

"""

from .main import get_move
from .evaluation import get_evaluation
from .minimax import minimax, clear_tt, get_search_stats

__all__ = ['get_move', 'get_evaluation', 'minimax', 'clear_tt', 'get_search_stats']
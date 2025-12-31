
import logging
import random
import chess
from chess.engine import Limit, PlayResult

from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import HOMEMADE_ARGS_TYPE, MOVE

from engines.bot.main import get_move

logger = logging.getLogger(__name__)


def _as_seconds(x):
    return float(x) if isinstance(x, (int, float)) else 0.0


def _compute_time_budget(board, time_limit):
#Calculate time to spend on this move."""
    # Per-move time limit
    per_move = getattr(time_limit, "time", None)
    if isinstance(per_move, (int, float)) and per_move > 0:
        return min(float(per_move) * 0.95, 20.0)
    
    # Get clock info
    if board.turn == chess.WHITE:
        clock = _as_seconds(getattr(time_limit, "white_clock", 0))
        inc = _as_seconds(getattr(time_limit, "white_inc", 0))
    else:
        clock = _as_seconds(getattr(time_limit, "black_clock", 0))
        inc = _as_seconds(getattr(time_limit, "black_inc", 0))
    
    if clock <= 0:
        return 5.0
    
    # Estimate moves remaining
    pieces = len(board.piece_map())
    if pieces <= 10:
        expected_moves = 15
    elif pieces <= 16:
        expected_moves = 25
    elif pieces <= 24:
        expected_moves = 35
    else:
        expected_moves = 40
    
    # Base time allocation
    budget = clock / expected_moves + inc * 0.9
    
    # Limits
    max_budget = clock * 0.15  # Never use more than 15%
    budget = min(budget, max_budget, 20.0)
    
    # Emergency handling
    if clock < 5:
        budget = min(budget, 0.5 + inc * 0.5)
    elif clock < 15:
        budget = min(budget, 1.5 + inc * 0.7)
    elif clock < 30:
        budget = min(budget, 3.0 + inc * 0.8)
    
    return max(0.5, budget)


def _compute_depth(board, budget):
    #Map time budget to search depth.
    pieces = len(board.piece_map())
    moves = len(list(board.legal_moves))
    
    # Base depth from time
    if budget < 0.5:
        depth = 5
    elif budget < 1.0:
        depth = 6
    elif budget < 2.0:
        depth = 7
    elif budget < 4.0:
        depth = 8
    elif budget < 8.0:
        depth = 9
    else:
        depth = 10
    
    # Endgame bonus
    if pieces <= 8:
        depth += 4
    elif pieces <= 12:
        depth += 3
    elif pieces <= 16:
        depth += 2
    elif pieces <= 20:
        depth += 1
    
    # Low branching factor bonus
    if moves < 6:
        depth += 3
    elif moves < 10:
        depth += 2
    elif moves < 15:
        depth += 1
    
    # In check: search deeper
    if board.is_check():
        depth += 1
    
    return min(depth, 20)


class ExampleEngine(MinimalEngine):
    pass


class PyBot(ExampleEngine):

    def search(
        self,
        board: chess.Board,
        time_limit: Limit,
        ponder: bool,
        draw_offered: bool,
        root_moves: MOVE,
    ) -> PlayResult:
        #Main search function.
        budget = _compute_time_budget(board, time_limit)
        depth = _compute_depth(board, budget)
        
        logger.info(f"[PyBot] Budget={budget:.2f}s Depth={depth}")
        
        # Get allowed moves
        if isinstance(root_moves, list) and root_moves:
            allowed = root_moves
        else:
            allowed = list(board.legal_moves)
        allowed_set = set(allowed)
        
        # Search
        try:
            move = get_move(board, depth, time_budget=budget)
            if isinstance(move, str):
                move = chess.Move.from_uci(move)
        except Exception as e:
            logger.exception(f"[PyBot] Error: {e}")
            move = None
        
        # Validate move
        if move is None or move not in board.legal_moves:
            move = random.choice(allowed) if allowed else random.choice(list(board.legal_moves))
            logger.warning(f"[PyBot] Fallback: {move.uci()}")
        elif allowed_set and move not in allowed_set:
            move = random.choice(allowed)
            logger.warning(f"[PyBot] Restricted fallback: {move.uci()}")
        
        return PlayResult(move, None)


class RandomMove(ExampleEngine):
    #Random move engine for testing.

    def search(self, board: chess.Board, *args) -> PlayResult:
        return PlayResult(random.choice(list(board.legal_moves)), None)
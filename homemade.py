"""
Lichess-bot integration.
Connects our engine to the lichess-bot framework.
"""

import logging
import random
import chess
from chess.engine import Limit, PlayResult

from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import HOMEMADE_ARGS_TYPE, MOVE

from engines.bot.main import get_move

logger = logging.getLogger(__name__)


def _as_seconds(x):
    """Safely convert to float."""
    return float(x) if isinstance(x, (int, float)) else 0.0


def _compute_time_budget(board, time_limit):
    """Figure out how long we can think.
    
    We want to use time wisely:
    - Don't use too much early and flag later
    - Use increment wisely
    - Think longer in complex positions
    """
    # fixed time per move (like bullet arenas)
    per_move = getattr(time_limit, "time", None)
    if isinstance(per_move, (int, float)) and per_move > 0:
        return min(float(per_move) * 0.95, 20.0)
    
    # get our clock time and increment
    if board.turn == chess.WHITE:
        clock = _as_seconds(getattr(time_limit, "white_clock", 0))
        inc = _as_seconds(getattr(time_limit, "white_inc", 0))
    else:
        clock = _as_seconds(getattr(time_limit, "black_clock", 0))
        inc = _as_seconds(getattr(time_limit, "black_inc", 0))
    
    if clock <= 0:
        return 5.0
    
    # estimate how many moves left in the game
    pieces = len(board.piece_map())
    if pieces <= 10:
        moves_left = 15  # endgame
    elif pieces <= 16:
        moves_left = 25
    elif pieces <= 24:
        moves_left = 35
    else:
        moves_left = 40
    
    # base time: divide clock by moves left, plus most of increment
    budget = clock / moves_left + inc * 0.85
    
    # never use more than 12% of our clock
    budget = min(budget, clock * 0.12, 20.0)
    
    # emergency: if clock is low, play fast
    if clock < 3:
        budget = min(0.3 + inc * 0.5, budget)
    elif clock < 10:
        budget = min(1.0 + inc * 0.6, budget)
    elif clock < 30:
        budget = min(2.5 + inc * 0.7, budget)
    
    return max(0.3, budget)


def _compute_depth(board, budget):
    """Set search depth based on time and position."""
    pieces = len(board.piece_map())
    moves = len(list(board.legal_moves))
    
    # base depth from time
    if budget < 0.5:
        depth = 6
    elif budget < 1.0:
        depth = 7
    elif budget < 2.0:
        depth = 8
    elif budget < 4.0:
        depth = 9
    elif budget < 8.0:
        depth = 10
    else:
        depth = 11
    
    # endgame: search deeper
    if pieces <= 8:
        depth += 4
    elif pieces <= 12:
        depth += 3
    elif pieces <= 16:
        depth += 2
    
    # few legal moves: can search deeper
    if moves < 6:
        depth += 3
    elif moves < 10:
        depth += 2
    elif moves < 15:
        depth += 1
    
    return min(depth, 20)


class ExampleEngine(MinimalEngine):
    """Base class for engines."""
    pass


class PyBot(ExampleEngine):
    """Our chess bot."""
    
    def search(
        self,
        board: chess.Board,
        time_limit: Limit,
        ponder: bool,
        draw_offered: bool,
        root_moves: MOVE,
    ) -> PlayResult:
        """Find the best move."""
        budget = _compute_time_budget(board, time_limit)
        depth = _compute_depth(board, budget)
        
        logger.info(f"[bot] budget={budget:.2f}s depth={depth}")
        
        # get allowed moves
        if isinstance(root_moves, list) and root_moves:
            allowed = root_moves
        else:
            allowed = list(board.legal_moves)
        allowed_set = set(allowed)
        
        # search for best move
        try:
            move = get_move(board, depth, time_budget=budget)
            if isinstance(move, str):
                move = chess.Move.from_uci(move)
        except Exception as e:
            logger.exception(f"[bot] error: {e}")
            move = None
        
        # make sure move is valid
        if move is None or move not in board.legal_moves:
            move = random.choice(allowed) if allowed else random.choice(list(board.legal_moves))
            logger.warning(f"[bot] fallback: {move.uci()}")
        elif allowed_set and move not in allowed_set:
            move = random.choice(allowed)
            logger.warning(f"[bot] restricted: {move.uci()}")
        
        logger.info(f"[bot] playing: {move.uci()}")
        return PlayResult(move, None)


class RandomMove(ExampleEngine):
    """Random move engine for testing."""
    
    def search(self, board: chess.Board, *args) -> PlayResult:
        return PlayResult(random.choice(list(board.legal_moves)), None)
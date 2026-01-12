"""
Main entry point for the chess engine.
Handles iterative deepening and time management.
"""

import chess
import time
import random
import logging

from .minimax import negamax, clear_tt, get_search_stats
from .opening import get_opening_move

logger = logging.getLogger(__name__)

MATE_SCORE = 100000


def order_root_moves(board, moves, prev_best=None):
    """Sort moves at root for better search order."""
    def score(move):
        s = 0
        
        # always try previous best move first
        if move == prev_best:
            return 1000000
        
        # captures are usually interesting
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            if victim:
                s += victim.piece_type * 100
        
        # promotions are big
        if move.promotion:
            s += 50000
        
        # checks put pressure on opponent
        board.push(move)
        if board.is_check():
            s += 5000
        board.pop()
        
        # center control
        if move.to_square in [chess.D4, chess.D5, chess.E4, chess.E5]:
            s += 100
        
        return s
    
    return sorted(moves, key=score, reverse=True)


def iterative_deepening(board, max_depth, time_limit):
    """Search deeper and deeper until time runs out.
    
    This way we always have a move ready, and deeper searches
    benefit from info gathered at shallower depths.
    """
    start = time.time()
    
    best_move = None
    best_score = 0
    
    for depth in range(1, max_depth + 1):
        elapsed = time.time() - start
        
        # stop if we've used most of our time
        if time_limit and elapsed > time_limit * 0.7:
            break
        
        # aspiration window - search with narrow bounds first
        # this is faster when our guess is correct
        alpha = -999999
        beta = 999999
        
        if depth >= 4 and best_move:
            alpha = best_score - 50
            beta = best_score + 50
        
        depth_best = None
        depth_score = -999999
        
        moves = list(board.legal_moves)
        moves = order_root_moves(board, moves, best_move)
        
        # search each move
        for i, move in enumerate(moves):
            if time_limit and (time.time() - start) > time_limit * 0.9:
                break
            
            board.push(move)
            
            # PVS: full window for first move, null window for rest
            if i == 0:
                score = -negamax(board, depth - 1, -beta, -alpha, ply=1)
            else:
                score = -negamax(board, depth - 1, -alpha - 1, -alpha, ply=1)
                if score > alpha and score < beta:
                    score = -negamax(board, depth - 1, -beta, -alpha, ply=1)
            
            board.pop()
            
            if score > depth_score:
                depth_score = score
                depth_best = move
            
            if score > alpha:
                alpha = score
        
        # if aspiration window failed, re-search with full window
        if depth >= 4 and best_move:
            if depth_score <= best_score - 50 or depth_score >= best_score + 50:
                if (time.time() - start) < time_limit * 0.6:
                    depth_best = None
                    depth_score = -999999
                    
                    for move in moves:
                        if time_limit and (time.time() - start) > time_limit * 0.9:
                            break
                        
                        board.push(move)
                        score = -negamax(board, depth - 1, -999999, 999999, ply=1)
                        board.pop()
                        
                        if score > depth_score:
                            depth_score = score
                            depth_best = move
        
        if depth_best:
            best_move = depth_best
            best_score = depth_score
            
            stats = get_search_stats()
            logger.info(f"depth {depth}: {best_move.uci()} ({best_score:+.0f}) "
                       f"nodes={stats['nodes']} tt={stats['tt_hits']}")
        
        # stop early if we found mate
        if abs(best_score) > MATE_SCORE - 100:
            logger.info(f"mate found at depth {depth}")
            break
    
    return best_move, best_score


def get_move(board, depth=10, time_budget=None):
    """Get the best move for this position.
    
    Args:
        board: chess.Board object
        depth: maximum search depth
        time_budget: seconds available (optional)
    
    Returns:
        chess.Move object
    """
    clear_tt()
    
    # check opening book first
    opening_move = get_opening_move(board)
    if opening_move:
        try:
            move = chess.Move.from_uci(opening_move)
            if move in board.legal_moves:
                logger.info(f"book: {opening_move}")
                return move
        except:
            pass
    
    # figure out how much time to use
    if isinstance(time_budget, (int, float)) and time_budget > 0:
        search_time = min(float(time_budget) * 0.9, 15.0)
    else:
        search_time = 5.0
    
    # adjust depth based on position complexity
    piece_count = len(board.piece_map())
    move_count = len(list(board.legal_moves))
    
    # in endgames we can search much deeper
    if piece_count <= 8:
        depth = min(depth + 4, 16)
    elif piece_count <= 12:
        depth = min(depth + 3, 14)
    elif piece_count <= 16:
        depth = min(depth + 2, 12)
    
    # fewer moves = can search deeper
    if move_count < 8:
        depth = min(depth + 2, 14)
    elif move_count < 15:
        depth = min(depth + 1, 12)
    
    logger.info(f"search: depth={depth}, time={search_time:.1f}s, "
               f"pieces={piece_count}, moves={move_count}")
    
    best_move, best_score = iterative_deepening(board, depth, search_time)
    
    # fallback to random move if something went wrong
    if best_move is None:
        moves = list(board.legal_moves)
        if moves:
            best_move = random.choice(moves)
            logger.warning(f"fallback: {best_move.uci()}")
    
    stats = get_search_stats()
    logger.info(f"result: {best_move.uci()} eval={best_score:+.0f} "
               f"nodes={stats['nodes']} pruned={stats['pruned']}")
    
    return best_move


def get_evaluation(board):
    """Get the static evaluation of a position."""
    from .evaluation import get_evaluation as eval_fn
    return eval_fn(board)
"""
MAXIMUM STRENGTH ENGINE CONTROLLER
Based on Course Lesson 4: Minimax in Board Games

Optimized for deepest possible search within time limits.
"""

import chess
import time
import random
import logging

from .minimax import minimax, clear_tt, get_search_stats
from .opening import play_opening, get_builtin_opening_move

logger = logging.getLogger(__name__)


def order_root_moves(board, moves, prev_best=None):
    def score(move):
        s = 0
        if move == prev_best:
            return 1000000
        
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            if victim:
                s += victim.piece_type * 100
        
        if move.promotion:
            s += 50000
        
        board.push(move)
        if board.is_check():
            s += 5000
        board.pop()
        
        # Center moves
        if move.to_square in [chess.D4, chess.D5, chess.E4, chess.E5]:
            s += 100
        
        return s
    
    return sorted(moves, key=score, reverse=True)


def iterative_deepening(board, max_depth, time_limit):
    start = time.time()
    
    best_move = None
    best_score = 0
    is_max = board.turn == chess.WHITE
    
    for depth in range(1, max_depth + 1):
        elapsed = time.time() - start
        
        # Stop if time running out
        if time_limit and elapsed > time_limit * 0.75:
            break
        
        alpha = -999999
        beta = 999999
        
        # Aspiration window for depth >= 4
        if depth >= 4 and best_move:
            alpha = best_score - 50
            beta = best_score + 50
        
        depth_best = None
        depth_score = -999999 if is_max else 999999
        
        moves = list(board.legal_moves)
        moves = order_root_moves(board, moves, best_move)
        
        fail_high = False
        fail_low = False
        
        for i, move in enumerate(moves):
            if time_limit and (time.time() - start) > time_limit * 0.9:
                break
            
            board.push(move)
            
            # PVS at root
            if i == 0:
                score = minimax(board, depth - 1, alpha, beta, ply=1)
            else:
                score = minimax(board, depth - 1, alpha, alpha + 1, ply=1)
                if alpha < score < beta:
                    score = minimax(board, depth - 1, alpha, beta, ply=1)
            
            board.pop()
            
            if is_max:
                if score > depth_score:
                    depth_score = score
                    depth_best = move
                alpha = max(alpha, score)
            else:
                if score < depth_score:
                    depth_score = score
                    depth_best = move
                beta = min(beta, score)
        
        # Handle aspiration window failures
        if depth >= 4 and best_move:
            if depth_score <= best_score - 50:
                fail_low = True
            elif depth_score >= best_score + 50:
                fail_high = True
            
            if (fail_low or fail_high) and (time.time() - start) < time_limit * 0.6:
                # Re-search with full window
                depth_best = None
                depth_score = -999999 if is_max else 999999
                
                for move in moves:
                    if time_limit and (time.time() - start) > time_limit * 0.9:
                        break
                    
                    board.push(move)
                    score = minimax(board, depth - 1, -999999, 999999, ply=1)
                    board.pop()
                    
                    if is_max and score > depth_score:
                        depth_score = score
                        depth_best = move
                    elif not is_max and score < depth_score:
                        depth_score = score
                        depth_best = move
        
        if depth_best:
            best_move = depth_best
            best_score = depth_score
            
            stats = get_search_stats()
            logger.info(f"[Engine] Depth {depth}: {best_move.uci()} ({best_score:+.0f}) "
                       f"nodes={stats['nodes']} tt={stats['tt_hits']}")
        
        # Stop if mate found
        if abs(best_score) > 90000:
            logger.info(f"[Engine] Mate found at depth {depth}")
            break
    
    return best_move, best_score


def get_move(board, depth, time_budget=None):
    # Main entry point."""
    clear_tt()
    
    # Try opening book first
    opening_move = play_opening(board)
    if not opening_move:
        opening_move = get_builtin_opening_move(board)
    
    if opening_move:
        try:
            move = chess.Move.from_uci(opening_move)
            if move in board.legal_moves:
                logger.info(f"[Engine] Opening book: {opening_move}")
                return move
        except:
            pass
    
    # Calculate search time
    if isinstance(time_budget, (int, float)) and time_budget > 0:
        search_time = min(float(time_budget) * 0.9, 15.0)
    else:
        search_time = 5.0
    
    # Adjust depth based on position
    piece_count = len(board.piece_map())
    move_count = len(list(board.legal_moves))
    
    # Endgame: search much deeper
    if piece_count <= 8:
        depth = min(depth + 4, 16)
    elif piece_count <= 12:
        depth = min(depth + 3, 14)
    elif piece_count <= 16:
        depth = min(depth + 2, 12)
    
    # Fewer moves: can search deeper
    if move_count < 8:
        depth = min(depth + 2, 14)
    elif move_count < 15:
        depth = min(depth + 1, 12)
    
    logger.info(f"[Engine] Search: depth={depth}, time={search_time:.1f}s, "
               f"pieces={piece_count}, moves={move_count}")
    
    best_move, best_score = iterative_deepening(board, depth, search_time)
    
    if best_move is None:
        moves = list(board.legal_moves)
        if moves:
            best_move = random.choice(moves)
            logger.warning(f"[Engine] Fallback: {best_move.uci()}")
    
    stats = get_search_stats()
    logger.info(f"[Engine] Final: {best_move.uci()} eval={best_score:+.0f} "
               f"nodes={stats['nodes']} pruned={stats['pruned']}")
    
    return best_move
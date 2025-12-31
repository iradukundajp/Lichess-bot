"""
MAXIMUM STRENGTH MINIMAX WITH ALL OPTIMIZATIONS
Based on Course Lesson 4: Minimax in Board Games

"""

import chess
from .evaluation import get_evaluation

# Transposition Table
transposition_table = {}
TT_EXACT, TT_ALPHA, TT_BETA = 0, 1, 2

# Search statistics
nodes_searched = 0
tt_hits = 0
pruned_branches = 0
null_move_cutoffs = 0
lmr_reductions = 0

# Killer moves (2 per ply)
MAX_PLY = 64
killer_moves = [[None, None] for _ in range(MAX_PLY)]

# History heuristic
history_table = {}

# MVV-LVA values
MVV_LVA = {1: 100, 2: 320, 3: 330, 4: 500, 5: 950, 6: 20000}


def clear_tt():
    global transposition_table, nodes_searched, tt_hits, pruned_branches
    global null_move_cutoffs, lmr_reductions, killer_moves, history_table
    transposition_table = {}
    nodes_searched = 0
    tt_hits = 0
    pruned_branches = 0
    null_move_cutoffs = 0
    lmr_reductions = 0
    killer_moves = [[None, None] for _ in range(MAX_PLY)]
    history_table = {}


def get_search_stats():
    return {
        'nodes': nodes_searched,
        'tt_hits': tt_hits,
        'pruned': pruned_branches,
        'null_cutoffs': null_move_cutoffs,
        'lmr_reductions': lmr_reductions
    }


def tt_probe(board, depth, alpha, beta):
    global tt_hits
    key = board._transposition_key()
    
    if key in transposition_table:
        stored_depth, stored_score, flag, stored_move = transposition_table[key]
        if stored_depth >= depth:
            tt_hits += 1
            if flag == TT_EXACT:
                return True, stored_score, stored_move
            elif flag == TT_ALPHA and stored_score <= alpha:
                return True, stored_score, stored_move
            elif flag == TT_BETA and stored_score >= beta:
                return True, stored_score, stored_move
        return False, 0, stored_move  # Return move for ordering
    return False, 0, None


def tt_store(board, depth, score, flag, best_move):
    key = board._transposition_key()
    if key in transposition_table:
        if transposition_table[key][0] > depth:
            return
    transposition_table[key] = (depth, score, flag, best_move)


def order_moves(board, moves, ply, tt_move=None):
    """Order moves for maximum pruning efficiency."""
    def score_move(move):
        # TT move first
        if move == tt_move:
            return 1000000
        
        score = 0
        
        # Promotions
        if move.promotion:
            score += 900000 + MVV_LVA.get(move.promotion, 0)
        
        # Captures (MVV-LVA)
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            victim_val = MVV_LVA.get(victim.piece_type, 100) if victim else 100
            attacker_val = MVV_LVA.get(attacker.piece_type, 0) if attacker else 0
            score += 100000 + victim_val * 10 - attacker_val
        
        # Killer moves
        if ply < MAX_PLY:
            if move == killer_moves[ply][0]:
                score = max(score, 90000)
            elif move == killer_moves[ply][1]:
                score = max(score, 89000)
        
        # History heuristic
        if not board.is_capture(move):
            piece = board.piece_at(move.from_square)
            if piece:
                key = (piece.piece_type, move.to_square)
                score += min(history_table.get(key, 0), 80000)
        
        return score
    
    return sorted(moves, key=score_move, reverse=True)


def quiescence(board, alpha, beta, ply):
    """Quiescence search - resolve captures."""
    global nodes_searched
    nodes_searched += 1
    
    if ply > 20:
        return get_evaluation(board)
    
    stand_pat = get_evaluation(board)
    is_max = board.turn == chess.WHITE
    
    if is_max:
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
    else:
        if stand_pat <= alpha:
            return alpha
        beta = min(beta, stand_pat)
    
    # Get captures and promotions only
    captures = [m for m in board.legal_moves if board.is_capture(m) or m.promotion]
    captures = order_moves(board, captures, ply)
    
    # Delta pruning
    if is_max and stand_pat + 1000 < alpha:
        return alpha
    if not is_max and stand_pat - 1000 > beta:
        return beta
    
    for move in captures:
        # SEE pruning: skip bad captures
        if board.is_capture(move) and not move.promotion:
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                if MVV_LVA.get(victim.piece_type, 0) < MVV_LVA.get(attacker.piece_type, 0) - 100:
                    continue
        
        board.push(move)
        score = quiescence(board, alpha, beta, ply + 1)
        board.pop()
        
        if is_max:
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        else:
            if score <= alpha:
                return alpha
            beta = min(beta, score)
    
    return alpha if is_max else beta


def minimax(board, depth, alpha, beta, ply=0, do_null=True):
    """Main search function with all optimizations."""
    global nodes_searched, pruned_branches, null_move_cutoffs, lmr_reductions
    nodes_searched += 1
    
    is_max = board.turn == chess.WHITE
    orig_alpha = alpha
    
    # TT lookup
    tt_hit, tt_score, tt_move = tt_probe(board, depth, alpha, beta)
    if tt_hit and ply > 0:
        return tt_score
    
    # Base case
    if depth <= 0:
        return quiescence(board, alpha, beta, ply)
    
    if board.is_game_over():
        return get_evaluation(board)
    
    in_check = board.is_check()
    
    # Check extension
    if in_check:
        depth += 1
    
    # Null move pruning
    if (do_null and depth >= 3 and not in_check and ply > 0 and
        has_non_pawn_material(board)):
        
        R = 3 if depth >= 6 else 2
        board.push(chess.Move.null())
        null_score = -minimax(board, depth - 1 - R, -beta, -beta + 1, ply + 1, False)
        board.pop()
        
        if (is_max and null_score >= beta) or (not is_max and null_score <= alpha):
            null_move_cutoffs += 1
            return beta if is_max else alpha
    
    # Get and order moves
    moves = list(board.legal_moves)
    if not moves:
        return get_evaluation(board)
    
    moves = order_moves(board, moves, ply, tt_move)
    
    best_move = moves[0]
    best_score = -999999 if is_max else 999999
    
    for i, move in enumerate(moves):
        is_capture = board.is_capture(move)
        gives_check = board.gives_check(move)
        
        board.push(move)
        
        # LMR: reduce depth for late quiet moves
        reduction = 0
        if (depth >= 3 and i >= 4 and not in_check and not is_capture and 
            not gives_check and not move.promotion):
            reduction = 1 if i < 10 else 2
            lmr_reductions += 1
        
        # PVS
        if i == 0:
            score = minimax(board, depth - 1, alpha, beta, ply + 1)
        else:
            # Null window search
            score = minimax(board, depth - 1 - reduction, alpha, alpha + 1, ply + 1)
            
            # Re-search if needed
            if is_max and score > alpha and (reduction > 0 or score < beta):
                score = minimax(board, depth - 1, alpha, beta, ply + 1)
            elif not is_max and score < beta and (reduction > 0 or score > alpha):
                score = minimax(board, depth - 1, alpha, beta, ply + 1)
        
        board.pop()
        
        if is_max:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
                pruned_branches += 1
                if not is_capture:
                    update_killers(move, ply)
                    update_history(move, depth, board)
                break
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                pruned_branches += 1
                if not is_capture:
                    update_killers(move, ply)
                    update_history(move, depth, board)
                break
    
    # Store in TT
    if best_score <= orig_alpha:
        flag = TT_ALPHA
    elif best_score >= beta:
        flag = TT_BETA
    else:
        flag = TT_EXACT
    tt_store(board, depth, best_score, flag, best_move)
    
    return best_score


def has_non_pawn_material(board):
    """Check if side to move has pieces (for null move safety)."""
    color = board.turn
    for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        if board.pieces(pt, color):
            return True
    return False


def update_killers(move, ply):
    if ply >= MAX_PLY:
        return
    if move != killer_moves[ply][0]:
        killer_moves[ply][1] = killer_moves[ply][0]
        killer_moves[ply][0] = move


def update_history(move, depth, board):
    piece = board.piece_at(move.from_square)
    if piece:
        key = (piece.piece_type, move.to_square)
        history_table[key] = history_table.get(key, 0) + depth * depth
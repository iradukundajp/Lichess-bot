"""
Minimax search with alpha-beta pruning.
Based on Course Lesson 4: Minimax in Board Games

Uses negamax formulation - score is always from the perspective
of the side to move. This makes the code cleaner and avoids sign bugs.
"""

import chess
from .evaluation import get_evaluation

# transposition table stores positions we've already searched
transposition_table = {}
TT_EXACT, TT_ALPHA, TT_BETA = 0, 1, 2

# search stats for debugging
nodes_searched = 0
tt_hits = 0
pruned_branches = 0

# killer moves - quiet moves that caused cutoffs at each ply
MAX_PLY = 64
killer_moves = [[None, None] for _ in range(MAX_PLY)]

# history table - tracks which moves have been good historically
history_table = {}

# piece values for move ordering (most valuable victim, least valuable attacker)
PIECE_VAL = {1: 100, 2: 320, 3: 330, 4: 500, 5: 950, 6: 20000}

MATE_SCORE = 100000


def clear_tt():
    """Reset everything for a new search."""
    global transposition_table, nodes_searched, tt_hits, pruned_branches
    global killer_moves, history_table
    transposition_table = {}
    nodes_searched = 0
    tt_hits = 0
    pruned_branches = 0
    killer_moves = [[None, None] for _ in range(MAX_PLY)]
    history_table = {}


def get_search_stats():
    """Return search statistics."""
    return {
        'nodes': nodes_searched,
        'tt_hits': tt_hits,
        'pruned': pruned_branches,
    }


def tt_probe(board, depth, alpha, beta):
    """Check if we've seen this position before."""
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
        # even if we can't use the score, use the move for ordering
        return False, 0, stored_move
    return False, 0, None


def tt_store(board, depth, score, flag, best_move):
    """Save position to transposition table."""
    key = board._transposition_key()
    # only replace if new search is deeper
    if key in transposition_table:
        if transposition_table[key][0] > depth:
            return
    transposition_table[key] = (depth, score, flag, best_move)


def order_moves(board, moves, ply, tt_move=None):
    """Sort moves so we search the best ones first.
    
    Good move ordering = more pruning = faster search.
    Order: TT move > captures > killers > history
    """
    def score_move(move):
        # always search the TT move first
        if move == tt_move:
            return 1000000
        
        score = 0
        
        # promotions are usually good
        if move.promotion:
            score += 900000 + PIECE_VAL.get(move.promotion, 0)
        
        # captures: take big pieces with small pieces (MVV-LVA)
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            victim_val = PIECE_VAL.get(victim.piece_type, 100) if victim else 100
            attacker_val = PIECE_VAL.get(attacker.piece_type, 0) if attacker else 0
            score += 100000 + victim_val * 10 - attacker_val
        
        # killer moves caused cutoffs before at this ply
        if ply < MAX_PLY:
            if move == killer_moves[ply][0]:
                score = max(score, 90000)
            elif move == killer_moves[ply][1]:
                score = max(score, 89000)
        
        # history heuristic - moves that were good before
        if not board.is_capture(move):
            piece = board.piece_at(move.from_square)
            if piece:
                key = (piece.piece_type, move.to_square)
                score += min(history_table.get(key, 0), 80000)
        
        return score
    
    return sorted(moves, key=score_move, reverse=True)


def evaluate_relative(board):
    """Get evaluation from side-to-move's perspective.
    
    This is key for negamax - we always want the score
    to be positive if the position is good for US.
    """
    score = get_evaluation(board)  # this returns score for WHITE
    return score if board.turn == chess.WHITE else -score


def quiescence(board, alpha, beta, ply):
    """Search captures until the position is quiet.
    
    This prevents the horizon effect where we stop searching
    right before losing a piece.
    """
    global nodes_searched
    nodes_searched += 1
    
    # don't go too deep
    if ply > 30:
        return evaluate_relative(board)
    
    # stand pat - can we just not capture and be happy?
    stand_pat = evaluate_relative(board)
    
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat
    
    # delta pruning - if we're way behind, don't bother
    if stand_pat + 1000 < alpha:
        return alpha
    
    # only look at captures and promotions
    captures = [m for m in board.legal_moves if board.is_capture(m) or m.promotion]
    captures = order_moves(board, captures, ply)
    
    for move in captures:
        # skip obviously bad captures (trading queen for pawn when defended)
        if board.is_capture(move) and not move.promotion:
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                if PIECE_VAL.get(victim.piece_type, 0) + 100 < PIECE_VAL.get(attacker.piece_type, 0):
                    continue
        
        board.push(move)
        score = -quiescence(board, -beta, -alpha, ply + 1)
        board.pop()
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha


def negamax(board, depth, alpha, beta, ply=0, do_null=True):
    """Main search function using negamax with alpha-beta.
    
    Negamax trick: instead of alternating max/min, we always
    maximize but negate the score when recursing. This works
    because max(a,b) = -min(-a,-b).
    """
    global nodes_searched, pruned_branches
    nodes_searched += 1
    
    orig_alpha = alpha
    
    # check transposition table
    tt_hit, tt_score, tt_move = tt_probe(board, depth, alpha, beta)
    if tt_hit and ply > 0:
        return tt_score
    
    # leaf node - run quiescence search
    if depth <= 0:
        return quiescence(board, alpha, beta, ply)
    
    # game over?
    if board.is_game_over():
        if board.is_checkmate():
            return -MATE_SCORE + ply  # prefer faster mates
        return 0  # draw
    
    in_check = board.is_check()
    
    # extend search when in check
    if in_check:
        depth += 1
    
    # null move pruning - skip our turn and see if we're still winning
    # if so, this position is probably good and we can prune
    if do_null and depth >= 3 and not in_check and ply > 0:
        if has_non_pawn_material(board):
            R = 3 if depth >= 6 else 2
            board.push(chess.Move.null())
            null_score = -negamax(board, depth - 1 - R, -beta, -beta + 1, ply + 1, False)
            board.pop()
            
            if null_score >= beta:
                return beta
    
    # get and sort moves
    moves = list(board.legal_moves)
    if not moves:
        if in_check:
            return -MATE_SCORE + ply
        return 0
    
    moves = order_moves(board, moves, ply, tt_move)
    
    best_score = -999999
    best_move = moves[0]
    
    for i, move in enumerate(moves):
        is_capture = board.is_capture(move)
        gives_check = board.gives_check(move)
        
        board.push(move)
        
        # late move reductions - search "boring" moves less deeply
        reduction = 0
        if depth >= 3 and i >= 4 and not in_check and not is_capture:
            if not gives_check and not move.promotion:
                reduction = 1 if i < 10 else 2
        
        # principal variation search
        if i == 0:
            # search first move with full window
            score = -negamax(board, depth - 1, -beta, -alpha, ply + 1, True)
        else:
            # search other moves with null window first
            score = -negamax(board, depth - 1 - reduction, -alpha - 1, -alpha, ply + 1, True)
            
            # if it beats alpha, re-search with full window
            if score > alpha and (reduction > 0 or score < beta):
                score = -negamax(board, depth - 1, -beta, -alpha, ply + 1, True)
        
        board.pop()
        
        if score > best_score:
            best_score = score
            best_move = move
        
        if score > alpha:
            alpha = score
        
        # beta cutoff - opponent won't let us get here
        if alpha >= beta:
            pruned_branches += 1
            if not is_capture:
                update_killers(move, ply)
                update_history(move, depth, board)
            break
    
    # save to transposition table
    if best_score <= orig_alpha:
        flag = TT_ALPHA
    elif best_score >= beta:
        flag = TT_BETA
    else:
        flag = TT_EXACT
    tt_store(board, depth, best_score, flag, best_move)
    
    return best_score


def has_non_pawn_material(board):
    """Check if we have pieces (not just pawns).
    
    Null move is dangerous in endgames with only pawns
    because zugzwang is more common.
    """
    color = board.turn
    for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        if board.pieces(pt, color):
            return True
    return False


def update_killers(move, ply):
    """Remember this move caused a cutoff."""
    if ply >= MAX_PLY:
        return
    if move != killer_moves[ply][0]:
        killer_moves[ply][1] = killer_moves[ply][0]
        killer_moves[ply][0] = move


def update_history(move, depth, board):
    """Track that this move was good."""
    piece = board.piece_at(move.from_square)
    if piece:
        key = (piece.piece_type, move.to_square)
        # bonus is depth squared - deeper cutoffs are more valuable
        history_table[key] = history_table.get(key, 0) + depth * depth


# keep old name for backwards compatibility
def minimax(board, depth, alpha, beta, ply=0, do_null=True):
    """Wrapper for backwards compatibility."""
    return negamax(board, depth, alpha, beta, ply, do_null)
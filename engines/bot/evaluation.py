
import chess

# PIECE VALUES
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 950,
    chess.KING: 20000
}

# PIECE-SQUARE TABLES (Built-in)
# Pawn tables
PAWN_MG = [
      0,   0,   0,   0,   0,   0,   0,   0,
     98, 134,  61,  95,  68, 126,  34, -11,
     -6,   7,  26,  31,  65,  56,  25, -20,
    -14,  13,   6,  21,  23,  12,  17, -23,
    -27,  -2,  -5,  12,  17,   6,  10, -25,
    -26,  -4,  -4, -10,   3,   3,  33, -12,
    -35,  -1, -20, -23, -15,  24,  38, -22,
      0,   0,   0,   0,   0,   0,   0,   0,
]

PAWN_EG = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
]

# Knight tables
KNIGHT_MG = [
   -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
     -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
   -105, -21, -58, -33, -17, -28, -19,  -23,
]

KNIGHT_EG = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]

# Bishop tables
BISHOP_MG = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]

BISHOP_EG = [
    -14, -21, -11,  -8,  -7,  -9, -17, -24,
     -8,  -4,   7, -12,  -3, -13,  -4, -14,
      2,  -8,   0,  -1,  -2,   6,   0,   4,
     -3,   9,  12,   9,  14,  10,   3,   2,
     -6,   3,  13,  19,   7,  10,  -3,  -9,
    -12,  -3,   8,  10,  13,   3,  -7, -15,
    -14, -18,  -7,  -1,   4,  -9, -15, -27,
    -23,  -9, -23,  -5,  -9, -16,  -5, -17,
]

# Rook tables
ROOK_MG = [
     32,  42,  32,  51,  63,   9,  31,  43,
     27,  32,  58,  62,  80,  67,  26,  44,
     -5,  19,  26,  36,  17,  45,  61,  16,
    -24, -11,   7,  26,  24,  35,  -8, -20,
    -36, -26, -12,  -1,   9,  -7,   6, -23,
    -45, -25, -16, -17,   3,   0,  -5, -33,
    -44, -16, -20,  -9,  -1,  11,  -6, -71,
    -19, -13,   1,  17,  16,   7, -37, -26,
]

ROOK_EG = [
     13,  10,  18,  15,  12,  12,   8,   5,
     11,  13,  13,  11,  -3,   3,   8,   3,
      7,   7,   7,   5,   4,  -3,  -5,  -3,
      4,   3,  13,   1,   2,   1,  -1,   2,
      3,   5,   8,   4,  -5,  -6,  -8, -11,
     -4,   0,  -5,  -1,  -7, -12,  -8, -16,
     -6,  -6,   0,   2,  -9,  -9, -11,  -3,
     -9,   2,   3,  -1,  -5, -13,   4, -20,
]

# Queen tables
QUEEN_MG = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]

QUEEN_EG = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]

# King tables
KING_MG = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

KING_EG = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43,
]

# PST lookup
PST_MG = {
    chess.PAWN: PAWN_MG,
    chess.KNIGHT: KNIGHT_MG,
    chess.BISHOP: BISHOP_MG,
    chess.ROOK: ROOK_MG,
    chess.QUEEN: QUEEN_MG,
    chess.KING: KING_MG,
}

PST_EG = {
    chess.PAWN: PAWN_EG,
    chess.KNIGHT: KNIGHT_EG,
    chess.BISHOP: BISHOP_EG,
    chess.ROOK: ROOK_EG,
    chess.QUEEN: QUEEN_EG,
    chess.KING: KING_EG,
}

# GAME PHASE
PHASE_WEIGHT = {chess.KNIGHT: 1, chess.BISHOP: 1, chess.ROOK: 2, chess.QUEEN: 4}
TOTAL_PHASE = 24

def get_game_phase(board):
    phase = 0
    for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        phase += len(board.pieces(pt, chess.WHITE)) * PHASE_WEIGHT[pt]
        phase += len(board.pieces(pt, chess.BLACK)) * PHASE_WEIGHT[pt]
    return min(phase / TOTAL_PHASE, 1.0)


# MAIN EVALUATION

def get_evaluation(board):
    #Main evaluation function.
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    if board.can_claim_fifty_moves() or board.is_repetition(2):
        return 0
    
    phase = get_game_phase(board)
    score = 0
    
    score += evaluate_material(board)
    score += evaluate_pst(board, phase)
    score += evaluate_pawns(board, phase)
    score += evaluate_king_safety(board, phase)
    score += evaluate_mobility(board)
    score += evaluate_rooks(board)
    score += evaluate_bishops(board)
    score += evaluate_knights(board)
    score += evaluate_threats(board)
    score += evaluate_center(board, phase)
    
    if phase < 0.4:
        score += evaluate_king_activity(board)
    
    return int(score)


def evaluate_material(board):
    score = 0
    for pt in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        score += len(board.pieces(pt, chess.WHITE)) * PIECE_VALUES[pt]
        score -= len(board.pieces(pt, chess.BLACK)) * PIECE_VALUES[pt]
    return score


def evaluate_pst(board, phase):
    """Piece-square table evaluation with phase interpolation."""
    score = 0
    
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None:
            continue
        
        pt = piece.piece_type
        
        if piece.color == chess.WHITE:
            mg_val = PST_MG.get(pt, [0]*64)[sq]
            eg_val = PST_EG.get(pt, [0]*64)[sq]
        else:
            mirrored = chess.square_mirror(sq)
            mg_val = PST_MG.get(pt, [0]*64)[mirrored]
            eg_val = PST_EG.get(pt, [0]*64)[mirrored]
        
        # Interpolate between middlegame and endgame
        pst_val = int(mg_val * phase + eg_val * (1 - phase))
        
        if piece.color == chess.WHITE:
            score += pst_val
        else:
            score -= pst_val
    
    return score


def evaluate_pawns(board, phase):
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        pawns = board.pieces(chess.PAWN, color)
        enemy_pawns = board.pieces(chess.PAWN, not color)
        
        files = [0] * 8
        for sq in pawns:
            files[chess.square_file(sq)] += 1
        
        # Doubled pawns
        for count in files:
            if count > 1:
                score -= mult * 20 * (count - 1)
        
        for sq in pawns:
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            
            # Isolated pawns
            has_neighbor = any(0 <= f <= 7 and files[f] > 0 for f in [file-1, file+1])
            if not has_neighbor:
                score -= mult * 15
            
            # Passed pawns
            is_passed = True
            for esq in enemy_pawns:
                ef, er = chess.square_file(esq), chess.square_rank(esq)
                if abs(ef - file) <= 1:
                    if (color == chess.WHITE and er > rank) or (color == chess.BLACK and er < rank):
                        is_passed = False
                        break
            
            if is_passed:
                advance = rank if color == chess.WHITE else 7 - rank
                base_bonus = [0, 10, 17, 30, 55, 90, 140, 200][advance]
                eg_mult = 1.0 + (1.0 - phase) * 0.8
                score += mult * int(base_bonus * eg_mult)
    
    return score


def evaluate_king_safety(board, phase):
    if phase < 0.3:
        return 0
    
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        king_sq = board.king(color)
        if not king_sq:
            continue
        
        kf, kr = chess.square_file(king_sq), chess.square_rank(king_sq)
        safety = 0
        
        # Pawn shield
        shield_rank = kr + (1 if color == chess.WHITE else -1)
        if 0 <= shield_rank <= 7:
            for f in range(max(0, kf-1), min(8, kf+2)):
                piece = board.piece_at(chess.square(f, shield_rank))
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    safety += 12
                else:
                    safety -= 10
        
        # Open files near king
        for f in range(max(0, kf-1), min(8, kf+2)):
            own_pawn = any(chess.square_file(sq) == f for sq in board.pieces(chess.PAWN, color))
            enemy_pawn = any(chess.square_file(sq) == f for sq in board.pieces(chess.PAWN, not color))
            if not own_pawn and not enemy_pawn:
                safety -= 30
            elif not own_pawn:
                safety -= 18
        
        # Attackers in king zone
        king_zone = []
        for f in range(max(0, kf-1), min(8, kf+2)):
            for r in range(max(0, kr-1), min(8, kr+2)):
                king_zone.append(chess.square(f, r))
        
        attacker_weight = 0
        for sq in king_zone:
            for att_sq in board.attackers(not color, sq):
                piece = board.piece_at(att_sq)
                if piece:
                    weights = {chess.QUEEN: 5, chess.ROOK: 3, chess.BISHOP: 2, chess.KNIGHT: 2}
                    attacker_weight += weights.get(piece.piece_type, 1)
        
        safety -= attacker_weight * 3
        
        # King in center penalty
        if kf in [3, 4] and kr in [0, 7]:
            enemy_major = len(board.pieces(chess.QUEEN, not color)) + len(board.pieces(chess.ROOK, not color))
            if enemy_major > 0:
                safety -= 60
        
        score += mult * int(safety * phase)
    
    return score


def evaluate_mobility(board):
    orig = board.turn
    board.turn = chess.WHITE
    wm = len(list(board.legal_moves))
    board.turn = chess.BLACK
    bm = len(list(board.legal_moves))
    board.turn = orig
    return (wm - bm) * 4


def evaluate_rooks(board):
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        rooks = list(board.pieces(chess.ROOK, color))
        
        for rook_sq in rooks:
            file = chess.square_file(rook_sq)
            rank = chess.square_rank(rook_sq)
            
            own_pawn = any(chess.square_file(sq) == file for sq in board.pieces(chess.PAWN, color))
            enemy_pawn = any(chess.square_file(sq) == file for sq in board.pieces(chess.PAWN, not color))
            
            if not own_pawn and not enemy_pawn:
                score += mult * 30
            elif not own_pawn:
                score += mult * 18
            
            # 7th rank
            if (color == chess.WHITE and rank == 6) or (color == chess.BLACK and rank == 1):
                score += mult * 35
            
            # Connected rooks
            for other in rooks:
                if other != rook_sq and rook_sq in board.attacks(other):
                    score += mult * 12
                    break
    
    return score


def evaluate_bishops(board):
    score = 0
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 55
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 55
    return score


def evaluate_knights(board):
    score = 0
    total_pawns = len(board.pieces(chess.PAWN, chess.WHITE)) + len(board.pieces(chess.PAWN, chess.BLACK))
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        for sq in board.pieces(chess.KNIGHT, color):
            score += mult * (total_pawns - 8) * 2
            
            file, rank = chess.square_file(sq), chess.square_rank(sq)
            in_enemy_half = (color == chess.WHITE and rank >= 4) or (color == chess.BLACK and rank <= 3)
            
            if in_enemy_half:
                can_be_attacked = False
                for af in [file-1, file+1]:
                    if 0 <= af <= 7:
                        for r in (range(rank+1, 8) if color == chess.WHITE else range(0, rank)):
                            piece = board.piece_at(chess.square(af, r))
                            if piece and piece.piece_type == chess.PAWN and piece.color != color:
                                can_be_attacked = True
                                break
                
                if not can_be_attacked:
                    score += mult * 30
    
    return score


def evaluate_threats(board):
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        
        for pt in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
            for sq in board.pieces(pt, color):
                attackers = len(board.attackers(not color, sq))
                defenders = len(board.attackers(color, sq))
                
                if attackers > 0 and defenders == 0:
                    score -= mult * (PIECE_VALUES[pt] // 5)
                elif attackers > defenders:
                    score -= mult * (PIECE_VALUES[pt] // 12)
    
    return score


def evaluate_center(board, phase):
    if phase < 0.3:
        return 0
    
    score = 0
    center = [chess.D4, chess.D5, chess.E4, chess.E5]
    
    for sq in center:
        piece = board.piece_at(sq)
        if piece:
            score += 18 if piece.color == chess.WHITE else -18
        
        if board.is_attacked_by(chess.WHITE, sq):
            score += 6
        if board.is_attacked_by(chess.BLACK, sq):
            score -= 6
    
    return int(score * phase)


def evaluate_king_activity(board):
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        king_sq = board.king(color)
        
        if king_sq:
            f, r = chess.square_file(king_sq), chess.square_rank(king_sq)
            center_dist = max(abs(f - 3.5), abs(r - 3.5))
            score += mult * (4 - center_dist) * 12
            
            enemy_pawns = board.pieces(chess.PAWN, not color)
            if enemy_pawns:
                min_dist = min(chess.square_distance(king_sq, psq) for psq in enemy_pawns)
                score += mult * (7 - min_dist) * 6
    
    return score

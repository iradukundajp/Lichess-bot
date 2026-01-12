"""
Position evaluation for the chess engine.
Returns a score in centipawns from WHITE's perspective.
Positive = white is winning, negative = black is winning.
"""

import chess

# piece values in centipawns (100 = 1 pawn)
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 950,
    chess.KING: 20000
}

# piece-square tables tell us where pieces want to be
# these are from white's perspective, we flip for black

# pawns: control the center, advance in endgame
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

# knights: love the center, hate the edges
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

# bishops: like long diagonals
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

# rooks: love open files and 7th rank
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

# queen: stay safe early, get active late
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

# king: hide in middlegame, come out in endgame
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

# lookup tables for quick access
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

# for calculating game phase
PHASE_WEIGHT = {chess.KNIGHT: 1, chess.BISHOP: 1, chess.ROOK: 2, chess.QUEEN: 4}
TOTAL_PHASE = 24  # 2 knights + 2 bishops + 2 rooks + 1 queen per side


def get_game_phase(board):
    """Figure out if we're in middlegame or endgame.
    
    Returns 1.0 for opening/middlegame, 0.0 for pure endgame.
    We use this to blend between middlegame and endgame piece tables.
    """
    phase = 0
    for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        phase += len(board.pieces(pt, chess.WHITE)) * PHASE_WEIGHT[pt]
        phase += len(board.pieces(pt, chess.BLACK)) * PHASE_WEIGHT[pt]
    return min(phase / TOTAL_PHASE, 1.0)


def get_evaluation(board):
    """Main evaluation function.
    
    Returns score in centipawns from WHITE's perspective.
    Combines material, piece placement, and various bonuses.
    """
    # handle game over positions
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    if board.can_claim_fifty_moves() or board.is_repetition(2):
        return 0
    
    phase = get_game_phase(board)
    
    # start with material and piece-square tables
    mg_score = 0  # middlegame score
    eg_score = 0  # endgame score
    
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece is None:
            continue
        
        pt = piece.piece_type
        value = PIECE_VALUES[pt]
        
        # get piece-square bonus (flip board for black pieces)
        if piece.color == chess.WHITE:
            mg_pst = PST_MG[pt][sq]
            eg_pst = PST_EG[pt][sq]
            mg_score += value + mg_pst
            eg_score += value + eg_pst
        else:
            flipped = chess.square_mirror(sq)
            mg_pst = PST_MG[pt][flipped]
            eg_pst = PST_EG[pt][flipped]
            mg_score -= value + mg_pst
            eg_score -= value + eg_pst
    
    # blend middlegame and endgame scores based on phase
    score = int(mg_score * phase + eg_score * (1 - phase))
    
    # bishop pair bonus - two bishops work well together
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 50
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 50
    
    # rook on open/semi-open file bonus
    score += evaluate_rooks(board)
    
    # passed pawn bonus
    score += evaluate_passed_pawns(board, phase)
    
    return score


def evaluate_rooks(board):
    """Bonus for rooks on open files."""
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        
        for rook_sq in board.pieces(chess.ROOK, color):
            file = chess.square_file(rook_sq)
            
            # check if file has our pawns
            own_pawn = any(chess.square_file(p) == file 
                         for p in board.pieces(chess.PAWN, color))
            # check if file has enemy pawns
            enemy_pawn = any(chess.square_file(p) == file 
                           for p in board.pieces(chess.PAWN, not color))
            
            if not own_pawn and not enemy_pawn:
                score += mult * 25  # open file
            elif not own_pawn:
                score += mult * 15  # semi-open file
    
    return score


def evaluate_passed_pawns(board, phase):
    """Bonus for passed pawns (no enemy pawns can block them)."""
    score = 0
    
    for color in [chess.WHITE, chess.BLACK]:
        mult = 1 if color == chess.WHITE else -1
        
        for pawn_sq in board.pieces(chess.PAWN, color):
            file = chess.square_file(pawn_sq)
            rank = chess.square_rank(pawn_sq)
            
            # check if any enemy pawn can stop this one
            is_passed = True
            for enemy_sq in board.pieces(chess.PAWN, not color):
                enemy_file = chess.square_file(enemy_sq)
                enemy_rank = chess.square_rank(enemy_sq)
                
                # enemy pawn on same or adjacent file ahead of us?
                if abs(enemy_file - file) <= 1:
                    if color == chess.WHITE and enemy_rank > rank:
                        is_passed = False
                        break
                    elif color == chess.BLACK and enemy_rank < rank:
                        is_passed = False
                        break
            
            if is_passed:
                # bonus based on how far advanced
                advance = rank if color == chess.WHITE else 7 - rank
                bonus = [0, 5, 10, 20, 35, 60, 100, 0][advance]
                # passed pawns are more valuable in endgame
                eg_mult = 1.5 - phase * 0.5
                score += mult * int(bonus * eg_mult)
    
    return score
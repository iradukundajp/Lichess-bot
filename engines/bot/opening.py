"""
Opening book for the chess engine.
Loads opening lines from CSV and caches them in memory.
"""

import chess
import random
import os

# cache for opening positions - loaded once at startup
_BOOK_CACHE = {}
_LOADED = False


def _load_book():
    """Load the opening book from CSV file.
    
    Only runs once - results are cached for future calls.
    """
    global _BOOK_CACHE, _LOADED
    
    if _LOADED:
        return
    
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openings.csv')
    
    try:
        import csv
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            
            for row in reader:
                if len(row) < 3:
                    continue
                
                moves_str = row[2].strip()
                if not moves_str:
                    continue
                
                # play through the moves and record each position
                board = chess.Board()
                moves = moves_str.split()
                
                for san_move in moves:
                    try:
                        # make a key from the position
                        fen_key = board.fen().split(' ')[0] + ' ' + ('w' if board.turn else 'b')
                        
                        move = board.parse_san(san_move)
                        uci = move.uci()
                        
                        # add this move as an option for this position
                        if fen_key not in _BOOK_CACHE:
                            _BOOK_CACHE[fen_key] = []
                        if uci not in _BOOK_CACHE[fen_key]:
                            _BOOK_CACHE[fen_key].append(uci)
                        
                        board.push(move)
                    except:
                        break
        
        _LOADED = True
        print(f"[book] loaded {len(_BOOK_CACHE)} positions")
        
    except Exception as e:
        print(f"[book] failed to load: {e}")
        _LOADED = True


# some basic opening moves hardcoded as backup
BUILTIN_BOOK = {
    # starting position
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w": ["e2e4", "d2d4", "c2c4", "g1f3"],
    
    # after 1.e4
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b": ["e7e5", "c7c5", "e7e6", "c7c6"],
    
    # after 1.e4 e5
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w": ["g1f3"],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b": ["b8c6"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w": ["f1b5", "f1c4", "d2d4"],
    
    # ruy lopez
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b": ["a7a6", "g8f6"],
    "r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w": ["b5a4"],
    
    # italian
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b": ["f8c5", "g8f6"],
    
    # sicilian
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w": ["g1f3", "b1c3"],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b": ["d7d6", "b8c6", "e7e6"],
    
    # french
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w": ["d2d4"],
    "rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b": ["d7d5"],
    
    # caro-kann
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w": ["d2d4"],
    "rnbqkbnr/pp1ppppp/2p5/8/3PP3/8/PPP2PPP/RNBQKBNR b": ["d7d5"],
    
    # after 1.d4
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b": ["g8f6", "d7d5", "e7e6"],
    
    # queen's gambit
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w": ["c2c4"],
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b": ["e7e6", "c7c6"],
    
    # indian defenses
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w": ["c2c4"],
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b": ["e7e6", "g7g6"],
    
    # king's indian
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w": ["b1c3"],
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR b": ["f8g7"],
    "rnbqk2r/ppppppbp/5np1/8/2PP4/2N5/PP2PPPP/R1BQKBNR w": ["e2e4"],
}


def get_opening_move(board):
    """Get a book move for the current position.
    
    Returns UCI string like 'e2e4' or None if not in book.
    """
    # load book on first call
    _load_book()
    
    # make key from position
    fen_key = board.fen().split(' ')[0] + ' ' + ('w' if board.turn else 'b')
    
    # try CSV book first
    if fen_key in _BOOK_CACHE:
        moves = _BOOK_CACHE[fen_key]
        # filter to legal moves only
        valid = [m for m in moves if chess.Move.from_uci(m) in board.legal_moves]
        if valid:
            return random.choice(valid)
    
    # try builtin book
    if fen_key in BUILTIN_BOOK:
        moves = BUILTIN_BOOK[fen_key]
        valid = []
        for uci in moves:
            try:
                m = chess.Move.from_uci(uci)
                if m in board.legal_moves:
                    valid.append(uci)
            except:
                pass
        if valid:
            return random.choice(valid)
    
    # first moves with weights
    if board.fullmove_number == 1:
        if board.turn == chess.WHITE:
            return _weighted_pick([("e2e4", 45), ("d2d4", 40), ("c2c4", 10), ("g1f3", 5)])
        else:
            try:
                last = board.peek().uci()
                if last == "e2e4":
                    return _weighted_pick([("c7c5", 35), ("e7e5", 30), ("e7e6", 20), ("c7c6", 15)])
                elif last == "d2d4":
                    return _weighted_pick([("g8f6", 45), ("d7d5", 40), ("e7e6", 15)])
            except:
                pass
    
    return None


def _weighted_pick(choices):
    """Pick randomly from weighted choices."""
    total = sum(w for _, w in choices)
    r = random.uniform(0, total)
    cum = 0
    for move, weight in choices:
        cum += weight
        if r <= cum:
            return move
    return choices[0][0]


def get_book_size():
    """Return number of positions in book."""
    _load_book()
    return len(_BOOK_CACHE) + len(BUILTIN_BOOK)
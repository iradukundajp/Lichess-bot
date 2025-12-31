"""
SMART OPENING BOOK WITH KNN-INSPIRED MATCHING
==============================================
Based on Course Lesson 5: Recommendations in Spotify (KNN)

FROM YOUR COURSE (Lesson 5):
"The k-Nearest Neighbour (kNN) algorithm is based on the idea that 
the class of an item is equal to those closest to it, which are my neighbors :)"

"K is a variable, at K=5 you look at the 5 nearest neighbors"

"Euclidean distance given by the following formula:
d(p,q) = sqrt((p1-q1)² + (p2-q2)² + ...)"

HOW WE APPLY KNN TO CHESS OPENINGS:
Instead of exact position matching, we use "similarity" matching.
If the current position is "close" to a known opening position,
we can use moves from similar positions.

This is like Spotify's collaborative filtering:
"Users who liked this also like..." → "Positions similar to this lead to..."

ALSO USES CONCEPTS FROM:
- Lesson 1 (Randomness): "Randomly choose" from good opening moves
- Lesson 11 (GA): Selection of "fittest" opening moves
"""

import pandas as pd
import chess
import random
import os
import math


def position_similarity(board1, board2):
    """
    CALCULATE POSITION SIMILARITY (KNN-Inspired)
    
    From Course Lesson 5:
    "Euclidean distance: d(p,q) = sqrt((p1-q1)² + (p2-q2)² + ...)"
    
    We adapt this to chess positions by comparing:
    - Piece placement (which squares have which pieces)
    - Material balance
    - Pawn structure
    
    Returns a similarity score (higher = more similar)
    """
    similarity = 0
    
    # Compare piece positions
    for square in chess.SQUARES:
        piece1 = board1.piece_at(square)
        piece2 = board2.piece_at(square)
        
        if piece1 == piece2:
            similarity += 10  # Same piece on same square
        elif piece1 is not None and piece2 is not None:
            if piece1.piece_type == piece2.piece_type:
                similarity += 5  # Same type, different color
            elif piece1.color == piece2.color:
                similarity += 2  # Same color, different type
    
    # Compare castling rights
    if board1.has_kingside_castling_rights(chess.WHITE) == board2.has_kingside_castling_rights(chess.WHITE):
        similarity += 5
    if board1.has_queenside_castling_rights(chess.WHITE) == board2.has_queenside_castling_rights(chess.WHITE):
        similarity += 5
    if board1.has_kingside_castling_rights(chess.BLACK) == board2.has_kingside_castling_rights(chess.BLACK):
        similarity += 5
    if board1.has_queenside_castling_rights(chess.BLACK) == board2.has_queenside_castling_rights(chess.BLACK):
        similarity += 5
    
    # Same side to move
    if board1.turn == board2.turn:
        similarity += 20
    
    return similarity


def find_k_nearest_openings(board, openings_data, k=5):
    """
    FIND K NEAREST OPENINGS (KNN Algorithm from Lesson 5)
    
    From Course:
    "K is a variable, at K=5 you look at the 5 nearest neighbors"
    
    This finds the K most similar opening positions to the current board.
    """
    similarities = []
    
    for opening_moves in openings_data:
        try:
            test_board = chess.Board()
            moves_list = opening_moves.split()
            
            # Replay the opening and check similarity at each step
            for i, move_san in enumerate(moves_list):
                if i > 0:  # Don't compare from starting position
                    sim = position_similarity(board, test_board)
                    if sim > 500:  # Threshold for "similar enough"
                        # Store the next move as a candidate
                        if i < len(moves_list):
                            similarities.append((sim, moves_list[i]))
                
                # Check for exact match
                if board == test_board and i < len(moves_list):
                    similarities.append((9999, moves_list[i]))  # Perfect match
                    break
                
                test_board.push_san(move_san)
                
        except Exception:
            continue
    
    # Sort by similarity (highest first) and return top K
    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:k]


def play_opening(board):
    """
    PLAY OPENING MOVE
    
    Uses the opening book with randomness (Lesson 1):
    "Chatbots: generate random yet relevant responses, feels more human-like"
    
    We randomly choose from good opening moves to:
    1. Add variety (don't always play the same)
    2. Be unpredictable to opponents
    """
    next_opening_moves = []

    # If we go first, play strong opening moves
    if board.turn == chess.WHITE and board.fullmove_number == 1:
        # Multiple good first moves with weights (like GA fitness - Lesson 11)
        weighted_moves = [
            ("e2e4", 40),   # King's pawn - most popular
            ("d2d4", 35),   # Queen's pawn - solid
            ("c2c4", 15),   # English - flexible
            ("g1f3", 10),   # Reti - hypermodern
        ]
        
        # Weighted random selection (from Lesson 1 - randomness)
        total_weight = sum(w for _, w in weighted_moves)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for move, weight in weighted_moves:
            cumulative += weight
            if r <= cumulative:
                return move
        return weighted_moves[0][0]

    # Response to 1.e4
    if board.fullmove_number == 1 and board.turn == chess.BLACK:
        try:
            last_move = board.peek()
            if last_move.uci() == "e2e4":
                responses = [
                    ("e7e5", 35),   # Classical
                    ("c7c5", 35),   # Sicilian - fighting
                    ("e7e6", 15),   # French - solid
                    ("c7c6", 10),   # Caro-Kann - very solid
                    ("d7d5", 5),    # Scandinavian
                ]
                total = sum(w for _, w in responses)
                r = random.uniform(0, total)
                cumulative = 0
                for move, weight in responses:
                    cumulative += weight
                    if r <= cumulative:
                        return move
        except:
            pass

    # Response to 1.d4
    if board.fullmove_number == 1 and board.turn == chess.BLACK:
        try:
            last_move = board.peek()
            if last_move.uci() == "d2d4":
                responses = [
                    ("g8f6", 40),   # Indian defenses
                    ("d7d5", 40),   # Classical
                    ("e7e6", 10),   # Can transpose to QGD
                    ("f7f5", 10),   # Dutch - sharp
                ]
                total = sum(w for _, w in responses)
                r = random.uniform(0, total)
                cumulative = 0
                for move, weight in responses:
                    cumulative += weight
                    if r <= cumulative:
                        return move
        except:
            pass

    # Try to match against the CSV opening book
    new_board = chess.Board()

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'openings.csv')

    try:
        chess_openings = pd.read_csv(file_path)
        chess_openings = chess_openings["moves"].tolist()

        # Loop over each opening
        for opening in chess_openings:
            moves_in_openings = opening.split()

            for index, move in enumerate(moves_in_openings):
                try:
                    new_board.push_san(move)

                    if board == new_board:
                        # Found exact match - get next move
                        if index + 1 < len(moves_in_openings):
                            next_move = board.parse_san(moves_in_openings[index + 1]).uci()
                            next_opening_moves.append(next_move)
                except:
                    break

            new_board.reset()

    except FileNotFoundError:
        pass  # No opening book file

    # If there are no more opening moves, return None
    if not next_opening_moves:
        return None

    # RANDOM SELECTION (From Lesson 1)
    # "Chatbots: generate random yet relevant responses, feels more human-like"
    random_opening_from_array = random.choice(next_opening_moves)

    return random_opening_from_array


# ============================================================================
# BUILT-IN OPENING KNOWLEDGE (EXPANDED)
# When no opening book file is available, use this knowledge
# Covers main lines and common responses
# ============================================================================

BUILT_IN_OPENINGS = {
    # Starting position responses
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w": ["e2e4", "d2d4", "c2c4", "g1f3"],
    
    # After 1.e4
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b": ["e7e5", "c7c5", "e7e6", "c7c6"],
    
    # After 1.d4
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b": ["g8f6", "d7d5", "e7e6"],
    
    # After 1.c4 (English)
    "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b": ["e7e5", "c7c5", "g8f6", "e7e6"],
    
    # After 1.Nf3 (Reti)
    "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b": ["d7d5", "g8f6", "c7c5"],
    
    # ========== 1.e4 e5 lines ==========
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w": ["g1f3", "f1c4", "b1c3"],
    
    # After 1.e4 e5 2.Nf3
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b": ["b8c6", "g8f6"],
    
    # After 1.e4 e5 2.Nf3 Nc6 (Italian/Spanish)
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w": ["f1b5", "f1c4", "d2d4"],
    
    # After 1.e4 e5 2.Nf3 Nc6 3.Bb5 (Ruy Lopez)
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b": ["a7a6", "g8f6", "f7f5"],
    
    # After 1.e4 e5 2.Nf3 Nc6 3.Bc4 (Italian)
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b": ["f1c5", "g8f6"],
    
    # ========== Sicilian Defense ==========
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w": ["g1f3", "b1c3", "c2c3"],
    
    # After 1.e4 c5 2.Nf3
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b": ["d7d6", "b8c6", "e7e6"],
    
    # Open Sicilian 2...d6 3.d4
    "rnbqkbnr/pp2pppp/3p4/2p5/3PP3/5N2/PPP2PPP/RNBQKB1R b": ["c5d4"],
    
    # ========== French Defense ==========
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w": ["d2d4", "b1c3"],
    
    # After 1.e4 e6 2.d4
    "rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b": ["d7d5"],
    
    # ========== Caro-Kann ==========
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w": ["d2d4", "b1c3"],
    
    # ========== 1.d4 d5 lines ==========
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w": ["c2c4", "g1f3", "c1f4"],
    
    # Queen's Gambit 1.d4 d5 2.c4
    "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b": ["e7e6", "c7c6", "d5c4"],
    
    # QGD 1.d4 d5 2.c4 e6
    "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w": ["b1c3", "g1f3"],
    
    # Slav 1.d4 d5 2.c4 c6
    "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w": ["g1f3", "b1c3"],
    
    # ========== Indian Defenses ==========
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w": ["c2c4", "g1f3", "c1f4"],
    
    # King's Indian setup
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b": ["g7g6", "e7e6"],
    
    # After 1.d4 Nf6 2.c4 g6
    "rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w": ["b1c3", "g1f3"],
    
    # After 1.d4 Nf6 2.c4 e6 (Nimzo/QID)
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR w": ["b1c3", "g1f3", "g2g3"],
}


def get_builtin_opening_move(board):
    """
    Get move from built-in opening knowledge.
    Used as fallback when CSV file is not available.
    """
    fen_key = board.board_fen() + " " + ("w" if board.turn else "b")
    
    if fen_key in BUILT_IN_OPENINGS:
        moves = BUILT_IN_OPENINGS[fen_key]
        # Random selection (Lesson 1)
        return random.choice(moves)
    
    return None

import chess

def is_legal_move_sequence(move_sequence):
    board = chess.Board()

    for move_str in move_sequence.split():
        move = chess.Move.from_uci(chess.SQUARE_NAMES.index(move_str[:2].lower()) + chess.SQUARE_NAMES.index(move_str[2:].lower()))
        if move not in board.legal_moves:
            return False
        board.push(move)

    return True

move_sequence = "d4 d5 Nf3 Nf6 Bf4 c5 e3 Nc6 c3 Qb6 Qb3 c4 Qc2 Bf5 Qc1 e6 h3 h6"
result = is_legal_move_sequence(move_sequence)

if result:
    print("The move sequence is legal.")
else:
    print("The move sequence is not legal.")

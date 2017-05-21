from chess import uci
from chess import Board
import engines.ChessAI as ChessAI
import copy

engine = uci.popen_engine('engines/stockfish')
engine.uci()

myAI = ChessAI.ChessAI()
board = Board()

while not board.is_stalemate() and not board.is_game_over():
	m = myAI.getMove(copy.deepcopy(board))
	board.push_uci(m)	

	if board.is_stalemate() or board.is_game_over():
		break; 
	
	engine.position(board)
	engine_move = str(engine.go(movetime=1)[0])
	board.push_uci(engine_move)

print(board)
	

from chess import uci
from chess import Board
import engines.AI as AI
import copy

def runMatches(engine):

	engine = uci.popen_engine('engines/stockfish')
	engine.uci()

	myAI = AI.NN_AI()


	for i in range(1,10):
		board = Board()
		while not board.is_stalemate() and not board.is_game_over():
			m = myAI.getMove(copy.deepcopy(board))
			board.push_uci(m)	

			if board.is_stalemate() or board.is_game_over():
				break; 
			
			engine.position(copy.deepcopy(board))
			engine_move = str(engine.go(movetime=5, depth=i)[0])
			board.push_uci(engine_move)

		print('Depth:',i, 'Result:',board.result())


runMatches('engines/stockfish')

		

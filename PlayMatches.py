from chess import uci
from chess import Board
import engines.AI as AI
import copy

def runMatches(engine):

	engine = uci.popen_engine('engines/stockfish')
	engine.uci()
	
	ai_type = input("1 for minimax, 2 for nn: ")
	if ai_type == '1':
		myAI = AI.Minimax_AI(3)
	elif ai_type == '2':
		myAI = AI.NN_AI()

	log = input("1 for log, enter for no log: ")
	logging = False
	if log == '1':
		logging = True

	for i in range(1,10):
		board = Board()
		while not board.is_stalemate() and not board.is_game_over():
			m = myAI.getMove(copy.deepcopy(board))
			if logging:
				print("AI Move:",m)
				print(board)
			board.push_uci(m)	

			if board.is_stalemate() or board.is_game_over():
				break; 
			
			engine.position(copy.deepcopy(board))
			engine_move = str(engine.go(movetime=5, depth=i)[0])
			if logging:
				print("Engine move:",engine_move)
				print(board)
			board.push_uci(engine_move)

		print('Depth:',i, 'Result:',board.result())


runMatches('engines/stockfish')

		

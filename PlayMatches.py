from chess import uci
from chess import Board
import timeit
import engines.AI as AI
import copy

def runAlphaVsMinimax():
	
	minimax = AI.Minimax_AI(3, alphabeta=False)
	alphabeta = AI.Minimax_AI(4, alphabeta=True)

	minimax_times = []
	alphabeta_times = []

	board = Board()
	while not board.is_stalemate() and not board.is_game_over():
		start = timeit.default_timer()
		m = minimax.getMove(copy.deepcopy(board))
		stop = timeit.default_timer()
		minimax_times.append(stop-start)
		print("Minimax Move:",m)
		board.push_uci(m)	
		print(board)

		if board.is_stalemate() or board.is_game_over():
			break; 

		start = timeit.default_timer()
		m = alphabeta.getMove(copy.deepcopy(board))
		stop = timeit.default_timer()
		alphabeta_times.append(stop-start)
		print("Alphabeta Move:",m)
		board.push_uci(m)	
		print(board)

	print("minimax   avg time:",sum(minimax_times)/len(minimax_times))
	print("alphabeta avg time:",sum(alphabeta_times)/len(alphabeta_times))
	print(board)
	if board.result() == '1-0':
		res = 'Minimax Wins!'
	if board.result() == '0-1':
		res = 'Alphabeta Wins!'
	else:
		res = 'Stalemate'
	print('Result:',res,'==============================================')
	







def runMatches(engine):

	engine = uci.popen_engine('engines/stockfish')
	engine.uci()
	
	ai_type = input("1 for minimax, 2 for nn: ")
	if ai_type == '1':
		myAI = AI.Minimax_AI(3, alphabeta=True)
	elif ai_type == '2':
		myAI = AI.NN_AI()


	log = input("1 for log, enter for no log: ")
	logging = False
	if log == '1':
		logging = True

	maxdepth = int(input('max depth for opponent: ')) + 1

	for i in range(1,maxdepth):
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

		print('Depth:',i, 'Result:',board.result(),'==============================================')


#runMatches('engines/stockfish')
runAlphaVsMinimax()


		

from chess import uci
from chess import Board
import timeit
import engines.AI as AI
import copy

def getInput(inputString, default=None):
	user_input = input(str(inputString) + ' (' + str(default) + '): ')
	if user_input == '':
		return default
	return user_input

def printBoard(board):
	s = str(board).split('\n')
	count = 8
	for i in s:
		print(count,i)	
		count-=1
	print('  a b c d e f g h')

def runMatches():

	whiteEngine = False
	blackEngine = False
	engineDepth = 1
	engineNodes = 1
	engineMovetime = .0001

	ai_type = getInput("White: 1 console, 2 minimax, 3 MonteCarlo, 4 stockfish", default='4')
	if ai_type == '1':
		white = AI.ConsoleAI()
	elif ai_type == '2':
		white = AI.Minimax_AI(int(getInput("Minimax Depth",default=3)))
	elif ai_type == '3':
		white = AI.MonteCarlo()
	elif ai_type == '4':
		whiteEngine = True
		white = uci.popen_engine('engines/stockfish')
		white.uci()

	ai_type = getInput("Black: 1 console, 2 minimax, 3 MonteCarlo, 4 stockfish", default='4')
	if ai_type == '1':
		black = AI.ConsoleAI()
	elif ai_type == '2':
		black = AI.Minimax_AI(int(input("Minimax Depth: ")))
	elif ai_type == '3':
		black = AI.MonteCarlo()
	elif ai_type == '4':
		blackEngine = True
		black = uci.popen_engine('engines/stockfish')
		black.uci()

	log = getInput("Logging?", default='n')
	logging = False
	if log == 'y':
		logging = True

	num_games = int(getInput("Number of games", default=10))

	white_times = []
	black_times = []

	white_wins = 0
	black_wins = 0
	ties = 0


	for i in range(num_games):
		print("Playing game:",str(i+1) + '/' + str(num_games))
		board = Board()
		while not board.is_stalemate() and not board.is_game_over():

			# Get and play White's move
			start = timeit.default_timer()
			if whiteEngine:
				white.position(copy.deepcopy(board))
				whiteMove = str(white.go(movetime=engineMovetime, depth=engineDepth, nodes=engineNodes)[0])
			else:
				whiteMove = white.getMove(copy.deepcopy(board))
			stop = timeit.default_timer()
			white_times.append(stop-start)

			board.push_uci(whiteMove)
			if logging:
				print("White Move:",whiteMove)
				printBoard(board)

			# check if game over
			if board.is_stalemate() or board.is_game_over():
				break;

			# Get and play Black's move
			start = timeit.default_timer()
			if blackEngine:
				black.position(copy.deepcopy(board))
				blackMove = str(black.go(movetime=engineMovetime, depth=engineDepth, nodes=engineNodes)[0])
			else:
				blackMove = black.getMove(copy.deepcopy(board))
			stop = timeit.default_timer()
			black_times.append(stop-start)

			board.push_uci(blackMove)
			if logging:
				print("Black move:",blackMove)
				printBoard(board)

		print(board.result())
		if board.result() == '1-0':
			white_wins += 1
		elif board.result() == '0-1':
			black_wins += 1
		else:
			ties += 1

	print("======================================================")
	print("White:",str(white))
	print("Average move time:",sum(white_times)/len(white_times))
	print("Wins:",white_wins)
	print("======================================================")
	print("Black:",str(black))
	print("Average move time:",sum(black_times)/len(black_times))
	print("Wins:",black_wins)
	print("======================================================")
	print("Ties:",ties)
	print("======================================================")

runMatches()

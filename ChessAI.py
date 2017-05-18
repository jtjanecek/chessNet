import numpy as np
import chess.pgn
from keras.models import load_model

move_map = {'p':-1, 'n':-2,'b':-3,'r':-4,'q':-5,'k':-6,
		    'P': 1, 'N': 2,'B': 3,'R': 4,'Q': 5,'K': 6,
		    '.': 0}

move_to_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

def board_to_str(board, turn):
	s = str(board)
	rows = s.split("\n")	
	result = []	
	for row in rows:
		for piece in row.split(" "):
			result.append(move_map[piece])
	for i in range(8):
		result.append(turn)
	return np.array(result)



class ChessAI():
	def __init__(self):
		from_file = 'from.h5'
		to_file = 'to.h5'
                	

		self._from_nn = load_model(from_file)
		self._to_file = load_model(to_file)

	def getMove(self, board):
		if board.turn:
			t = 1
		else:
			t = -1
		input_board = board_to_str(board,t)
		input_board = input_board.reshape((1,72))
		print(input_board)
		results = self._from_nn.predict(input_board)		
		print(results)


import chess
import copy
b = chess.Board()
c = ChessAI()
move = c.getMove(copy.deepcopy(b))
print("Move:",move)


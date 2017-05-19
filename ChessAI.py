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
		self._to_nn = load_model(to_file)

	def getMove(self, board):
		if board.turn:
			t = 1
		else:
			t = -1
		input_board = board_to_str(board,t)
		from_board = input_board.reshape((1,72))
		results = self._from_nn.predict(from_board)		
		move_from = self._get_sorted(results)
		moves = self._get_to(input_board, move_from)
		for move_from, move_to in moves:
			try:
				board.push_uci(move_from+move_to)
				return move_from + move_to
			except:
				pass
		return "none"
				

	def _get_sorted(self, softmax):
		''' 
		Returns a list of move numbers in order of best -> worst given a softmax
		'''
		softmax = list(softmax[0])
		results = []
		for i in range(len(softmax)):
			results.append((i,softmax[i]))	
		r = sorted(results, key = lambda x: x[1], reverse=True)
		r = [x[0] for x in r]
		return r

	def _get_to(self, board, froms):
		results = []
		for move in froms:
			from_board = self._get_from_board(move)
			brd = np.append(board,from_board) 	
			brd = brd.reshape((1,144))
			tos = self._to_nn.predict(brd)
			x = self._get_sorted(tos)[0:5]
			for move_to in x:
				results.append((self._get_uci_from_int(move),self._get_uci_from_int(move_to)))
		return results

	def _get_from_board(self, num):
		res = [0]*72
		res[num] = 1	
		return res
	
	def _get_uci_from_int(self, num):
		m = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
		col = m[num%8]
		row = 8 - int(num/8) 		
		return str(col) + str(row)
	


import chess
import copy
b = chess.Board()
c = ChessAI()
while(True):
	#print(b)
	while True:
		m = input("Your move: ")
		try:
			b.push_uci(m)
			break;
		except:
			print("Invalid move.")

	move = c.getMove(copy.deepcopy(b))
	print("Computers move:",move)
	b.push_uci(move)


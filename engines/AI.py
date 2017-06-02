import numpy as np
import chess.pgn
from keras.models import load_model
import copy

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



class NN_AI():
	def __init__(self):
		from_file = 'engines/from.h5'
		to_file = 'engines/to.h5'
                	

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
	
		final_movelist = []
		legal_movelist = [str(x) for x in board.legal_moves]

		for move_from, move_to in moves:
			if move_from+move_to in legal_movelist:
				final_movelist.append(move_from+move_to)	
		'''	try:
				board.push_uci(move_from+move_to)
				return move_from + move_to
			except:
				pass
		'''
		for move in final_movelist:
			return move
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
			#x = self._get_sorted(tos)[0:5]
			x = self._get_sorted(tos)
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


class Minimax_AI():
	def __init__(self, depth, alphabeta=True):
		self._depth = depth
		self._opposite = {1:-1,-1:1}
		self._move_map = {'p':-1, 'n':-3,'b':-3,'r':-5,'q':-9,'k':-200,
		    'P': 1, 'N': 3,'B': 3,'R': 5,'Q': 9,'K': 200,
		    '.': 0}
		self._alpha_beta = alphabeta


	def getMove(self, board):
		if board.turn:
			self._turn = 1
		else:
			self._turn = -1
		if self._alpha_beta:
			return self._alphabeta(board, self._depth, True, -999999, 999999)[0]
		else:
			return self._minimax(board, self._depth, True)[0]

	def _minimax(self, board, depth, maxPlayer):
		legal_movelist = [str(x) for x in board.legal_moves]
		if depth == 0 or legal_movelist == []:
			return ('term',self.evaluateBoard(board))
		
		if maxPlayer:
			bestMove = 'none'
			bestValue = -9999
			for move in legal_movelist:
				newBoard = copy.deepcopy(board)	
				newBoard.push_uci(move)
				v = self._minimax(copy.deepcopy(newBoard), depth-1, False)
				if v[1] > bestValue:
					bestValue = v[1]
					bestMove = move
			return (bestMove,bestValue)

		# minimized move
		else:
			bestMove = 'none'
			bestValue = 9999
			for move in legal_movelist:
				newBoard = copy.deepcopy(board)	
				newBoard.push_uci(move)
				v = self._minimax(copy.deepcopy(newBoard), depth-1, True)
				if v[1] < bestValue:
					bestValue = v[1]
					bestMove = move
			return (bestMove,bestValue)

	def _alphabeta(self, board, depth, maxPlayer, alpha, beta):
		legal_movelist = [str(x) for x in board.legal_moves]
		if depth == 0 or legal_movelist == []:
			return ('term',self.evaluateBoard(board))
		
		if maxPlayer:
			bestMove = 'none'
			bestValue = -9999
			for move in legal_movelist:
				newBoard = copy.deepcopy(board)	
				newBoard.push_uci(move)
				v = self._alphabeta(copy.deepcopy(newBoard), depth-1, False, alpha, beta)
				if v[1] > bestValue:
					bestValue = v[1]
					bestMove = move
				alpha = max(alpha, bestValue)
				if beta <= alpha:
					break
			return (bestMove,bestValue)

		# minimized move
		else:
			bestMove = 'none'
			bestValue = 9999
			for move in legal_movelist:
				newBoard = copy.deepcopy(board)	
				newBoard.push_uci(move)
				v = self._alphabeta(copy.deepcopy(newBoard), depth-1, True, alpha, beta)
				if v[1] < bestValue:
					bestValue = v[1]
					bestMove = move
				beta = min(beta, bestValue)
				if beta <= alpha:
					break
			return (bestMove,bestValue)

	def evaluateBoard(self, board):
		sum = 0
		temp = str(board).split('\n')
		for row in temp:
			x = row.split(' ')
			for piece in x:
				sum += self._move_map[piece]
		if self._turn == -1:
			return sum * -1
		return sum	

# for testing
if __name__ == '__main__':
	def _get_uci_from_int(num):
		m = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
		col = m[num%8]
		row = 8 - int(num/8) 		
		return str(col) + str(row)
	while True:
		x = int(input('number: '))	
		print('uci : ', _get_uci_from_int(x))









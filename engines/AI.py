import numpy as np
import chess.pgn
#from keras.models import load_model
import copy
from math import log, sqrt
import random

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


class Node():
	def __init__(self, fen, move, parentNode):
		self.parent = parentNode
		self.children = []

		self.fen = fen
		self._move = move

		self.wins = 0
		self.playouts = 0

	###################################################################################
	# EXPANSION
	###################################################################################
	def genChildren(self):
		board = chess.Board(fen=self.fen)
		board.push_uci(self._move)
		legal_movelist = [str(x) for x in board.legal_moves]
		for move in legal_movelist:
			self.children.append(Node(board.fen(), move, self))

	###################################################################################
	# BACK PROPAGATION
	###################################################################################
	def backPropagate(self, outcome):
		self.playouts += 1
		board = chess.Board(fen=self.fen)
		if board.turn and outcome == 1:
			self.wins += 1
		elif not board.turn and outcome == -1:
			self.wins += 1
		if self.parent == None:
			return
		self.parent.backPropagate(outcome)


class MonteCarlo():
	def __init__(self):
		self._num_simulations = 500
		self._exploitation_parameter = 1.41421356237

	def getMove(self,board):
		if board.turn:
			self._turn = 1
		else:
			self._turn = -1

		bestMove = self.runAllSimulations(board)
		return bestMove

	def runAllSimulations(self, board):
		print("Generating top nodes")
		topNodes = self.genNodesFromBoard(board)

		for i in range(self._num_simulations):
			print("Running simulation",i+1)

			# Selection
			leafNode = self.selection(topNodes)

			# Expansion
			leafNode.genChildren()
			expandedNode = leafNode.children[int(random.random() * len(leafNode.children))]

			# Simulation
			result = self.simulate(expandedNode)

			# Backpropagation
			expandedNode.backPropagate(result)

		# pick best move from top nodes
		for node in topNodes:
			print(node._move,node.wins,node.playouts)

	###################################################################################
	# SELECTION
	###################################################################################
	def selection(self, nodeList):
		selectedNode = self.selectNext(nodeList)
		while selectedNode.children != []:
			selectedNode = self.selectNext(selectedNode.children)
		return selectedNode

	def selectNext(self, nodeList):
		t = 0
		for node in nodeList:
			if node.playouts == 0:
				return node
			t += node.playouts

		best = -9999
		bestNode = None
		for node in nodeList:
			v = self.nodeValue(node, t)
			if v > best:
				best = v
				bestNode = node
		return bestNode

	def nodeValue(self, node, t):
		c1 = node.wins / node.playouts
		c2 = self._exploitation_parameter + sqrt(log(t) / node.playouts)
		return c1 + c2

	###################################################################################
	# SIMULATION
	###################################################################################
	def simulate(self, node):
		board = chess.Board(fen = node.fen)
		while board.result() == '*':
			m = str(list(board.legal_moves)[int(random.random() * len(list(board.legal_moves)))])
			board.push_uci(m)
		if board.result() == '1-0':
			return 1
		elif board.result() == '0-1':
			return -1
		elif board.result() == '1/2-1/2':
			return 0

	def genNodesFromBoard(self, board):
		nodeList = []
		legal_movelist = [str(x) for x in board.legal_moves]
		for move in legal_movelist:
			nodeList.append(Node(board.fen(), move, None))
		return nodeList



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


board = chess.Board()
mc = MonteCarlo()
mc.getMove(board)

# for testing
#if __name__ == '__main__':
	# def _get_uci_from_int(num):
	# 	m = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
	# 	col = m[num%8]
	# 	row = 8 - int(num/8)
	# 	return str(col) + str(row)
	# while True:
	# 	x = int(input('number: '))
	# 	print('uci : ', _get_uci_from_int(x))

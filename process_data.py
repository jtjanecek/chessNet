import numpy as np
import chess.pgn


move_map = {'p':-1, 'n':-2,'b':-3,'r':-4,'q':-5,'k':-6,
		    'P': 1, 'N': 2,'B': 3,'R': 4,'Q': 5,'K': 6,
		    '.': 0}

move_to_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}


def process_data(filename, start, stop):
	board_list = []
	move_from = []
	move_to = []
	count = 0
	with open(filename, 'r') as f:
		for line in f:
			count += 1
			if count < start:
				continue
			if count == end:
				break;
			if count % 100000 == 0:
				print("Processing game:",count)			
			line = line.strip()
			cols = line.split(" ")
			x = eval(cols[0])
			board_list.append(x)
			y = eval(cols[1])
			move_from.append(y)
			z = eval(cols[2])
			move_to.append(z)
	return np.array(board_list), np.array(move_from), np.array(move_to)


def gen_matrix_data(pgn_db, matrix_file):
	count = 0
	pgn_file = open(pgn_db)
	f = open(matrix_file,'a')
	print()
	while True:
		count += 1
		node = chess.pgn.read_game(pgn_file)
		if node == None:
			break;
		if count % 500 == 0:
			print("Game: ",count)
		turn = 1
		board = chess.Board()
		while not node.is_end():
			next_node = node.variation(0)
			curr_move = node.board().uci(next_node.move)
			node = next_node

			board_str = board_to_str(board, turn)
			move_from, move_to = get_move_from_to(curr_move)
			f.write(board_str + ' ' + move_from + ' ' + move_to + '\n') 
			board.push_uci(curr_move)				
			if turn == 1:
				turn = -1
			else:
				turn = 1
	print('Games from:',pgn_db,':',count)	
	pgn_file.close();
	f.close()

def board_to_str(board, turn):
	s = str(board)
	rows = s.split("\n")	
	result = []	
	for row in rows:
		for piece in row.split(" "):
			result.append(move_map[piece])
	for i in range(8):
		result.append(turn)
	return str(result).replace(' ','')

def get_move_from_to(move):
	m1 = move[0:2]
	m2 = move[2:4]	
	move_from = ((8-int(m1[1]))*8) + move_to_map[m1[0]] 	
	move_to = ((8-int(m2[1]))*8) + move_to_map[m2[0]] 	
	x = [0]*72	
	y = [0]*72
	x[move_from] = 1	
	y[move_to] = 1
	return str(x).replace(' ',''), str(y).replace(' ','')





#gen_matrix_data('pgnFiles/2005.pgn', 'mat.txt')



if __name__ == '__main__':
	pgn_file = input('pgn file: ')
	matrix_file = input('matrix file to append to: ')
	gen_matrix_data(pgn_file, matrix_file)




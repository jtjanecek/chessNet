
import chess.pgn

game_moves_file='moves.txt'
moves_matrix_file='matrix_data.txt'

move_map = {'p':-1, 'n':-2,'b':-3,'r':-4,'q':-5,'k':-6,
	    'P': 1, 'N': 2,'B': 3,'R': 4,'Q': 5,'K': 6,
	    '.': 0}

move_to_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

def gen_game_moves():
	pgn_db = input(".pgn file to read: ")
	game_moves_file = input("file to output game moves (1 line per game, delimiter = ' '): ")
	f = open(game_moves_file,'w')
	count = 0
	pgn_file = open(pgn_db)
	while True:
		count += 1
		game = chess.pgn.read_game(pgn_file)
		if game == None:
			break;
		print("Game Number: " + str(count) + " " + game.headers["Result"])
		node = game
		all_moves = ''
		while not node.is_end():
			next_node = node.variation(0)
			all_moves += node.board().uci(next_node.move) + " "
			node = next_node
		f.write(all_moves + '\n')
	pgn.close();
	f.close()

def gen_supervised_data():
	game_move_file = input('file with game moves data: ')	
	matrix_file = input("file for output of matrix data: ")
	f = open(game_move_file,'r')
	lines = f.readlines()
	f.close()	
	count = 1
	for line in lines:
		if line != '\n':
			if count % 100 == 0:
				print("Processing game: ",count)
			record_game(line.strip(), matrix_file)
			count += 1

def record_game(moves, matrix_file):
	f = open(matrix_file,'a')
	move_list = moves.split(" ")
	turn = 1
	board = chess.Board()
	for move in move_list:
		board_str = board_to_str(board, turn)
		move_from, move_to = get_move_from_to(move)
		f.write(board_str + ' ' + move_from + ' ' + move_to + '\n') 
		board.push_uci(move)				
		if turn == 1:
			turn = -1
		else:
			turn = 1
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
		
gen_moves = input("1 = generate game moves from chess_db.pgn\n2 = generate matrix data for each move from each game\n  : ")
if gen_moves == '1':
	gen_game_moves()	
elif gen_moves == '2':
	gen_supervised_data()		
else:
	print("Closing...")

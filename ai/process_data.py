import numpy as np


def process_data(filename, n):
	board_list = []
	move_from = []
	move_to = []
	count = 0
	with open('../data/' + filename, 'r') as f:
		for line in f:
			count += 1
			if count % 10000 == 0:
				print("Processing game:",count)			
			if n == count:
				break;
			line = line.strip()
			cols = line.split(" ")
			x = eval(cols[0])
			board_list.append(x)
			y = eval(cols[1])
			move_from.append(y)
			z = eval(cols[2])
			move_to.append(z)
	return np.array(board_list), np.array(move_from), np.array(move_to)


from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def load_index():
	content = ['r' + str(i) + 'c' + str(j) for i in range(9) for j in range(9)]
	sudoku = []
	error_message = ''
	solution = ['' for i in range(81)]	
	some_input = False

	for i in content:
		if request.args.get(i) is None:
			sudoku.append('')
		else:
			some_input = True
			if request.args.get(i).isalpha() or request.args.get(i) == '0':
				error_message = 'Only numeric values between 1 and 9 allowed.'
			sudoku.append(request.args.get(i))

	if error_message != '':
		return render_template('index.html', sudoku = sudoku, content = content, error_message = error_message, solution = solution)		

	def valid_input(grid,y,x,n):
		if n == 0: 
			return False

		for i in range(0,9):
			if i != x and grid[y][i] == n:
				return False
		for i in range(0,9):
			if i != y and grid[i][x] == n:
				return False	
		x0 = (x//3)*3
		y0 = (y//3)*3
		for i in range(0,3):
			for j in range(0,3):
				if y0+i != y and x0+j != x and j != y and grid[y0+i][x0+j] == n:
					return False
		return True


	def solve(grid):
		find = find_empty(grid)
		if not find:
			return True
		else:
			row, col = find

		for i in range(1,10):
			if valid(grid, i, (row, col)):
				grid[row][col] = i

				if solve(grid):
					return True

				grid[row][col] = 0

		return False

	def valid(grid, num, pos):
		for i in range(len(grid[0])):
			if grid[pos[0]][i] == num and pos[1] != i:
				return False

		for i in range(len(grid)):
			if grid[i][pos[1]] == num and pos[0] != i:
				return False

		gridx_x = pos[1] // 3
		gridx_y = pos[0] // 3

		for i in range(gridx_y*3, gridx_y*3 + 3):
			for j in range(gridx_x * 3, gridx_x*3 + 3):
				if grid[i][j] == num and (i,j) != pos:
					return False
		return True

	def find_empty(grid):
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 0:
					return (i, j)  
		return None



	if some_input:

		s = sudoku
		grid = [
		[s[0], s[1], s[2], s[9], s[10], s[11], s[18], s[19], s[20]], 
		[s[3], s[4], s[5], s[12], s[13], s[14], s[21], s[22], s[23]], 
		[s[6], s[7], s[8], s[15], s[16], s[17], s[24], s[25], s[26]], 
		[s[27], s[28], s[29], s[36], s[37], s[38], s[45], s[46], s[47]], 
		[s[30], s[31], s[32], s[39], s[40], s[41], s[48], s[49], s[50]], 
		[s[33], s[34], s[35], s[42], s[43], s[44], s[51], s[52], s[53]], 
		[s[54], s[55], s[56], s[63], s[64], s[65], s[72], s[73], s[74]], 
		[s[57], s[58], s[59], s[66], s[67], s[68], s[75], s[76], s[77]], 
		[s[60], s[61], s[62], s[69], s[70], s[71], s[78], s[79], s[80]]
		]

		for i in range(9):
			for j in range(9):
				if grid[i][j] != '':
					grid[i][j] = int(grid[i][j])
				else:
					grid[i][j] = 0

		for y in range(9):
			for x in range(9):	
				if grid[y][x] != 0:
					if not valid_input(grid, y, x, grid[y][x]):
						error_message = 'Input not valid.'
						return render_template('index.html', sudoku = sudoku, content = content, error_message = error_message, solution = solution)	
					else:
						error_message = ''

		solve(grid)	

		solution = []
		for k in range(0,9,3):
			for i in range(3):
				for count, j in enumerate(grid[i+k]):
					if count in (0,1,2):
						solution.append(j)
			for i in range(3):
				for count, j in enumerate(grid[i+k]):
					if count in (3,4,5):
						solution.append(j)
			for i in range(3):
				for count, j in enumerate(grid[i+k]):
					if count in (6,7,8):
						solution.append(j)

	return render_template('index.html', sudoku = sudoku, content = content, error_message = error_message, solution = solution)


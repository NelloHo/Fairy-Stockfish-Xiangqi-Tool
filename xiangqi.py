import json
import subprocess
import matplotlib.pyplot as plt

global red, black ,chinesed_data , data, uci
chinese_data = []
eval_data = []

uci_x = {1:'i',2:'h',3:'g',4:'f',5:'e',6:'d',7:'c',8:'b',9:'a'}
x_uci={'i': 1, 'h': 2, 'g': 3, 'f': 4, 'e': 5, 'd': 6, 'c': 7, 'b': 8, 'a': 9}
black_x_uci = {'i': 9, 'h': 8, 'g': 7, 'f': 6, 'e': 5, 'd': 4, 'c': 3, 'b': 2, 'a': 1}
sf_location = 'C:\\Users\\user\\Desktop\\chess\\fairy-stockfish-largeboard_x86-64.exe'
chinese_piece_name = {'k':'將', 'a':'士', 'e':'象', 'r':'車', 'h':'馬', 'c':'炮','p':'兵','+':'進','-':'退','=':'平'}


with open("setting.json") as f:
	load = json.loads(f.read())
	red = load[0]
	black = load[1]
	del load

def Engine(sf_location):
	engine = subprocess.Popen(
		sf_location,
		universal_newlines=True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		bufsize=1,
	)
	return engine

#把字元轉成數字
def input_process(inp):
	move = [i for i in inp]
	for i in range(len(move)):
		try:
			move[i]=int(move[i])
		except:
			pass
	return move


def convert_to_x(engine_move):
	
	engine_move = [i for i in engine_move]
	for i in range(len(engine_move)):
		try:
			engine_move[i]=int(engine_move[i])
		except:
			pass
	output = [[x_uci[engine_move[0]],engine_move[1]+1],[x_uci[engine_move[2]],engine_move[3]+1]]
	return output


def convert_to_uci(origin_position, position):
	
	output = [uci_x[origin_position[0]],origin_position[1]-1,uci_x[position[0]],position[1]-1]
	output =''.join([str(i) for i in output])
	
	return output

def convert_to_chinese(engine_move): #[[8,10],[7,8]]
	
	need_more_love = False
	for piece, value in black.items():
		for index ,position in enumerate(value):
			
			if position == engine_move[0]: #[[8,8],[8,9]]
				
				if len(value) == 2 :
					if value[0][0]==value[1][0]:
						need_more_love = True
				
				if need_more_love:
					if value[index][1] < value[1-index][1]: #前
						if piece in 'eha':
							if engine_move[0][1] - engine_move[1][1] > 0:
								show = '前{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[1][0]))
								
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								show = '前{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]))
						
						else:
							if engine_move[0][1] - engine_move[1][1] > 0:
								show = '前{}進{}'.format(chinese_piece_name[piece], str(engine_move[0][1]-engine_move[1][1]))
							
							elif engine_move[0][1] - engine_move[1][1] == 0:
								show = '前{}平{}'.format(chinese_piece_name[piece], str(engine_move[1][0]))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								show = '前{}退{}'.format(chinese_piece_name[piece], str(engine_move[1][1]-engine_move[0][1]))

					else: #後
						if piece in 'eha':
							if engine_move[0][1] - engine_move[1][1] > 0:
								show = '後{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[1][0]))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								show = '後{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]))
						
						else:
							if engine_move[0][1] - engine_move[1][1] > 0:
								show = '後{}進{}'.format(chinese_piece_name[piece], str(engine_move[0][1]-engine_move[1][1]))
							
							elif engine_move[0][1] - engine_move[1][1] == 0:
								show = '後{}平{}'.format(chinese_piece_name[piece], str(engine_move[1][0]))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								show = '後{}退{}'.format(chinese_piece_name[piece], str(engine_move[1][1]-engine_move[0][1]))

				
				else:
					if piece in 'eha':
						if engine_move[0][1] - engine_move[1][1] > 0:
							show = '{}{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0]))
						
						elif engine_move[0][1] - engine_move[1][1] < 0:
							show = '{}{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0]))
					
					else:
						if engine_move[0][1] - engine_move[1][1] > 0:
							show = '{}{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(engine_move[0][1]-engine_move[1][1]))
						
						elif engine_move[0][1] - engine_move[1][1] == 0:
							show = '{}{}平{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0]))
						
						elif engine_move[0][1] - engine_move[1][1] < 0:
							show = '{}{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(engine_move[1][1]-engine_move[0][1]))
				print(show)
				chinese_data.append(show)



def Engine_response(uci_move):
	
	engine.stdin.write(uci_move+'\n')
	eval()
	engine.stdin.write('go\n')
	
	while True:
		out = engine.stdout.readline()
		if out[0:4] == 'move':
			return convert_to_x(out[5:9])
		elif out[0:5] == 'Error':
			print('Error Move')
			return []
		

#是否吃子
def check_eat_piece(moved_piece,color):
	for piece,value in color.items():
		for opposite_position in value:
			if opposite_position == moved_piece:
				print('吃',chinese_piece_name[piece])
				color[piece].remove(opposite_position)
				break

def move_piece_black(engine_move):
	for piece, value in black.items():
		for position in value:
			if position == engine_move[0]:
				black[piece].remove(engine_move[0])
				black[piece].append(engine_move[1])
				
				


#動子
def move_piece(position,move): # position:[1,2] | move:['c',2,'=',5], ['h','+','+',1]
	#c2=5 h2+3 e3+5 h++3
	origin_position = position[:]
	
	if move[0] == 'h':                #馬的移動
		if move[2] == "+":
			if abs(move[3] - position[0]) == 1:
				position[0] = move[3]
				position[1] += 2
			elif abs(move[3] - position[0]) == 2:
				position[0] = move[3]
				position[1] += 1
			
		elif move[2] == "-":
			if abs(move[3] - position[0]) == 1:
				position[0] = move[3]
				position[1] -= 2
			elif abs(move[3] - position[0]) ==  2:
				position[0] = move[3]
				position[1] -= 1
	
	elif move[0] == 'e':              #象的移動
		if move[2] == "+":
			position[0] = move[3]
			position[1] += 2
			
		elif move[2] == "-":
			position[0] = move[3]
			position[1] -= 2


	elif move[0] == 'a':              #士的移動
		if move[2] == '+':
			position[0] = move[3]
			position[1] += 1
		elif move[2] == '-':
			position[0] = move[3]
			position[1] -= 1

	else:							  #其餘移動
		
		if move[2] == "+":
			position[1] += move[3]
			
		elif move[2] == "-":
			position[1] -= move[3]
			
		elif move[2] == "=":
			position[0] = move[3]

	chinese_data.append(chinese_piece_name[move[0]]+str(move[1])+chinese_piece_name[move[2]]+str(move[3]))
	uci_move = convert_to_uci(origin_position,position)
	
	return uci_move



def print_opposite_position():
	engine.stdin.write('d\n')
	output = []
	while True:
		engine_response = engine.stdout.readline()
		output.append(engine_response)
		if engine_response[0:3] == 'Key':
			break
	output.reverse()
	for i in output:
		print(i.rstrip())

def print_position():
	engine.stdin.write('d\n')
	while True:
		output = engine.stdout.readline()
		print(output.rstrip())
		if output[0:3] == 'Key':
			break

def eval():
	engine.stdin.write('eval\n')
	while True:
		output  = engine.stdout.readline()
		if 'Final evaluation' in output:
			index = []
			for i in range(len(output)):
				if output[i] in ['+','-','(']:
					index.append(i)
			try:
				eval_data.append(output[index[0]:index[1]])
			except:
				pass
			break 
		
def show_eval_chart():
	plt.bar(chinese_data,eval_data,width = 0.2)
	plt.show()

def show_history_move():
	for history_move in chinese_data:
		print(history_move)


def move_handler(position, move):
	uci_move = move_piece(position,move) # ↑
	check_eat_piece(position,black)            #position已經動過了
	engine_move = Engine_response(uci_move)  #type(engine)=x
	convert_to_chinese(engine_move)
	move_piece_black(engine_move) #moved piece: 引擎動的棋子名稱
	check_eat_piece(engine_move[1],red)
	eval()



def start_red():
	while True:
		inp = input()

		if inp == 'd':
			print_position()

		if inp == 'D':
			print_opposite_position()

		if inp == 'e':
			print(eval_data[-2:])
		
		if inp == 'h':
			show_history_move()

		if inp == 'c':#chart
			show_eval_chart()

		elif len(inp) == 4:
			move = input_process(inp) #轉move成int串列
			
			if move[1] not in ['+','-']:
				for i in range(len(red[move[0]])):
					position = red[move[0]][i]
					if position[0] == move[1]:
						move_handler(position,move)
						break	
			
			else:
				if move[1]=='+':
					bigger = [0,'']
					for i in range(len(red[move[0]])):
						position = red[move[0]][i]
						if position[1] > bigger[0]:
							bigger[0]=position[1]
							bigger[1]=position
					move_handler(bigger[1],move)


				elif move[1]=='-':
					smaller = [11,'']
					for i in range(len(red[move[0]])):
						position = red[move[0]][i]
						if position[1] < smaller[0]:
							smaller[0]=position[1]
							smaller[1]=position
					move_handler(smaller[1],move)

	

'''-------------------------------initialize--------------------------------------'''

engine = Engine(sf_location)
engine.stdin.write('xboard\n')
engine.stdin.write('variant xiangqi\n')
engine.stdin.write('st 3\n')


is_red = input('red or black , (r/b) ?') == 'r'


if is_red:
	start_red()

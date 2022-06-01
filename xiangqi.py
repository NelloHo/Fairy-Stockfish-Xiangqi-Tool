import json
import subprocess

global red, black ,chinesed_data , data, uci
chinese_data = []
data =[]

uci_x = {1:'i',2:'h',3:'g',4:'f',5:'e',6:'d',7:'c',8:'b',9:'a'}
x_uci={'i': 1, 'h': 2, 'g': 3, 'f': 4, 'e': 5, 'd': 6, 'c': 7, 'b': 8, 'a': 9}
black_x_uci = {'i': 9, 'h': 8, 'g': 7, 'f': 6, 'e': 5, 'd': 4, 'c': 3, 'b': 2, 'a': 1}
sf_location = 'C:\\Users\\user\\Desktop\\chess\\fairy-stockfish-largeboard_x86-64.exe'
chinese_piece_name = {'k':'將', 'a':'士', 'e':'象', 'r':'車', 'h':'馬', 'c':'炮','p':'兵'}

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
	output =''.join( [str(i) for i in output])
	print(output)
	return output

def convert_to_chinese(engine_move): #[[8,10],[7,8]]
	
	need_more_love = False
	for piece, value in black.items():
		for index ,position in enumerate(value):
			print(position)
			if position == engine_move[0]: #[[8,8],[8,9]]
				
				if len(value) == 2 :
					if value[0][0]==value[1][0]:
						need_more_love = True
				
				if need_more_love:
					if value[index][1] < value[1-index][1]: #前
						if piece in 'eha':
							if engine_move[0][1] - engine_move[1][1] > 0:
								print('前{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[1][0])))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								print('前{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0])))
						
						else:
							if engine_move[0][1] - engine_move[1][1] > 0:
								print('前{}進{}'.format(chinese_piece_name[piece], str(engine_move[0][1]-engine_move[1][1])))
							
							elif engine_move[0][1] - engine_move[1][1] == 0:
								print('前{}平{}'.format(chinese_piece_name[piece], str(engine_move[1][0])))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								print('前{}退{}'.format(chinese_piece_name[piece], str(engine_move[1][1]-engine_move[0][1])))

					else: #後
						if piece in 'eha':
							if engine_move[0][1] - engine_move[1][1] > 0:
								print('後{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[1][0])))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								print('後{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0])))
						
						else:
							if engine_move[0][1] - engine_move[1][1] > 0:
								print('後{}進{}'.format(chinese_piece_name[piece], str(engine_move[0][1]-engine_move[1][1])))
							
							elif engine_move[0][1] - engine_move[1][1] == 0:
								print('後{}平{}'.format(chinese_piece_name[piece], str(engine_move[1][0])))
							
							elif engine_move[0][1] - engine_move[1][1] < 0:
								print('後{}退{}'.format(chinese_piece_name[piece], str(engine_move[1][1]-engine_move[0][1])))

				
				else:
					if piece in 'eha':
						if engine_move[0][1] - engine_move[1][1] > 0:
							print('{}{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0])))
						
						elif engine_move[0][1] - engine_move[1][1] < 0:
							print('{}{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0])))
					
					else:
						if engine_move[0][1] - engine_move[1][1] > 0:
							print('{}{}進{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(engine_move[0][1]-engine_move[1][1])))
						
						elif engine_move[0][1] - engine_move[1][1] == 0:
							print('{}{}平{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(10-engine_move[1][0])))
						
						elif engine_move[0][1] - engine_move[1][1] < 0:
							print('{}{}退{}'.format(chinese_piece_name[piece], str(10-engine_move[0][0]), str(engine_move[1][1]-engine_move[0][1])))
		


def Engine_response(uci_move):
	engine.stdin.write(uci_move+'\n')
	engine.stdin.write('go\n')
	
	while True:
		out = engine.stdout.readline()
		
		print(out)
		if out[0:4] == 'move':
			print(convert_to_x(out[5:9]))
			return convert_to_x(out[5:9])
		elif out[0:5] == 'Error':
			print('Error Move')
			return []
		

#是否吃子
def check_eat_piece(moved_piece):
	for piece,value in black.items():
		for opposite_position in value:
			if opposite_position == moved_piece:
				print('remove',piece)
				black[piece].remove(opposite_position)
				break

def check_eat_piece_red(engine_move):
	for piece,value in red.items():
		for opposite_position in value:
			if opposite_position == engine_move[1]:
				print('remove',piece)
				red[piece].remove(opposite_position)
				break

def move_piece_black(engine_move):
	for piece, value in black.items():
		for position in value:
			if position == engine_move[0]:
				black[piece].remove(engine_move[0])
				black[piece].append(engine_move[1])
				print(piece)
				


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

	chinese_data.append(move)
	uci_move = convert_to_uci(origin_position,position)
	print(position)
	print(uci_move)
	return uci_move


def print_position():
	engine.stdin.write('d\n')
	while True:
		output = engine.stdout.readline()
		print(output)
		if output[0:3] == 'Key':
			break




def move_handler(position, move):
	uci_move = move_piece(position,move) # ↑
	check_eat_piece(position)            #position已經動過了
	engine_move = Engine_response(uci_move)  #type(engine)=x
	convert_to_chinese(engine_move)
	move_piece_black(engine_move) #moved piece: 引擎動的棋子名稱
	check_eat_piece_red(engine_move)
	



def start():
	inp = input()

	if inp == 'd':
		print_position()


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
engine.stdin.write('level 40 5 0\n')

while True:
	start()
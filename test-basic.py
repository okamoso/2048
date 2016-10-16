#coding: utf-8

#

import random


X_MAX = 4
Y_MAX = 4

board = [[0 for y in range(Y_MAX)] for x in range(X_MAX)]

print "INITIAL_BOARD"
#     y
#  +--->
#  | 
# x|

print "---------------------------------"
print board
print "---------------------------------"

# ボードの中で空きのマスを探す
# 0 : 空きなし
def search_empty_cells(b):
	count = 0
	for x in range(X_MAX):
		for y in range(Y_MAX):
			# print x, y

			if b[x][y] == 0:
				count = count + 1			
#	print count
	return count

# ボードを表示
def print_board(b):
	for x in range(X_MAX):
		print b[x]

# ボードに１つ数値を置く
# 置けたらtrue,置けなかったらfalse
# 置く数値の値: INITIAL_CELL
# b : board
def put_another_board(b):
	INITIAL_CELL = 2
	empty_cells = search_empty_cells(b)
	if empty_cells == 0:
		#置き場所がない
		return False
	else:
		#置き場所あり	
		#置き場所を空きセルの中でランダムで決定
		next_cell = random.randint(1,empty_cells)
		
		#空きセルの中に置く
		count = 0;
		for y in range(Y_MAX):
			for x in range(X_MAX):
				if b[x][y] == 0:
					count = count + 1
					if count == next_cell:
						b[x][y] = INITIAL_CELL
	# print b
	return True


# 数値を移動させる
# 
# b: board
# direction: 向き (0-3)
# 0 : 上 ↑
# 1 : 右 →　
# 2 : 下 ↓
# 3 : 左 ←
def shift_board(b,directrion):
	# TODO: ロジック考え中
	return True


def shift_right(b):
	#試しに右移動をやってみる
	# 再帰的にやるのが楽かなー
	# 一番右端じゃなかったら、
	# すぐ隣のセルが空いているかを確認して
	# 空いてたら、すぐ右に移動
	# 
	return True

# x,yのセルをシフトする
# 再帰で最後までシフト
# 成功したらtrue
def shift_cell_right(b,x,y):

	#右端じゃなかったらFalse
	cell_to_move = b[x][y]

	if x >= X_MAX - 1:
		return False
	elif b[x][y] == 0:
		#空きセルには何もしない
		return False
	else:
		# すぐ右のセルが空でなかったらFalse
		if b[x + 1][y] != 0:
			# すぐ右のセルが自分のセルと同じ値
			if b[x + 1][y] == cell_to_move:
				# 値を加算
				b[x + 1][y] = b[x + 1][y] + cell_to_move
				b[x][y] = 0
				print "ADD"
				print_board(board)
			else:
				return False
		else:
			# すぐ右のセルが空の場合
			#右に移動
			b[x+1][y] = cell_to_move
			b[x][y] = 0
			print "SHIFT"
			print_board(board)
			#右に移動したセルで再度判定
			shift_cell_right(b,x+1,y)
	
	
	return True
	
# direction_xがx方向 (1:プラス方向 -1:マイナス方向)
# direction_yがy方向 (1:プラス方向 -1:マイナス方向)

def shift_cell(b,x,y,direction_x , direction_y):

	#direction_*の一応引数チェック(どちらかが1 or -1で他が0)
	if direction_x**2 == 1 and direction_y == 0:
		# ok
		pass
	elif direction_x == 0 and direction_y**2 == 1:
		# ok
		pass
	else:
		print "ERROR:" , direction_x , direction_y
		raise Exception
	
	cell_to_move = b[x][y]

	#右端じゃなかったらFalse

	# x方向の場合

	# 端っこであるかの判定
	if direction_x == 1:
		if x >= X_MAX - 1:
			return False
		pass
	elif direction_x == -1:
		if x <= 0:
			return False
		pass
	elif direction_y == 1:
		if y >= Y_MAX - 1:
			return False
		pass
	elif direction_y == -1:
		if y <= 0:
			return False
		pass
	else:
		print "ERROR:" , direction_x , direction_y
		raise Exception
		#何もしない
			
	if b[x][y] == 0:
		#空きセルには何もしない
		return False
	else:
		# 動かす方向のセルが空でなかったらFalse
		if b[x + direction_x][y+direction_y] != 0:
		
			# すぐ右のセルが自分のセルと同じ値
			if b[x + direction_x][y+direction_y] == cell_to_move:
				# 値を加算
				b[x + direction_x][y+direction_y] = \
					b[x + direction_x][y+direction_y] + cell_to_move
				b[x][y] = 0
				print "ADD"
				print_board(board)
			else:
				return False
		else:
			# 動かす方向のセルが空の場合
			# 移動
			b[x + direction_x][y+direction_y] = cell_to_move
			b[x][y] = 0
			print "SHIFT"
			print_board(board)
			#移動したセルで再度判定
			shift_cell(b,x+direction_x,y+direction_y,direction_x,direction_y)
	
	return True


def move_x_plus(board):
	# x軸プラス方向に動かす
	for y in range(Y_MAX):
		for x in range(X_MAX):
			if shift_cell(board, X_MAX - x - 1 , y , 1 , 0) == True:
#			if shift_cell_right(board, X_MAX - x - 1 , y) == True:
				print "SHIFT_RESULT"
				print_board(board)

def move_x_minus(board):
	# x軸マイナス方向に動かす
	for y in range(Y_MAX):
		for x in range(X_MAX):
			if shift_cell(board, x , y , -1 , 0) == True:
#			if shift_cell_right(board, X_MAX - x - 1 , y) == True:
				print "SHIFT_RESULT"
				print_board(board)

def move_y_plus(board):
	# x軸プラス方向に動かす
	for x in range(X_MAX):
		for y in range(Y_MAX):
			if shift_cell(board, x , Y_MAX - y - 1 , 0 , 1) == True:
#			if shift_cell_right(board, X_MAX - x - 1 , y) == True:
				print "SHIFT_RESULT"
				print_board(board)


def move_y_minus(board):
	# x軸マイナス方向に動かす
	for x in range(X_MAX):
		for y in range(Y_MAX):
			if shift_cell(board, x , y , 0 , -1) == True:
#			if shift_cell_right(board, X_MAX - x - 1 , y) == True:
				print "SHIFT_RESULT"
				print_board(board)

# main

for i in range(100):
	print "MOVE:" , i	

	empty_count = search_empty_cells(board)
	#print empty_count
	
	if put_another_board(board) != True:
		print "ERR: no more cells"
		break
	#
	print "PUT"
	print_board(board)

	move_x_plus(board)
			

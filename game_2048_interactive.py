#coding: utf-8

#

import random
import copy

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

# ボードの中で空きのセルを探す
# >0 :  空きセルの数を返す
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
						return True
	# print b
	return True

	
# １つのセルの値を特定方向に移動
# direction_xがx方向 (1:プラス方向 -1:マイナス方向)
# direction_yがy方向 (1:プラス方向 -1:マイナス方向)
#戻り値 True:動かした 
#      False:動かせなかった / 空のセル
#評価のために戻り値を仕様変更
# -1 : 移動できない or 空のセル
#  0 : セルを移動したが、加算はしていない
# >0 : 加算が発生したセルの数 (=1)
# バグあるかも
def shift_cell(b,x,y,direction_x , direction_y):
	# 加算した数値の数
	# このロジックだと2以上加算されないはずだけど一応カウントに。
	add_count = 0

	#direction_*の一応引数チェック(どちらかが1 or -1で他が0)
	if direction_x**2 == 1 and direction_y == 0:
		# ok
		pass
	elif direction_x == 0 and direction_y**2 == 1:
		# ok
		pass
	else:
		#ここには来ないはず
		print "ERROR:" , direction_x , direction_y
		raise Exception
	
	#自身のセルの値
	cell_to_move = b[x][y]

	# 端っこであるかの判定
	if direction_x == 1:
		if x >= X_MAX - 1:
			return -1
		pass
	elif direction_x == -1:
		if x <= 0:
			return -1
		pass
	elif direction_y == 1:
		if y >= Y_MAX - 1:
			return -1
		pass
	elif direction_y == -1:
		if y <= 0:
			return False
		pass
	else:
		#ここには来ないはず
		print "ERROR:" , direction_x , direction_y
		raise Exception
		#何もしない
			
	if b[x][y] == 0:
		#自身が空きセルの場合には何もしない
		return -1
	else:
		# 移動先のセルが正の値の場合、加算のチェックを実施
		if b[x + direction_x][y+direction_y] > 0:
		
			# 移動先のセルが自分のセルと同じ値
			if b[x + direction_x][y+direction_y] == cell_to_move:
				# 値を加算
				b[x + direction_x][y+direction_y] = \
					b[x + direction_x][y+direction_y] + cell_to_move
				add_count += 1
				# 同一ターンで2回加算されないように一度マイナスの値にしている
				# 最後にマイナス→プラスに戻すことを前提
				b[x + direction_x][y+direction_y] *= -1
				b[x][y] = 0
#				print "ADD"
#				print_board(board)
				return add_count

			else:
				#動かせない
				return -1
		elif b[x + direction_x][y+direction_y] == 0:
			# 動かす方向のセルが空(0)の場合
			# 移動
			b[x + direction_x][y+direction_y] = cell_to_move
			b[x][y] = 0
#			print "SHIFT"
#			print_board(board)
			#移動したセルで再度判定
			if shift_cell(b,x+direction_x,y+direction_y,direction_x,direction_y) > 0:
				add_count = 1 #TODO:微妙
				
				
			return add_count
		else:
			#動かす方向のセルが負の値の場合
			#一度加算されたセルのため、何もしない（動かせない)
			return -1
	
	#ここには来ないはずだけど一応
	return add_count

# ボード上のマイナスの値をプラスに戻す
def flip_positive(b):
	for y in range(Y_MAX):
		for x in range(X_MAX):
			if b[x][y] < 0:
				b[x][y] *= -1

# 
# -1 : 全く移動できない
#  0 : 一つでも移動した
# >0 : 加算したセルの数 (=1)
def move_x_plus(board):
	add_count = 0 # 加算したセルの数
	does_move = 0 # 加算or移動したセルの数 0のまま:移動してない
	# x軸プラス方向に動かす
	for y in range(Y_MAX):
		for x in range(X_MAX):
			a = shift_cell(board, X_MAX - x - 1 , y , 1 , 0)
			if a > 0:
				#加算あり
				add_count += 1
				does_move += 1
			elif a == 0:
				#移動のみ
				does_move += 1
			else:
				pass
	
	#移動
	if does_move > 0:
		return add_count
	else:
		return -1


def move_x_minus(board):
	add_count = 0 # 加算したセルの数
	does_move = 0 # 加算or移動したセルの数 0のまま:移動してない
	# x軸マイナス方向に動かす
	for y in range(Y_MAX):
		for x in range(X_MAX):
			a = shift_cell(board, x , y , -1 , 0)
			if a > 0:
				#加算あり
				add_count += 1
				does_move += 1
			elif a == 0:
				#移動のみ
				does_move += 1
			else:
				pass
	
	#移動
	if does_move > 0:
		return add_count
	else:
		return -1

def move_y_plus(board):
	add_count = 0 # 加算したセルの数
	does_move = 0 # 加算or移動したセルの数 0のまま:移動してない
	# x軸プラス方向に動かす
	for x in range(X_MAX):
		for y in range(Y_MAX):
			a = shift_cell(board, x , Y_MAX - y - 1 , 0 , 1)
			if a > 0:
				#加算あり
				add_count += 1
				does_move += 1
			elif a == 0:
				#移動のみ
				does_move += 1
			else:
				pass
	
	#移動
	if does_move > 0:
		return add_count
	else:
		return -1


def move_y_minus(board):
	add_count = 0 # 加算したセルの数
	does_move = 0 # 加算or移動したセルの数 0のまま:移動してない
	# x軸マイナス方向に動かす
	for x in range(X_MAX):
		for y in range(Y_MAX):
			a = shift_cell(board, x , y , 0 , -1)
			if a > 0:
				#加算あり
				add_count += 1
				does_move += 1
			elif a == 0:
				#移動のみ
				does_move += 1
			else:
				pass
	
	#移動
	if does_move > 0:
		return add_count
	else:
		return -1

#動かせるかどうかチェック
def test_can_move(b):
	test_board = copy.deepcopy(b)
	if move_x_plus(test_board) >= 0:
		return True
	elif move_x_minus(test_board) >= 0:
		return True
	elif move_y_plus(test_board) >= 0:
		return True
	elif move_y_minus(test_board) >= 0:
		return True
	else:
		#no move
		pass
	return False



# main

move_count = 0
does_quit = 0
while True:
	flip_positive(board)
	empty_count = search_empty_cells(board)
	#print empty_count
	
	if put_another_board(board) != True:
		print "ERR: no more cells"
		break
	#

	#動かせるかどうかチェック
	#動かせるのがないと終了
	if test_can_move(board) :
		pass
	else:
		print "no more move"
		print_board(board)
		break
	
	while True:
		print "MOVE:" , move_count	
		print_board(board)
		print "KEY: awsd or q"
		key = raw_input()
		if key == 'a':
			c = move_y_minus(board)
			if c >= 0:
				break
			else:
				print "no move"
		elif key == 'd':
			c = move_y_plus(board)
			if c >= 0:
				break
			else:
				print "no move"
		elif key == 'w':
			c = move_x_minus(board)
			if c >= 0:
				break
			else:
				print "no move"
		elif key == 's':
			c = move_x_plus(board)
			if c >= 0:
				break
			else:
				print "no move"
		elif key == 'q':
			print "QUIT: total move:" , move_count
			does_quit = 1
			break
		else:
			print "WRONG key"
			pass
			
	if does_quit > 0:
		break
	else:
		# loop
		move_count = move_count + 1

#-------
# 探索



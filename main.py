'''
模仿游戏汉诺塔 https://zhangxiaoleiwk.gitee.io/h.html
'''
import pygame
import random

# 初始化
pygame.init()

# 时钟
clock = pygame.time.Clock()

# 游戏帧数
FPS = 60
# 游戏屏幕宽度, 高度
WIDTH  = 900
HEIGHT = 800

# 创建屏幕对象
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 游戏执行条件
run = True

# 常量
# 边框长度
BORDER = 1

# 颜色
BLACK      = (0, 0, 0)
RED        = (255, 0, 0)
WHITE      = (255, 255, 255)
GREY       = (221, 221, 221)
WHITE_GREY = (240, 240, 240)
GOLD       = (255, 255, 0)
GREEN      = (154, 205, 50)

# 透明
CLICK_GREEN = (204, 230, 204, 40)
CLICK_RED   = (255, 204, 204, 128)

# 游戏模式
MODE_CLASSIC   = 1   # 经典
MODE_ATHLETICS = 2   # 街机 竞技
MODE_DHYANA    = 3   # 禅
MODE_FASTEST   = 4   # 极速
MODE_RELEVOS   = 5   # 接力
MODE_RANK      = 6   # 排行榜


yahei10       = pygame.font.SysFont('microsoftjhengheiui', 30, bold=True)


a_tower = [ 1, 2, 3, 4, 5, 6, 7, 8 ]
b_tower = []
c_tower = []

clicked = []

FAILURE = False
fail_clicked = []

counter = 0


# 绘制文字
def draw_text(text, font, text_col, x, y, is_center=False):
	img = font.render(text, True, text_col)
	if is_center:
		rect = img.get_rect()
		rect.center = (x, y)
		screen.blit(img, rect)
	else:
		screen.blit(img, (x,y))


# 绘制柱子
def draw_pillar(x, y, size=8):

	# 高度
	h = HEIGHT//2//8
	# 半径
	r = h//2

	rect = pygame.Rect((0, 0, WIDTH//3 - 60 - ( (8 - size) % 8) * 25, h))

	rect.center = (x, y)

	# 绘制矩形
	pygame.draw.rect(screen, GREEN, rect)

	# 绘制左右两个圆
	pygame.draw.circle(screen, GREEN, rect.midleft, r)
	pygame.draw.circle(screen, GREEN, rect.midright, r)

	# 绘制中心白色的数字圆
	pygame.draw.circle(screen, WHITE, rect.center, r)

	# 绘制数字
	draw_text(str(size), yahei10, BLACK, rect.centerx, rect.centery, True)

# 绘制底座
def draw_base(rect, types):
	pygame.draw.rect(screen, WHITE_GREY, rect)
	pygame.draw.rect(screen, BLACK, rect, BORDER)

	r = pygame.Rect(rect)
	# 绘制数字
	draw_text(types, yahei10, BLACK, r.centerx, r.centery, True)

# 绘制塔
def draw_tower(x, y, tower, types):

	global FAILURE, counter

	# 绘制竖直柱子
	pygame.draw.rect(screen, GREY, (x-5, y - HEIGHT//2//8 * (10 - 1), 10, 65 * 8))

	length = len(tower)
	index = 8
	# 绘制水平柱子
	# 倒叙 和 8 匹配, 算出 高度
	for i in range(length, 0, -1):
		draw_pillar(
			x,
			y - HEIGHT//2//8 * (8 - index)  + (index - 1) * 2,
			tower[i-1]
		)
		index -= 1

	# 绘制底座
	draw_base((x-WIDTH//3//2, y + HEIGHT//2//8//2 + 20, WIDTH//3, HEIGHT//2//8), types)
	# pygame.draw.rect(screen, WHITE_GREY, (x-WIDTH//3//2, y + HEIGHT//2//8//2 + 20, WIDTH//3, HEIGHT//2//8))
	# pygame.draw.rect(screen, BLACK, (x-WIDTH//3//2, y + HEIGHT//2//8//2 + 20, WIDTH//3, HEIGHT//2//8), BORDER)

	# 绘制选中
	if clicked:
		if clicked[0] == 'a':
			i = 0
		if clicked[0] == 'b':
			i = 1
		if clicked[0] == 'c':
			i = 2
		s = pygame.Surface((WIDTH//3, 600), pygame.SRCALPHA)
		s.fill(CLICK_GREEN)
		screen.blit(s, (WIDTH//3*i, 100))
	# 选错
	elif not clicked:
		s = pygame.Surface((WIDTH//3, 600), pygame.SRCALPHA)
		if FAILURE:
			if fail_clicked[0] == 'a':
				i = 0
			if fail_clicked[0] == 'b':
				i = 1
			if fail_clicked[0] == 'c':
				i = 2
			s.fill(CLICK_RED)
			counter += 1
			if counter > FPS/3:
				counter = 0
				FAILURE = False
				fail_clicked.clear()

			screen.blit(s, (WIDTH//3*i, 100))


# 1 2
# 2 1
# -1 2
# 2 -1
# -1 -1
def switch(tower_b, tower_a, types):
	global FAILURE
	if len(tower_b) > 0 and len(tower_a) >= 0:
		if len(tower_a) == 0 or tower_b[0] < tower_a[0]:
			tower_a.insert(0, tower_b.pop(0))
		elif tower_b[0] > tower_a[0]:
			FAILURE = True
			fail_clicked.append(types)


while run:

	clock.tick(FPS)

	screen.fill(WHITE)

	for i, tower in enumerate([a_tower, b_tower, c_tower]):
		draw_tower(WIDTH//3//2 + WIDTH//3 * i, 600, tower, chr(ord('A') + i))

	# draw_tower(WIDTH//3//2, 600, a_tower, 'A')
	# draw_tower(WIDTH//3 + WIDTH//3//2, 600, b_tower, 'B')
	# draw_tower(WIDTH//3 + WIDTH//3 + WIDTH//3//2, 600, c_tower, 'C')

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				x, y = pygame.mouse.get_pos()
				types = x//(WIDTH//3)
				# 塔 A 被点击
				if types == 0:

					print('a click')

					if len(clicked) == 0:
						clicked.append('a')
					elif len(clicked) == 1:
						t = clicked.pop()

						if t == 'b':
							# if len(b_tower) > 0 and len(a_tower) >= 0:
							# 	if len(a_tower) == 0 or b_tower[0] < a_tower[0]:
							# 		a_tower.insert(0, b_tower.pop(0))
							# 	elif b_tower[0] > a_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('a')
							switch(b_tower, a_tower, 'a')
						elif t == 'c':
							# if len(c_tower) > 0 and len(a_tower) >= 0:
							# 	if len(a_tower) == 0 or c_tower[0] < a_tower[0]:
							# 		a_tower.insert(0, c_tower.pop(0))
							# 	elif c_tower[0] > a_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('a')
							switch(c_tower, a_tower, 'a')

						clicked.clear()
				# 塔 B 被点击
				elif types == 1:
					print('b click')
					if len(clicked) == 0:
						clicked.append('b')
					elif len(clicked) == 1:
						t = clicked.pop()
						if t == 'a':
							switch(a_tower, b_tower, 'b')
							# if len(a_tower) > 0 and len(b_tower) >= 0:
							# 	if len(b_tower) == 0 or a_tower[0] < b_tower[0]:
							# 		b_tower.insert(0, a_tower.pop(0))
							# 	elif a_tower[0] > b_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('b')
						elif t == 'c':
							switch(c_tower, b_tower, 'b')
							# if len(c_tower) > 0 and len(b_tower) >= 0:
							# 	if len(b_tower) == 0 or c_tower[0] < b_tower[0]:
							# 		b_tower.insert(0, c_tower.pop(0))
							# 	elif a_tower[0] > b_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('b')

						clicked.clear()
				# 塔 C 被点击
				elif types == 2:
					print('c click')
					if len(clicked) == 0:
						clicked.append('c')
					elif len(clicked) == 1:
						t = clicked.pop()
						if t == 'a':
							switch(a_tower, c_tower, 'c')
							# if len(a_tower) > 0 and len(c_tower) >= 0:
							# 	if len(c_tower) == 0 or a_tower[0] < c_tower[0]:
							# 		c_tower.insert(0, a_tower.pop(0))
							# 	elif a_tower[0] > c_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('c')
						elif t == 'b':
							switch(b_tower, c_tower, 'c')
							# if len(b_tower) > 0 and len(c_tower) >= 0:
							# 	if len(c_tower) == 0 or b_tower[0] < c_tower[0]:
							# 		c_tower.insert(0, b_tower.pop(0))
							# 	elif b_tower[0] > c_tower[0]:
							# 		FAILURE = True
							# 		fail_clicked.append('c')

						clicked.clear()

	pygame.display.update()

pygame.quit()

import numpy as np
import curses
from time import sleep

import sys

class World:

	def __init__(self, m, n, init_state = [], init_graphics = None):

		# init world
		self.size = (m, n)
		self.world = [0 for i in range(m*n)]

		if len(init_state) > 0:
			self.init_world(init_state)

		if init_graphics == None:
			self.stdscr = curses.initscr()
			curses.noecho()
			curses.cbreak()
			self.stdscr.keypad(True)
		else: 
			self.stdscr = init_graphics
		
		self.init_graphics()

	def init_world(self, init_state):

		for inst in init_state:
			y = inst[0]
			x = inst[1]

			if y > self.size[1] or x > self.size[0]:
				continue

			self.world[y*self.size[0]+x] = 1

	def init_graphics(self):

		curses.curs_set(0)
		begin_x = 0; begin_y = 0
		height = self.size[0]; width = self.size[1]
		self.win = curses.newwin(height, width, begin_y, begin_x)
		self.display()

	def terminate_graphics(self):

		curses.nocbreak()
		self.stdscr.keypad(False)
		curses.echo()
		curses.endwin()

	def update(self):

		w, h = self.size
		new_world = []
		
		for i, v in enumerate(self.world):

			acc = 0

			ymin = i/w >= 1.0
			ymax = i/w < h-1
			xmin = i%w
			xmax = i%w != w-1

			if ymin and xmin:
				acc += self.world[i-w] + self.world[i-w-1]
			elif ymin:
				acc += self.world[i-w]

			if ymax and xmax:
				acc += self.world[i+w] + self.world[i+w+1]
			elif ymax:
				acc += self.world[i+w]

			if xmin and ymax:
				acc += self.world[i-1] + self.world[i-1+w]
			elif xmin:
				acc += self.world[i-1]

			if xmax and ymin:
				acc += self.world[i+1] + self.world[i+1-w]
			elif xmax:
				acc += self.world[i+1]

			if not v and acc == 3:
				new_world.append(1)
			elif v and (acc == 2 or acc == 3):
				new_world.append(1)
			else:
				new_world.append(0)

		self.world = new_world


	def display(self):

		self.win.clear()
		
		for i, v in enumerate(self.world):
			if v:
				coordy = int(i / self.size[0])
				coordx = i % self.size[0]
				self.win.move(coordy, coordx)
				self.win.addch('0')

		self.win.refresh()

def main(stdscr):

	if len(sys.argv) > 1:
		ite = int(sys.argv[1])
	else:
		ite = 100

	init = [(25, 24), (25, 25), (23, 24), (24, 25), (24, 26)]
	
	world = World(50, 50, init, stdscr)
	sleep(0.5)

	for i in range(ite):
		world.update()
		world.display()
		sleep(0.5)

if __name__ == '__main__':

	curses.wrapper(main)

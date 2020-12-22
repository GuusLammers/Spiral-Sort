import pygame as pg
import math
import random
import time
pg.font.init()

# GLOBAL VARIABLES
WIDTH = 1001
HEIGHT = WIDTH
SLEEP_NUM = 1 

# FONT
myfont = pg.font.SysFont('Arial', 15)

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
RAINBOW = [(255, i, 0) for i in range(255)] + [(255 - 1, 255, 0) for i in range(255)] + [(0, 255, i) for i in range(255)] + [(0, 255 - i, 255) for i in range(255)] + [(i, 0, 255) for i in range(255)] + [(255, 0, 255 - i) for i in range(255)]     


# SET DISPLAY CAPTION, WIDTH, AND HEIGHT
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Spiral Sort')


class Dot:

	def __init__(self, width, radius, angle, center, colour=WHITE):
		self.width = width
		self.radius = radius
		self.angle = angle
		self.center = center
		self.pos = self.set_position()
		self.colour = colour

	def set_position(self):
		# initiate values for x, y position
		x_pos = 0	
		y_pos = 0

		
		# the code below splits the screen into four quadrants so that simple SOHCAHTOA can be used to compute dot position 	
		if self.angle <= 90:
			x_pos = self.radius * math.sin(math.radians(self.angle))
			y_pos = math.sqrt(self.radius ** 2 - x_pos ** 2)
			return (self.center + round(x_pos, 0), self.center - round(y_pos, 0))

		elif self.angle <= 180:
			x_pos = self.radius * math.cos(math.radians(self.angle - 180))
			y_pos = math.sqrt(self.radius ** 2 - x_pos ** 2)
			return (self.center + round(y_pos, 0), self.center + round(x_pos, 0))

		elif self.angle <= 270:
			x_pos = self.radius * math.sin(math.radians(self.angle))
			y_pos = math.sqrt(self.radius ** 2 - x_pos ** 2)
			return (self.center + round(x_pos, 0), self.center + round(y_pos, 0))

		else:
			x_pos = self.radius * math.cos(math.radians(self.angle - 270))
			y_pos = math.sqrt(self.radius ** 2 - x_pos ** 2)
			return (self.center - round(x_pos, 0),  self.center - round(y_pos, 0))	

	# update dots position		
	def update_position(self):
		self.pos = self.set_position()

	# sets dot colours to create rainbow	
	def set_colour(self, len_rainbow, radius_max):
		i = int(self.radius / radius_max * len_rainbow)
		self.colour = RAINBOW[i - 1]
			

class Spiral:

	def __init__(self, width, dot_width, win):
		self.dot_width = dot_width
		self.width = width
		self.center = self.width / 2
		self.radius = [i for i in range(1440)] 
		self.angle = [i for i in range(360)] + [i for i in range(360)] + [i for i in range(360)] + [i for i in range(360)]
		self.dots = [Dot(self.dot_width, self.radius[i]/3, self.angle[i], self.center) for i in range(len(self.radius))]
		self.sorting_list = [[self.dots[i], self.angle[i]] for i in range(len(self.angle))]
		self.win = win

	def shuffle(self):
		# shuffles dots by changing the angle they are plotted at
		for i in range(len(self.sorting_list)):
			j = random.randint(0, len(self.radius) - 1)
			self.sorting_list[i][0], self.sorting_list[j][0] = self.sorting_list[j][0], self.sorting_list[i][0]
			self.sorting_list[i][0].angle, self.sorting_list[j][0].angle = self.sorting_list[i][1], self.sorting_list[j][1]	
			self.sorting_list[i][0].update_position()
			self.sorting_list[j][0].update_position()

	def draw(self):
		# draw all dots to screen
		for dot in self.dots:
			x, y = dot.pos
			pg.draw.rect(self.win, dot.colour, (x, y, dot.width, dot.width))	

	def selection_sort(self, draw):
		# initialize start to zero
		start = 0
		# create a variable small which will hold the smallest value from a pass through the array, data stored (radius, index)
		small = (float('inf'), 0)

		# main sort loop, runs until start == 1
		while (len(self.sorting_list) - 1) - start > 1:
			# run through array from position start to end and record value with smallest radius
			for i in range(start, len(self.sorting_list)):
				if self.sorting_list[i][0].radius < small[0]:
					small = (self.sorting_list[i][0].radius, i)

			# swap object positions in array 		
			self.sorting_list[start][0], self.sorting_list[small[1]][0] = self.sorting_list[small[1]][0], self.sorting_list[start][0]	
			# update object angles to properly display spiral
			self.sorting_list[start][0].angle, self.sorting_list[small[1]][0].angle = self.sorting_list[start][1], self.sorting_list[small[1]][1]
			# update positions for both elements that were moved
			self.sorting_list[start][0].update_position()
			self.sorting_list[small[1]][0].update_position()

			# increment start and reset small
			start += 1	
			small = (float('inf'), 0)

			# update screen
			draw()
			
		# return when finished	
		return True

	def insertion_sort(self, draw):
		# iterate through entire list 	
		for i in range(1, len(self.sorting_list)):
			# set key to radius of the current dot being considered
			key = self.sorting_list[i][0]
			# create variable j wgich is 1 less than i
			j = i - 1

			# keep shifting array elements upwards until the correct position for key is found
			while j >= 0 and key.radius < self.sorting_list[j][0].radius:
				# shift element up
				self.sorting_list[j + 1][0] = self.sorting_list[j][0]
				# update position of shifted element
				self.sorting_list[j + 1][0].angle = self.sorting_list[j + 1][1]
				self.sorting_list[j + 1][0].update_position()
				# decrement j
				j -= 1

			# insert key 
			self.sorting_list[j + 1][0] = key	
			# update position of key
			self.sorting_list[j + 1][0].angle = self.sorting_list[j + 1][1]
			self.sorting_list[j + 1][0].update_position()
			# redraw screen
			draw()

	def quick_sort_partition(self, low, high, draw):
		# calculate index of smaller element
		i = low - 1
		# set pivot
		pivot = self.sorting_list[high][0].radius

		# iterate between low and high
		for j in range(low, high):
			# check if current elemets is smaller than pivot
			if self.sorting_list[j][0].radius < pivot:
				# increment index of small element
				i += 1
				self.sorting_list[i][0], self.sorting_list[j][0] = self.sorting_list[j][0], self.sorting_list[i][0]
					
				# update angles and positions	
				self.sorting_list[i][0].angle = self.sorting_list[i][1]
				self.sorting_list[j][0].angle = self.sorting_list[j][1]
				self.sorting_list[i][0].update_position()
				self.sorting_list[j][0].update_position()

				# update screen every four passes through loop
				if j % 4 == 0:
					draw()

		# switch list elements 			
		self.sorting_list[i + 1][0], self.sorting_list[high][0] = self.sorting_list[high][0], self.sorting_list[i + 1][0]

		# update angles and positions
		self.sorting_list[i + 1][0].angle = self.sorting_list[i + 1][1]
		self.sorting_list[high][0].angle = self.sorting_list[high][1]
		self.sorting_list[i + 1][0].update_position()
		self.sorting_list[high][0].update_position()

		return i + 1			

	def quick_sort(self, low, high, draw):	

		if low < high:
			# pi represents the partitioning index, this sets arr[p] in the correct place
			pi = self.quick_sort_partition(low, high, draw)

			# sort elements before and after partition
			self.quick_sort(low, pi - 1, draw)
			self.quick_sort(pi + 1, high, draw)

	def bubble_sort(self, draw):
		# iterate through list elements
		for i in range(len(self.sorting_list)):
			# top elements in place
			for j in range(0, len(self.sorting_list) - i - 1):
				# swap if element found is greater
				if self.sorting_list[j][0].radius > self.sorting_list[j + 1][0].radius:
					# switch elements
					self.sorting_list[j][0], self.sorting_list[j + 1][0] = self.sorting_list[j + 1][0], self.sorting_list[j][0]		

					# update angles and positions
					self.sorting_list[j][0].angle = self.sorting_list[j][1]
					self.sorting_list[j + 1][0].angle = self.sorting_list[j + 1][1]
					self.sorting_list[j][0].update_position()
					self.sorting_list[j + 1][0].update_position()

			# update screen
			if i % 2 == 0:		
				draw()	

	def shell_sort(self, draw):
		# calculte gap
		gap = len(self.sorting_list) // 2

		# main loop runs while gap is greater than zero
		while gap > 0:
			# iterate through items in list
			for i in range(gap, len(self.sorting_list)):
				# create temporary copy of index i
				temp = self.sorting_list[i][0]

				j = i

				# shift shift elements up until location for location found
				while j >= gap and self.sorting_list[j - gap][0].radius > temp.radius:
					# shift elements
					self.sorting_list[j][0] = self.sorting_list[j - gap][0]
					# update angle and position
					self.sorting_list[j][0].angle = self.sorting_list[j][1]
					self.sorting_list[j][0].update_position()

					j -= gap

				# insert temp into list at proper index	
				self.sorting_list[j][0] = temp			
				# update angle and position
				self.sorting_list[j][0].angle = self.sorting_list[j][1]
				self.sorting_list[j][0].update_position()

				# update screen every 5 timems through loop 
				if i % 6 == 0:
					draw()

			# integer divide gap		
			gap //= 2	


	def cocktail_sort(self, draw):
		# required variables
		swapped = True
		start = 0
		end = len(self.sorting_list) - 1

		# main loop
		while swapped:
			# reset swapped flag
			swapped = False

			# iterate through list left to right
			for i in range(start, end):
				if self.sorting_list[i][0].radius > self.sorting_list[i + 1][0].radius:
					# switch elements
					self.sorting_list[i][0], self.sorting_list[i + 1][0] = self.sorting_list[i + 1][0], self.sorting_list[i][0] 		
					swapped = True
					# update angle and position
					self.sorting_list[i][0].angle = self.sorting_list[i][1]
					self.sorting_list[i + 1][0].angle = self.sorting_list[i + 1][1]
					self.sorting_list[i][0].update_position()
					self.sorting_list[i + 1][0].update_position()

			# if nothing moved then the list is sorted		
			if not swapped:
				break
			# update screen
			draw()	

			# reset swapped flag
			swapped = False
			
			# end item is sorted, decrement end
			end -= 1	

			# iterate through list right to left 
			for i in range(end - 1, start - 1, -1):
				if self.sorting_list[i][0].radius > self.sorting_list[i + 1][0].radius:
					# switch elements
					self.sorting_list[i][0], self.sorting_list[i + 1][0] = self.sorting_list[i + 1][0], self.sorting_list[i][0] 		
					swapped = True
					# update angle and position
					self.sorting_list[i][0].angle = self.sorting_list[i][1]
					self.sorting_list[i + 1][0].angle = self.sorting_list[i + 1][1]
					self.sorting_list[i][0].update_position()
					self.sorting_list[i + 1][0].update_position()

			# start point sorted, increment start		
			start += 1		
			# update screen
			draw()

	def comb_sort(self, draw):
		# initialize gap
		gap = len(self.sorting_list)
		#intialize swapped
		swapped = True
		# main loop
		while gap != 1 or swapped:
			# calculate gap and set gap to one if it is less then one
			gap = (gap * 10) // 13
			if gap < 1:
				gap = 1
			# reset swapped flag
			swapped = False

			# compare all elements with current gap
			for i in range(len(self.sorting_list) - gap):
				if self.sorting_list[i][0].radius > self.sorting_list[i + gap][0].radius:
					# swap elements
					self.sorting_list[i][0], self.sorting_list[i + gap][0] = self.sorting_list[i + gap][0], self.sorting_list[i][0]  	
					swapped = True
					# update angles and positions
					self.sorting_list[i][0].angle = self.sorting_list[i][1]
					self.sorting_list[i + gap][0].angle = self.sorting_list[i + gap][1]
					self.sorting_list[i][0].update_position()
					self.sorting_list[i + gap][0].update_position() 
					# update screen every 3 passes through loop
					if i % 3 == 0:
						draw()				


class Label:

	def __init__(self):
		self.label_idle = myfont.render('SPACE - Run All Sorts', True, WHITE, (0, 0, 0))
		self.label_selection_sort = myfont.render('Selection Sort', True, WHITE, (0, 0, 0))
		self.label_insertion_sort = myfont.render('Insertion Sort', True, WHITE, (0, 0, 0))
		self.label_quick_sort = myfont.render('Quick Sort', True, WHITE, (0, 0, 0))
		self.label_bubble_sort = myfont.render('Bubble Sort', True, WHITE, (0, 0, 0))
		self.label_shell_sort = myfont.render('Shell Sort', True, WHITE, (0, 0, 0))
		self.label_cocktail_sort = myfont.render('Cocktail Sort', True, WHITE, (0, 0, 0))
		self.label_comb_sort = myfont.render('Comb Sort', True, WHITE, (0, 0, 0))
		self.label_shuffling = myfont.render('Shuffling', True, WHITE, (0, 0, 0))
		self.label_active = self.label_idle

	# show idle label
	def set_idle(self):
		self.label_active = self.label_idle

	# show selection sort label
	def set_selection_sort(self):
		self.label_active = self.label_selection_sort

	# show insertion sort label
	def set_insertion_sort(self):
		self.label_active = self.label_insertion_sort

	# show quick sort label
	def set_quick_sort(self):
		self.label_active = self.label_quick_sort

	# show bubble sort label
	def set_bubble_sort(self):
		self.label_active = self.label_bubble_sort

	# show shell sort label
	def set_shell_sort(self):
		self.label_active = self.label_shell_sort

	# show cocktail sort sort label
	def set_cocktail_sort(self):
		self.label_active = self.label_cocktail_sort

	# show comc sort label
	def set_comb_sort(self):
		self.label_active = self.label_comb_sort

	# show shuffling label
	def set_shuffling(self):
		self.label_active = self.label_shuffling									

	# draws labels on screen
	def draw(self, width, win):
		offset_x = width - self.label_active.get_width() - 20
		offset_y = width - self.label_active.get_height() - 20
		win.blit(self.label_active, (offset_x, offset_y))
		


# DRAW OUT SCREEN
def update_win(win, width, spiral, label):
	# make background black
	win.fill(BLACK)

	# redraw spiral
	spiral.draw()

	# redraw label
	label.draw(width, win)

	# update display		
	pg.display.update()			


# MAIN FUNCTION, CONTROLLS MAIN LOOP
def main(win, width):

	s = Spiral(width, 2, win)

	label = Label()

	for dot in s.sorting_list:
		dot[0].set_colour(len(RAINBOW), max(s.radius)/3)

	# runs main loop until turned false
	run = True

	# controlls wheter the algorithms are running
	started = False

	# main loop
	while run:
		# draw screen
		update_win(win, width, s, label)
		
		# check through all events
		for event in pg.event.get():
			# allows user to close app
			if event.type == pg.QUIT:
				run = False

			if started:
				continue	

			# if key pressed		
			if event.type == pg.KEYDOWN:
				# if space is pressed run all sorting algorithms algoritm
				if event.key == pg.K_SPACE and not started:
					started = True

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set selection sort label
					label.set_selection_sort()
					# run selection sort
					s.selection_sort(lambda: update_win(win, width, s, label))		

					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set selection sort label
					label.set_insertion_sort()
					# run selection sort
					s.insertion_sort(lambda: update_win(win, width, s, label))		
	
					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set quick sort label
					label.set_quick_sort()
					# run quick sort
					s.quick_sort(0, len(s.sorting_list) - 1, lambda: update_win(win, width, s, label))

					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set bubble sort label
					label.set_insertion_sort()
					# run bubble sort
					s.bubble_sort(lambda: update_win(win, width, s, label))

					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set shell sort label
					label.set_shell_sort()
					# run shell sort
					s.shell_sort(lambda: update_win(win, width, s, label))

					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set cocktail sort label
					label.set_cocktail_sort()
					# run cocktail sort
					s.cocktail_sort(lambda: update_win(win, width, s, label))

					time.sleep(1)

					# set shuffling label
					label.set_shuffling()
					for i in range(SLEEP_NUM):
						# shuffle dots
						s.shuffle()
						# update window
						update_win(win, width, s, label)
						# wait for 0.25 seconds
						time.sleep(0.25)

					time.sleep(1)	

					# set comb sort label
					label.set_insertion_sort()
					# run comb sort
					s.comb_sort(lambda: update_win(win, width, s, label))

					# done
					label.set_idle()
					started = False

				if event.key == pg.K_1 and not started:
					started = True
					s.selection_sort(lambda: update_win(win, width, s, label))	
					started = False

				if event.key == pg.K_2 and not started:
					started = True
					s.insertion_sort(lambda: update_win(win, width, s, label))		
					started = False

				if event.key == pg.K_3 and not started:
					started = True
					s.quick_sort(0, len(s.sorting_list) - 1, lambda: update_win(win, width, s, label))		
					started = False	

				if event.key == pg.K_4 and not started:
					started = True
					s.bubble_sort(lambda: update_win(win, width, s, label))		
					started = False		

				if event.key == pg.K_5 and not started:
					started = True
					s.shell_sort(lambda: update_win(win, width, s, label))		
					started = False		

				if event.key == pg.K_6 and not started:
					started = True
					s.cocktail_sort(lambda: update_win(win, width, s, label))		
					started = False			

				if event.key == pg.K_7 and not started:
					started = True
					s.comb_sort(lambda: update_win(win, width, s, label))		
					started = False		
					
	# quit			
	pg.quit()			

# main loop
main(win, WIDTH)	








#Darwindrian: Prototype
#Genetic related module
#Related article: Cyber-Genetic Neo-Plasticism
#Current status: theoritical development
#Author: Jian Yin Shen, ANU

import random
import math
from darwindrian_color_sample import *

#initial arguments
#50%
CROSS_POINT = 0.5
COMPLEXITY = 4
POPULATION = 100


#Chromosome pieces

def switch(point):
	temp = point.y
	point.y = point.x
	point.x = temp
	return point

def uneven(point):
	point.x = point.x /2
	point.y = point.y*2
	return point

def multi(point):
	a = point.x * point.y
	b = 1
	if point.y <> 0.0:
		b = point.x/point.y
		
	point.x = a
	point.y = b
	return point

def balance(point):
	a = (point.x + point.y)/2
	b = math.sqrt(point.x * point.y)
	point.x = a
	point.y = b
	return point

def get_chromo_group_A():
	lengh = 8
	result = []
	for i in range(0, lengh):
		result.append(random.choice([switch,uneven,multi, balance]))
	return result

def get_chromo_group_B():
	length = 4*COMPLEXITY
	result = []
	for i in range(0, length):
		result.append(random.choice(['East','North','West','South',None, None]))
	return result

	
def cross_over(a, b):
	cp = int(len(a)*CROSS_POINT)
	_new = a[0:cp] + b[cp:]
	return _new
	
#Very simple class for point description
class point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		

def test():
	a = get_chromo_group_B()
	b = get_chromo_group_B()
	print cross_over(a,b)
	
test()

class Chromosome:
	
	def __init__(self, \
		g1 = get_chromo_group_A(), \
		g2 = get_chromo_group_B(), \
		g3 = [], \
		g4 = []):
		
		self.__g1 = g1
		self.__g2 = g2
		self.__g3 = g3
		self.__g4 = g4
		
		#fitness value from 1~10
		self.fitness = 5
		
		self.complexity = 3 #default
		self.loop = 4 
		#Possibility value for each node type to have 1 more line
		self.__structure_dist = \
			{'Cross':0.0, 'Nodal':0.2, 'Terminal':0.9, 'OnLine':0.3, 'RightAngle':1.0, 'Initial':1.0}
	
			
	def g1(self):
		return self.__g1
		
	def g2(self):
		return self.__g2
			
	def have_more_line(self, node):
		probability = self.__structure_dist[node.get_type()]
		return luck(probability)
	
	#return value structure:
	#([x, y, width, height],color)
	#impl
	def pick_rectangles(self, all_avail):
		result = []
		if all_avail == []:
			print 'warning: no rectangles found'
			return []
		for i in range(0,2):
			result.append((random.choice(all_avail),random.choice([RED, BLUE, YELLOW])))
			
		return result
		
	def cross_over(self, another):
		_g1 = cross_over(self.g1(), another.g1())
		_g2 = cross_over(self.g2(), another.g2())
		return Chromosome(_g1, _g2)

class EvolutionManager:
	
	def __init__(self):
		self.__current = [];
		self.__history = [];
		
	
	def new_generation(self):
		self.__current = []
		for i in range(0, POPULATION):
			self.__current.append(Chromosome())
	
	def next_generation(self):
		_next = []
		if(len(self.__current) <= 1):
			print "No more samples in current generation"
			return
			
		for i in range(-1, len(self.__current)-1):
			_next.append(self.__current[i].cross_over(self.__current[i+1]))
		
		self.__history.append(self.__current)
		self.__current = _next
	
	def evaluate():
		pass
	
	def sample(self):
		return self.__current[0]
	
class ChromosomeManager:
	def __init__(self):
		pass
		
	def get_next_chromosome(self):
		#impl
		return Chromosome()
		
#static instance
ChromoManager = ChromosomeManager()

#Util methods
def luck(percentage):
	return random.uniform(0,1) <= percentage

#return value structure: list of:
#[x, y, width, height]
def search_rectangles(nodes):
	found = []
	keys = nodes.keys()
	keys.sort()
	
	def find_rec_between_row(row1, row2):
		result = []
		for p_i in range(0, len(row1) - 1):
			#should include rectangles has several points wide?
			p1 = row1[p_i]
			p2 = row1[p_i+1]
			p3_a = filter(lambda p, p2 = p2: p2.x == p.x, row2)
			p4_a = filter(lambda p, p1 = p1: p1.x == p.x, row2)
			if p3_a == [] or p4_a == []:
				continue
			else: #found
				p3 = p3_a[0]
				result.append([p1.x,p1.y,p2.x-p1.x,p3.y-p2.y])
		return result
		
	#print 'nodes:',nodes
	#print 'rows:',keys
	#find possible rectangle, clockwise
	#Guarenteed one row has at least 2 elements
	#guarenteed has at least 2 columns
	for key_i in range(0, len(keys)-1):
		#print 'current row:',key_i
		row1 = nodes[keys[key_i]]
		for rest_i in range(key_i+1, len(keys)):
			row2 = nodes[keys[rest_i]]
			found += find_rec_between_row(row1, row2)
		
	print 'rec found:',len(found)
	return found
	
#Global instances
evolution = EvolutionManager()

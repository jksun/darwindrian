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
POPULATION = 20



def scale_down(dist):
	_all = reduce(lambda x,y: x+y, dist.values())
	for k in dist.keys():
		
		dist[k] = float(dist[k])/float(_all)
	
	return dist

#simple random point on intialization
class RandomPoint:
  	def __init__(self):
		self.x = random.randint(1,100)
		self.y = random.randint(1,100) 
	
	def scale_upto(self, max_x, max_y):
	  	self.x = int((self.x/100.0)*max_x)
		self.y = int((self.y/100.0)*max_y)
	
class Chromosome:
	
	def __init__(self):
		
		#fitness value from 1~10
		self.color_fitness = 5.0
		self.structure_fitness = 5.0
		self.survival_chance = 1
		self.complexity = 3 #Fixed
		self.loop = 4  #fixed
		
		self.direction_dist = \
			{'East': self.__rand_d(),'West':self.__rand_d(),'South':self.__rand_d(),'North':self.__rand_d()}

		self.structure_dist = \
			{'Cross':0.0, 'Nodal':0.2, 'Terminal':0.9, 'OnLine':0.3, 'RightAngle':1.0, 'Initial':1.0}
		#Color distribution
		self.color_dist = {RED: random.uniform(1,10), BLUE: random.uniform(1,10), YELLOW: random.uniform(1,10)}
		self.origin_points = [RandomPoint(), RandomPoint(), RandomPoint()]
	
	def overall_fitness(self):
		return (self.color_fitness+self.structure_fitness)/2.0
		
	def __rand_d(self):
		v = []
		for i in range(0, self.loop):
			v.append(random.choice(range(1,11)))
		return v
	
	#loop: 0~3
	def get_direction_by_loop(self, hvpoint, loop):
		local_dist = self.direction_dist.copy()
		for k in local_dist.keys():
			if k not in hvpoint.get_aval_direction():
				del(local_dist[k])
			else:
				local_dist[k] = local_dist[k][loop]
		scale_down(local_dist)
		#randomly choose a direction, according to their probability of being chosen
		while 1:
			unordered = local_dist.keys()
			random.shuffle(unordered)
			for k in unordered:
				p = local_dist[k]
				if luck(p):
					return k
	
	def map_directions(self, hvpoint):
		options = hvpoint.get_aval_direction()
		for k in self.direction_dist.keys():
			pass
		
	def have_more_line(self, node):
		probability = self.structure_dist[node.get_type()]
		return luck(probability)
	
	#return value structure:
	#([x, y, width, height],color)
	#impl
	def pick_rectangles(self, all_avail):
		result = []
		if all_avail == []:
			print 'warning: no rectangles found'
			return []
		
		scale_down(self.color_dist)
		while 1:
			for k in self.color_dist.keys():
				p = self.color_dist[k]
				if luck(p):	
					result.append((random.choice(all_avail), k))
				if len(result) >=2:
					return result
		#for i in range(0,2):
		#	result.append((random.choice(all_avail),random.choice([RED, BLUE, YELLOW])))
			
		#return result
		
	def cross_over(self, another):
		_new = Chromosome()
		#cross direction distribution
		_d_dist = self.direction_dist.copy()
		for k in _d_dist.keys():
			_d_dist[k][2:] = another.direction_dist[k][2:]
		#cross color distribution
		_c_dist = self.color_dist.copy()
		#randomly choose a color  probability value to be replaced by another chromosome
		chosen = random.choice(_c_dist.keys())
		_c_dist[chosen] = another.color_dist[chosen]
		
		_new.direction_dist = _d_dist
		_new.color_dist = _c_dist
		_new.origin_points = self.origin_points[0:2]+another.origin_points[2:]
		return _new
		
class EvolutionManager:
	
	def __init__(self):
		self.__current = [];
		self.__history = [];
		self.__initial = 1
	
	def new_generation(self):
		self.__initial = 0
		self.__current = []
		for i in range(0, POPULATION):
			self.__current.append(Chromosome())
		return self.__current
		
	def next_generation(self):
		if self.__initial:
			return self.new_generation()
			
		_next = []
		if(len(self.__current) <= 1):
			print "No more samples in current generation"
			return
		
		#sort chromosomes on fitness value
		self.__current.sort(lambda a,b : cmp(a.overall_fitness(), b.overall_fitness()))
		self.__current.reverse()
		max_survive = self.__current[0].overall_fitness()
		
		_next.append(self.__current[0])
		for i in range(0, len(self.__current)):
			#Determines whether this chromosome should reproduce
			#The first one should always survive, for it has the most high fitness value
			#The first one is unchanged and preserved on next generation (elite)
			#The last one is discarded, for it has the lowest fitness value
			
			if luck(self.__current[i].overall_fitness()/max_survive) and i != len(self.__current)-1:
				_next.append(self.__current[i].cross_over(self.__current[i+1]))
				
		self.__history = self.__current
		self.__current = _next
		return self.__current
		

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

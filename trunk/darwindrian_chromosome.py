#Darwindrian: Prototype
#Generic related module
#Related article: Cyber-Genetic Neo-Plasticism
#
#Author: Jian Yin Shen, ANU

import random
from darwindrian_color_sample import *

class Chromosome:
	def __init__(self):
		self.complexity = 3 #default
		self.loop = 4 
		#Possibility value for each node type to have 1 more line
		self.__structure_dist = \
			{'Cross':0.0, 'Nodal':0.2, 'Terminal':0.9, 'OnLine':0.3, 'RightAngle':1.0, 'Initial':1.0}
	
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

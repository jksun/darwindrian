#Darwindrian: Prototype
#Generic related module
#Related article: Cyber-Genetic Neo-Plasticism
#
#Author: Jian Yin Shen, ANU

import random

class Chromosome:
	def __init__(self):
		self.complexity = 3 #default
		self.loop = 4 
		#Possibility value for each node type to have 1 more line
		self.__structure_dist = \
			{'Cross':0.0, 'Nodal':0.2, 'Terminal':0.8, 'OnLine':0.3, 'RightAngle':1.0, 'Initial':1.0}
		pass
	
	def have_more_line(self, node):
		probability = self.__structure_dist[node.get_type()]
		return luck(probability)
		
	def next_rectangle(self, nodes):		
		keys = nodes.keys()
		keys.sort()
		
		#find possible rectangle, clockwise
		return None
	
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

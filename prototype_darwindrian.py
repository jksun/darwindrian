#Darwindrian: Prototype
#2D related module
#Related article: Cyber-Genetic Neo-Plasticism
#
#Author: Jian Yin Shen, ANU
#
#require: JPython + Swing

from javax import swing
from java import awt
from java.awt import geom
from java.awt.print import Printable

from darwindrian_chromosome import *

#debug flag
debug = 1

#Color samples from Mondrian's painting
WHITE = awt.Color(0.9,0.9,0.88)
BLUE = awt.Color(0.05,0.31,0.62)
YELLOW = awt.Color(0.96,0.83,0.28)
RED = awt.Color(0.66,0.13,0.17)
BLACK = awt.Color(0.06,0.06,0.06)

class HVLine(awt.geom.Line2D.Double):
	directions = ['East','West','South', 'North']
	def __init__(self,sp, direction, length):
		awt.geom.Line2D.Double.__init__(self)
		epx = sp.x
		epy = sp.y
		if direction == 'East':
			epx = sp.x + length
		elif direction == 'West':
			epx = sp.x - length
		elif direction == 'South':
			epy = sp.y + length
		elif direction == 'North':
			epy = sp.y - length
		self.setLine(sp.x,sp.y,epx,epy)
		self.__direction = direction
		self.__origin_point = sp
	
	def get_direction(self):
		return self.__direction
	
	def get_origin_point(self):
		return self.__origin_point
		
class HVPoint(awt.Point):
	#Cross: 4 lines connected
	#Nodal: 3 lines already connected
	#Terminal: 1 line connected
	#Online: 2 line connected and they form 180 degree
	#RightAngle 2 line connected and they form 90 degree
	#Initial: No line connected
	point_type = ('Cross', 'Nodal', 'Terminal', 'OnLine', 'RightAngle', 'Initial')
	
	def __init__(self, x, y):
		awt.Point.__init__(self, x, y)
		self.__options = ['East','West','North', 'South']
	
	def get_aval_direction(self):
		return self.__options
	
	def emit_on_direction(self, direction):
		if direction not in self.__options:
			raise 'direction not available'
		else:
			self.__options.remove(direction)
			
	def get_type(self):
		if len(self.__options) == 4:
			return 'Initial'
		elif len(self.__options) == 3:
			return 'Terminal'
		elif len(self.__options) == 2:
			self.__options.sort()
			if self.__options <> ['East', 'West'] and self.__options <> ['North', 'South']:
				return 'RightAngle'
			else:
				return 'OnLine'
		elif len(self.__options) == 1:
			return 'Nodal'
		else:
			return 'Cross'
	
	def __repr__(self):
		return '('+str(self.x)+', '+str(self.y)+')'
	
	def __add__(self, p):
		if p.__class__ == [].__class__:
			return HVPoint(self.x + p[0], self.y + p[1])

class Mondrian:	
	'''He who paints'''
	def __init__(self):
		self.__points = []
		self.__rectangle = {}
		self.__lines = {}
		self.__chromosome = None
			
	def __find_end_lengths(self, s_p, direction):
		endlengths = None
		candidate_lines = None
		test_line = None
		length = max(self.__size.width,self.__size.height)		
		test_line = HVLine(s_p, direction, length)		
		test_intersect = lambda l1, l2 = test_line: l2.intersectsLine(l1) \
			and l1.get_origin_point() <> l2.get_origin_point()
		candidate_lines = filter(test_intersect, self.get_all_lines())

		if direction in ['East','West']:
			endlengths = map(lambda l, s_p = s_p: abs(l.getX1() - s_p.x), candidate_lines)
		else:
			endlengths = map(lambda l, s_p = s_p: abs(l.getY1() - s_p.y), candidate_lines)
			
		return endlengths
	
	def __add_rectangles(self, nodes = None):
		if nodes == None:
			nodes = self.get_all_nodes()
		rec_color = self.__chromosome.next_rectangle(nodes)
		if rec_color == None:
			return
		else:
			self.__rectangle[rec_color[0]] = rec_color[1]
			self.__addRectangles(nodes)
		
	def __fill_color_rectangle(self):
		pass
			
	def __add_original_points(self):
		print 'complexity:',self.__chromosome.complexity
		for i in range(0, self.__chromosome.complexity):
			x = random.randint(1,self.__size.width)
			y = random.randint(1,self.__size.height)
			p = HVPoint(x, y)
			self.__points.append(p)
			print 'generated point:',p
			#Is sorting needed?
			self.__points.sort((lambda p1, p2: p1.x - p2.x))

	def __add_lines(self):
		for l in range(0,self.__chromosome.loop):
			random.shuffle(self.__points)
			for p in self.__points:
				if self.__chromosome.have_more_line(p):
					self.__generate_one_line(p)
							
		#eliminate all rightAngles
		r_a = filter(lambda p: p.get_type() == 'RightAngle', self.__points)
		print 'right angle:',len(r_a)
		for right_angle_p in r_a:
			self.__generate_one_line(right_angle_p)
			
	def __generate_one_line(self, op):
		d = random.choice(op.get_aval_direction())
		op.emit_on_direction(d)
		
		endlengths = self.__find_end_lengths(op, d)
		newline = HVLine(op,d,random.choice(endlengths))
		
		print'generated line:',d,"-",op.x,op.y
		
		self.__lines[d].append(newline)
			
	def refresh(self, dimension = None):
		if dimension != None:
			self.__size = dimension

		self.compose(ChromoManager.get_next_chromosome())
	
	def __load_borderline(self):
		d = 'East'
		self.__lines[d].append(HVLine(HVPoint(0,0),d,self.__size.width))
		self.__lines[d].append(HVLine(HVPoint(0,self.__size.height),d,self.__size.width))
		d = 'South'
		self.__lines[d].append(HVLine(HVPoint(0,0),d,self.__size.height))
		self.__lines[d].append(HVLine(HVPoint(self.__size.width,0),d,self.__size.height))
		
	#refine
	def compose(self, chromosome):
		self.__chromosome = chromosome
		self.__points = []
		self.__rectangle.clear()
		for direction in HVLine.directions:
			self.__lines[direction] = []
		self.__load_borderline()
		
		self.__add_original_points()
		self.__add_lines()
		self.__add_rectangles()
	
	def get_border_lines(self):
		east = self.__lines['East']
		east.sort(lambda l1,l2: int(l1.getY1() - l2.getY1()))
		south = self.__lines['South']
		south.sort(lambda l1,l2: int(l1.getX1() - l2.getX1()))
		return [east[0],east[-1],south[0],south[-1]]
	
	def get_all_lines(self):
		result = []
		for i in self.__lines.values():
			result += i
		return result
		
	def get_all_nodes(self):
		'''load all nodes in the graph. May or may not include original point'''
		points = {}
		all = self.get_all_lines()
		for l in all:
			for l2 in all:
				if l.intersectsLine(l2) and l <> l2:
					p = None
					if l in self.__lines['East'] or l in self.__lines['West']:
						p = geom.Point2D.Double(l2.getX1(),l.getY1())
					else:
						p = geom.Point2D.Double(l.getX1(),l2.getY1())
					#index by y value
					if not points.has_key(p.y):
						points[p.y] = []
					if p not in points[p.y]:
						points[p.y].append(p)
		
		#each 'row' sort by x value
		for row in points.values():
			row.sort(lambda p1, p2: int(p1.x - p2.x))			
		return points
							
	#Borderlines not included
	def get_lines(self):
		borders = self.get_border_lines()
		return filter(lambda l, b = borders: l not in b, self.get_all_lines())
	
	def get_rectangles(self):
		return self.__rectangle.items()
	
	def get_debug_lines(self):
		return map(lambda p: geom.Line2D.Double(0,0,p.x,p.y), \
			reduce(lambda s1, s2: s1+s2, self.get_all_nodes().values()))
		
class Canvas(swing.JPanel):
	def __init__(self):
		swing.JPanel.__init__(self)
		global mondrian_instance
		self.preferredSize = awt.Dimension(480,480)
		self.background = WHITE
		self.__line_stroke = awt.BasicStroke(9)
		self.__rec_stroke = awt.BasicStroke()
		mondrian_instance.refresh(self.preferredSize)
		
	def paint(self,g):
		global mondrian_instance
		swing.JPanel.paint(self,g)
		#draw rectangles
		g.setStroke(self.__rec_stroke)
		for r in mondrian_instance.get_rectangles():
			g.setColor(r[1])
			g.fill(r[0])
		#draw lines
		g.setStroke(self.__line_stroke)
		for l in mondrian_instance.get_lines():
			g.setColor(BLACK)
			g.draw(l)
		
		#debug line
		if not debug:
			return
			
		g.setStroke(self.__rec_stroke)
		for l in mondrian_instance.get_debug_lines():
			g.setColor(awt.Color.GRAY)
			g.draw(l)
		
		g.setStroke(self.__line_stroke)
		for l in mondrian_instance.get_border_lines():
			g.setColor(awt.Color.RED)
			g.draw(l)
			
class ControlPane(swing.JPanel,awt.event.ActionListener):
	def __init__(self):
		swing.JPanel.__init__(self)
		self.__next_b = swing.JButton('next')
		self.__next_b.addActionListener(self)
		self.layout = awt.FlowLayout(awt.FlowLayout.RIGHT)
		self.add(self.__next_b)
		
	def actionPerformed(self, e):
		global mondrian_instance
		if e.getSource() == self.__next_b:
			mondrian_instance.refresh()
			self.getParent().repaint()
		
#global singleton instance
mondrian_instance = Mondrian()

def start_window():
	root = swing.JFrame(title = 'Darwindrian - prototype')
	canvas = Canvas()
	control = ControlPane()
	
	content = swing.JPanel(layout = awt.BorderLayout())
	content.add(canvas, awt.BorderLayout.CENTER)
	content.add(control, awt.BorderLayout.SOUTH)
	
	root.contentPane = content
	root.visible = 1
	root.resizable = 0
	root.defaultCloseOperation = swing.JFrame.EXIT_ON_CLOSE
	root.pack()
			
def testing():
	if __name__ == '__main__':
		start_window()
		
#run
testing()

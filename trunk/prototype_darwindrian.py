#Darwindrian: Prototype
#Related article: Cyber-Genetic Neo-Plasticism
#
#Author: Jian Yin Shen, ANU
#
#require: JPython + Swing
import random

from javax import swing
from java import awt
from java.awt import geom
from java.awt.print import Printable

#debug flag
debug = 0

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
		
#OPoint stands for OriginalPoint
class OPoint(awt.Point):
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
	
	def __add__(self, p):
		if p.__class__ == [].__class__:
			return OPoint(self.x + p[0], self.y + p[1])

class Mondrian:
		
	def luck(self,percentage):
		return random.uniform(0,1) <= percentage
	
	def __init__(self):
		self.__points = []
		self.__rectangle = {}
		self.__line_vertical = []
		self.__line_horizontal = []
			
	def __find_end_lengths(self, s_p, direction):
		endlengths = None
		candidate_line = None
		test_line = None
		length = max(self.__size.width,self.__size.height)
		
		test_line = HVLine(s_p, direction, length)
		
		test_intersect = lambda l1, l2 = test_line: l2.intersectsLine(l1) and l1.get_origin_point() <> l2.get_origin_point()
		
		if direction in ['East','West']:
			candidate_line = filter(test_intersect, self.__line_vertical)
			endlengths = map(lambda l, s_p = s_p: abs(l.getX1() - s_p.x), candidate_line)
		else:
			candidate_line = filter(test_intersect, self.__line_horizontal)
			endlengths = map(lambda l, s_p = s_p: abs(l.getY1() - s_p.y), candidate_line)
			
		return endlengths
	
	def __add_rectangles(self):
		print 'add rectangle not implemented'	
		
	def __fill_color_rectangle(self):
		pass
			
	def __add_original_points(self, complexity):
		for i in range(0, complexity):
			x = random.randint(1,self.__size.width)
			y = random.randint(1,self.__size.height)
			p = OPoint(x, y)
			self.__points.append(p)
			print 'generated point: (',p.x,p.y,')'
			#Is sorting needed?
			self.__points.sort((lambda p1, p2: p1.x - p2.x))

	def __add_lines(self, loop = 5):
		for l in range(0,loop):
			random.shuffle(self.__points)
			for p in self.__points:
				if p.get_type() == 'Initial':
					self.__generate_one_line(p)
				elif p.get_type() == 'Terminal' and self.luck(0.95):
					self.__generate_one_line(p)
				elif p.get_type() == 'OnLine' and self.luck(0.4):
					self.__generate_one_line(p) 
				elif p.get_type() == 'Nodal' and self.luck(0.1):
					self.__generate_one_line(p)
				elif p.get_type() == 'Cross':
					continue
							
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
		
		if d in ['East','West']:
			self.__line_horizontal.append(newline)
		else:
			self.__line_vertical.append(newline)
			
	def refresh(self, dimension = None):
		if dimension != None:
			self.__size = dimension

		#Border lines
		self.compose()
	
	def __load_borderline(self):
		self.__line_horizontal += [HVLine(OPoint(0,0),'East',self.__size.width)]
		self.__line_horizontal += [HVLine(OPoint(0,self.__size.height),'East',self.__size.width)]
		self.__line_vertical += [HVLine(OPoint(0,0),'South',self.__size.height)]
		self.__line_vertical += [HVLine(OPoint(self.__size.width,0),'South',self.__size.height)]
		
	#refine
	def compose(self):
		self.__points = []
		self.__rectangle.clear()
		self.__line_vertical = []
		self.__line_horizontal = []
		self.__load_borderline()
		
		complexity = 3
		print 'composing, complexity =',complexity
		self.__add_original_points(complexity)
		self.__add_lines()
		self.__add_rectangles()
	
	def get_border_lines(self):
		self.__line_vertical.sort(lambda l1,l2: int(l1.getX1() - l2.getX1()))
		self.__line_horizontal.sort(lambda l1,l2: int(l1.getY1() - l2.getY1()))
		
		return [self.__line_vertical[0],self.__line_vertical[-1],self.__line_horizontal[0],self.__line_horizontal[-1]]
	
	#Borderlines not included
	def get_lines(self):
		borders = self.get_border_lines()
		return filter(lambda l, b = borders: l not in b, self.__line_vertical + self.__line_horizontal)
	
	def get_rectangles(self):
		return self.__rectangle.items()
	
	def get_debug_lines(self):
		return map(lambda p: geom.Line2D.Double(0,0,p.x,p.y), self.__points)
		
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

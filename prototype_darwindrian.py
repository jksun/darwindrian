#!/usr/bin/jython

#Darwindrian: Prototype
#2D related module
#Related article: Cyber-Genetic Neo-Plasticism
#
#Author: Jian Yin Shen, ANU
#
#require: JPython + Swing

from javax import swing
from java import awt
from java import io
from java.awt import geom
from java.awt import image
from java.awt.event import *
from javax.imageio import ImageIO
from java.lang import NullPointerException
from darwindrian_chromosome import *
from darwindrian_color_sample import *

#debug flag
debug = 0

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
			if self.__options <> ['East', 'West'] \
				and self.__options <> ['North', 'South']:
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

class MondrianGraph:
	def __init__(self):
		self.rectangles = None
		self.lines = None
			
class Mondrian:	
	'''He who paints'''
	def __init__(self):
		self.__points = []
		self.__rectangles = {}
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
	
	def __add_rectangles(self):
		nodes = self.get_all_nodes()
		avail = search_rectangles(nodes)
		picked = self.__chromosome.pick_rectangles(avail)
		for r in picked:
			rec = geom.Rectangle2D.Double(*r[0])
			color = r[1]
			self.__rectangles[rec] = color
					
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
		
		graph = MondrianGraph()
		graph.rectangles = self.get_rectangles()
		graph.lines = self.get_lines()
		return graph
	
	def __load_borderline(self):
		d = 'East'
		self.__lines[d].append(HVLine(HVPoint(0,0),d,self.__size.width))
		self.__lines[d].append(HVLine(HVPoint(0,self.__size.height),d,self.__size.width))
		d = 'South'
		self.__lines[d].append(HVLine(HVPoint(0,0),d,self.__size.height))
		self.__lines[d].append(HVLine(HVPoint(self.__size.width,0),d,self.__size.height))
		
	#refine
	def compose(self, chromosome, dimension = None):
		if dimension != None:
			self.__size = dimension
			
		self.__chromosome = chromosome
		self.__points = []
		self.__rectangles.clear()
		for direction in HVLine.directions:
			self.__lines[direction] = []
		self.__load_borderline()
		
		self.__add_original_points()
		self.__add_lines()
		self.__add_rectangles()
		
		graph = MondrianGraph()
		graph.rectangles = self.get_rectangles()
		graph.lines = self.get_lines()
		return graph
	
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
				if l.intersectsLine(l2) and l <> l2: #and l.get_origin_point() <> l2.get_origin_point():
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
		return self.__rectangles.items()
	
	def get_debug_lines(self):
		return map(lambda p: geom.Line2D.Double(0,0,p.x,p.y), \
			reduce(lambda s1, s2: s1+s2, self.get_all_nodes().values()))

#Over is Darwindrian drawing impl (high tech)
#Seperate ----------------------------------------------------------------------
#The following is Swing programming (low tech)

class MiniView(swing.JScrollPane):
	
	class __Renderer(swing.ListCellRenderer):
		def __init__(self):
			pass
			
		def getListCellRendererComponent(self, ls, value, index, selected, cellHasFocus):
			#Wrapper pane
			wrapper = swing.JPanel(layout = awt.FlowLayout(awt.FlowLayout.CENTER))
			wrapper.add(value)
			wrapper.preferredSize = awt.Dimension(100,90)
			
			if selected:
				wrapper.background = awt.Color.GRAY
				
			return wrapper
	
	class __MiniMondrian(swing.JPanel):
		def __init__(self, graph):
			swing.JPanel.__init__(self)
			self.preferredSize = awt.Dimension(80,80)
			self.background = WHITE
			self.__graph = graph
			
		def paint(self,g):
			swing.JPanel.paint(self, g)
			
			canvas_x = float(gui_canvas.preferredSize.width)
			canvas_y = float(gui_canvas.preferredSize.height)
			mini_x = float(self.preferredSize.width)
			mini_y = float(self.preferredSize.height)
			g.scale(mini_x/canvas_x, mini_y/canvas_y)
			
			#g.setStroke(self.__rec_stroke)
			for r in self.__graph.rectangles:
				g.setColor(r[1])
				g.fill(r[0])
				#draw lines
				#g.setStroke(self.__line_stroke)
			for l in self.__graph.lines:
				g.setColor(BLACK)
				g.draw(l)
			
			
	def __init__(self):
		swing.JScrollPane.__init__(self)
		self.__listModel = swing.DefaultListModel()
		self.__list = swing.JList(self.__listModel)
		self.__list.cellRenderer = self.__Renderer()
		
		#test add
		#self.__listModel.addElement(self.__MiniMondrian())
		
		self.setViewportView(self.__list)
		#self.minimumSize = awt.Dimension(80, 480)
		
		
	def add_mini_view(self, graph):
		mini = self.__MiniMondrian(graph)
		self.__listModel.addElement(mini)
		
class Canvas(swing.JPanel):
	def __init__(self):
		swing.JPanel.__init__(self)
		global mondrian_instance
		self.preferredSize = awt.Dimension(480,480)
		self.background = WHITE
		self.__line_stroke = awt.BasicStroke(9)
		self.__rec_stroke = awt.BasicStroke()
		self.__load_popup_menu()
		self.__current_graph = None
		
	def set_graph(self, graph):
		self.__current_graph = graph
	
	def get_graph(self, graph):
		return self.__current_graph
		
	def paint(self,g):
		swing.JPanel.paint(self,g)
		
		if self.__current_graph == None:
			pass
			
		#draw rectangles
		g.setStroke(self.__rec_stroke)
		for r in self.__current_graph.rectangles:
			g.setColor(r[1])
			g.fill(r[0])
		#draw lines
		g.setStroke(self.__line_stroke)
		for l in self.__current_graph.lines:
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
			#g.setColor(awt.Color.RED)
			#g.draw(l)
			pass
	
	def __save_as(self):
		#f = io.File(filename)
		#out = ImageIO.createImageOutputStream(f)
		#im = image.BufferedImage()
		print 'invoked save as'
		jc = swing.JFileChooser()
		resp = jc.showSaveDialog(self)
		if resp == swing.JFileChooser.APPROVE_OPTION:
			self.__output_image(jc.getSelectedFile())
	
	def __output_image(self, f):
		print 'saving image:',f.getPath()
		out = io.FileOutputStream(f)
		size = self.preferredSize
		im = image.BufferedImage(size.width, size.height, image.BufferedImage.TYPE_INT_RGB)
		g2d = im.getGraphics()
		self.paint(g2d)
		ImageIO.write(im,'png',out)
		out.close()
		print 'saving image done'
		
	def __load_popup_menu(self):
		self.__popup = swing.JPopupMenu()
		self.__saveas_b = swing.JMenuItem('Save as png...')
		self.__popup.add(self.__saveas_b)
		
		controller.add_mouse_action(self, self.__popingup, 'Clicked')
		controller.add_action(self.__saveas_b, self.__save_as)
		
	def __popingup(self, e):
		if e.getButton() == MouseEvent.BUTTON3:
			self.__popup.show(e.getComponent(), e.getX(), e.getY())
					
class ControlPane(swing.JPanel):
	def __init__(self):
		swing.JPanel.__init__(self)
		self.layout = awt.FlowLayout(awt.FlowLayout.RIGHT)
		
		self.__next_b = swing.JButton('See next')
		self.add(swing.JLabel("You like? "))
		self.__group = swing.ButtonGroup()
		
		#radio buttons
		def rb(text, _self = self):
			b = swing.JRadioButton(text)
			b.setActionCommand(text)
			return b
			
		for b in (rb('Structure'), rb('Color'), rb('Both'), rb('None')):
			self.add(b)
			self.__group.add(b)
			
		self.add(self.__next_b)
		controller.add_action(self.__next_b, self.next_paint)
		
	
	def next_paint(self):
		global graph_history;
		chromosome = ChromoManager.get_next_chromosome()
		graph = mondrian_instance.compose(chromosome, gui_canvas.preferredSize)
		gui_canvas.set_graph(graph)
		gui_canvas.repaint()
		graph_history.append(graph)
		gui_miniView.add_mini_view(graph)
		
#This class must be instanized after all other gui elements
class ControlMenu(swing.JMenuBar):
	def __init__(self):
		swing.JMenuBar.__init__(self)
		
		#init menus
		m_file = swing.JMenu("File")
		m_evolution = swing.JMenu("Evolution")
		m_about = swing.JMenu("about")
		
		for m in (m_file, m_evolution, m_about):
			self.add(m)
		
class StatusBar(swing.JTextField):
	def __init__(self):
		swing.JTextField.__init__(self)
		self.editable = 0
		
	def show_message(self, txt):
		self.text = txt
	
	def clear_message():
		self.show_message("")
		
class GlobalController:
	
	class DummyAction(awt.event.ActionListener):
		def __init__(self, target_method, parameters):
			self.__target = target_method
			self.__parameters = parameters
			
		def actionPerformed(self, e):
			self.__target(*self.__parameters)
	
	class DummyMouseAction(MouseAdapter):
		'''action type: Clicked/Entered/Exited/Pressed/Released'''
		def __init__(self, target_method, action_type, parameters):
			MouseAdapter.__init__(self)
			self.__target = target_method
			self.__action_type = action_type
			self.__parameters = parameters
			#Dynamic delegation
			setattr(self, 'mouse'+action_type, self.__delegate_to)
			
		def __delegate_to(self, event):
			self.__target(event, *self.__parameters)
		
		#Jython bug:
		#static definition must present or dynamic delegation won't work
		def mouseClicked(self, f):
			raise 'should never be called'
			
	#Inner class definition done		
			
	def add_action(self, source, method, *para):
		a = GlobalController.DummyAction(method, para)
		source.addActionListener(a)
		
	def add_mouse_action(self, source, method, action_type, *para):
		m = GlobalController.DummyMouseAction(method, action_type, para)
		source.addMouseListener(m)
		
	def __init__(self):
		pass
	
			
#global singleton instance
mondrian_instance = Mondrian()
controller = GlobalController()

#global GUI instance
gui_canvas = Canvas()
gui_control = ControlPane()
gui_miniView = MiniView()
gui_statusBar = StatusBar()
gui_menu = ControlMenu()

#history paint
graph_history = []

#Assemble gui elements
def start_window():
	root = swing.JFrame(title = 'Darwindrian - prototype')
	content = swing.JPanel(layout = awt.BorderLayout())
	content.add(gui_canvas, awt.BorderLayout.CENTER)
	content.add(gui_control, awt.BorderLayout.SOUTH)
	
	#Issue split bar
	split = swing.JSplitPane(swing.JSplitPane.HORIZONTAL_SPLIT)
	split.setLeftComponent(gui_miniView)
	split.setRightComponent(content)
	
	#Issue whole arrangment
	top = swing.JPanel(layout = awt.BorderLayout())
	
	top.add(split, awt.BorderLayout.CENTER)
	top.add(gui_statusBar, awt.BorderLayout.SOUTH)
	top.add(gui_menu, awt.BorderLayout.NORTH)
	
	root.contentPane = top
	root.visible = 1
	root.resizable = 0
	root.defaultCloseOperation = swing.JFrame.EXIT_ON_CLOSE
	root.pack()
	
	#generate first Mondrian graph
	gui_control.next_paint()
	
def testing():
	if __name__ == '__main__':
		#try:
		start_window()
		#except NullPointerException, e1:
		#	print 'Warning: null pointer exception detected'
		#except Exception, e2:
		#	print 'Warning: Exception detected:',e2
#run
testing()

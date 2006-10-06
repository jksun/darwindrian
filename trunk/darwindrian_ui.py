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

from prototype_darwindrian import *

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
			return
			
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
	
#global GUI instance
controller = GlobalController()
gui_canvas = Canvas()
gui_control = ControlPane()
gui_miniView = MiniView()
gui_statusBar = StatusBar()
gui_menu = ControlMenu()

#GUI module of Darwindrian.
#API used: java Swing/awt
#Author: Jian Yin Shen

from javax import swing
from java import awt
from java import io
from java.awt import geom
from java.awt import image
from java.awt.event import *
from javax.imageio import ImageIO

from java.lang import System
from darwindrian_geom import *
from darwindrian_controller import *

graph_history = []

class MiniView(swing.JScrollPane, swing.event.ListSelectionListener):
	
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
			
			value.gray_scale = selected	
			return wrapper
	
	class __MiniMondrian(swing.JPanel):
		def __init__(self, graph):
			swing.JPanel.__init__(self)
			self.preferredSize = awt.Dimension(80,80)
			self.background = WHITE
			self.__graph = graph
			self.gray_scale = 0
			
		def paint(self,g):
			swing.JPanel.paint(self, g)
			
			canvas_x = float(gui_canvas.preferredSize.width)
			canvas_y = float(gui_canvas.preferredSize.height)
			mini_x = float(self.preferredSize.width)
			mini_y = float(self.preferredSize.height)
			g.scale(mini_x/canvas_x, mini_y/canvas_y)
			
			for r in self.__graph.rectangles:
				
				if self.gray_scale:
					g.setColor(r[1])
				else:
					g.setColor(awt.Color.LIGHT_GRAY)
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
		self.__list.addListSelectionListener(self)
		
		self.setViewportView(self.__list)
		
		
	def add_mini_view(self, graph):
		mini = self.__MiniMondrian(graph)
		self.__listModel.addElement(mini)
		
	def valueChanged(self, e):
		self.__display_selected()
		
	def __display_selected(self):
		index = self.__list.getSelectedIndex()
		graph = graph_history[index]
		gui_canvas.set_graph(graph)
		
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
		self.repaint()
	
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
			
	def save_as(self):
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
		self.__saveas_b = swing.JMenuItem('Save as PNG...')
		self.__popup.add(self.__saveas_b)
		
		controller.add_mouse_action(self, self.__popingup, 'Clicked')
		controller.add_action(self.__saveas_b, self.save_as)
		
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
		graph_history.append(graph)
		gui_canvas.set_graph(graph)
		gui_miniView.add_mini_view(graph)
		
#This class must be instanized after all other gui elements
class ControlMenu(swing.JMenuBar):
	def __init__(self):
		swing.JMenuBar.__init__(self)
		
		#init menus
		m_file = swing.JMenu("File")
		mi_save_as = swing.JMenuItem("Save as PNG...")
		controller.add_action(mi_save_as, gui_canvas.save_as)
		sp = swing.JSeparator()
		mi_exit = swing.JMenuItem("Exit")
		controller.add_action(mi_exit, System.exit, 0)
		for m in (mi_save_as, sp, mi_exit):
			m_file.add(m)
		
		m_evolution = swing.JMenu("Evolution")
		mi_reset = swing.JMenuItem("Reset evolution")
		mi_next = swing.JMenuItem("Next graph")
		controller.add_action(mi_next, gui_control.next_paint)
		sp = swing.JSeparator()
		mi_info = swing.JMenuItem("Show evolution info...")
		
		for m in (mi_reset, mi_next, sp, mi_info):
			m_evolution.add(m)
			
		m_about = swing.JMenu("Help")
		mi_about = swing.JMenuItem("About Darwindrian")
		for m in [mi_about]:
			m_about.add(m)
		
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
		
		
#global GUI instance
gui_canvas = Canvas()
gui_control = ControlPane()
gui_miniView = MiniView()
gui_statusBar = StatusBar()
gui_menu = ControlMenu()

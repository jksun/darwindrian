from darwindrian_ui import *

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
		start_window()
#run
testing()

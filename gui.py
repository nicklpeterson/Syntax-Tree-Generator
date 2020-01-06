import PySimpleGUI as sg
import calculator as calc
from collections import defaultdict
import draw_tree as dt
import math

SPACING = 50
NODE_SIZE = 20

class Graphics:

    def __init__(self):
        sg.change_look_and_feel('GreenMono')

        layout = [      
           [sg.Graph(canvas_size=(1000, 400), graph_bottom_left=(0,0), graph_top_right=(1000, 400), key='graph', enable_events = True)],      
           [sg.Text('Enter Expression:'), 
            sg.Input(size=(100, 1), justification='left', key='Expression'), 
            sg.Button('Make Tree'), 
            sg.Button('Clear'), 
            sg.Button('Exit')]]

        self.window = sg.Window('Syntax Tree', layout)
        self.window.finalize()
        self.graph = self.window['graph']
        self.parser = calc.InputParser()
        self.figures = {'nodes' : [], 'text' : [], 'lines':[]}
        self.draw_tree = None
        self._event_loop()
        self.window.close()

    def _event_loop(self):
        """
        The UI event loop
        """
        while True:
            event, values = self.window.read()
            if event in (None, 'Make Tree'):
                self._clear_graph()
                #try:
                self._make_syntax_tree(values)
                #except:
                #self._pop_up("I am unable to evaluate that expression.", "Error")
            if event in (None, 'graph') and self.draw_tree:
                self._update_syntax_tree(values)
            if event in (None, 'Exit'):
                return
            if event in (None, 'Clear'):
                self._clear_graph()
                self.draw_tree = None
        
    def _pop_up(self, output, title):
        sg.popup(str(output), title = str(title))

    def _update_syntax_tree(self, values):
        clicked_node = self._find_node(values['graph'], self.draw_tree)
        if clicked_node:
            result = self.evaluate_tree(clicked_node.node)
            clicked_node.node = calc.Node(result, None, None)
            clicked_node.children = []
            self._clear_graph()
            self._render_tree(self.draw_tree)
            self._bring_nodes_to_front()

    def _make_syntax_tree(self, values):
        tree = self.parser.parse_input(str(values['Expression']))
        result = self.evaluate_tree(tree)
        self.draw_tree = self._generate_tree(tree)
        self._bring_nodes_to_front()

    def evaluate_tree(self, root):
        return self.parser.evaluate(root)
    
    def _generate_tree(self, tree):
        draw_tree = dt.DrawTree(tree, NODE_SIZE, 375)
        # draw_tree = dt.initialize(draw_tree)
        self._render_tree(draw_tree)
        return draw_tree

    def _render_tree(self, tree):
        if not tree:
            return
        self._draw_node(tree)
        current_coor = (tree.x, tree.y)
        for child in tree.children:
            if child:
                self._draw_branch(current_coor, (child.x, child.y))
            self._render_tree(child)

    def _draw_node(self, tree):
        """
        Draw a node on the graph

        :param tree: the node to draw
        """
        circle = self.graph.DrawCircle((tree.x, tree.y), NODE_SIZE, fill_color = 'white')
        self.figures['nodes'].append(circle)
        node_value = "^" if tree.node.value == "**" else str(tree.node.value)
        text = self.graph.DrawText(node_value, (tree.x, tree.y))
        self.figures['text'].append(text)

    def _draw_branch(self, coor_a, coor_b):
        """
        Draw a straight line between the (x_1, y_1) and (x_2, y_2)
        """
        line = self.graph.DrawLine(coor_a, coor_b)
        self.figures['lines'].append(line)

    def _clear_graph(self):
        for key in self.figures:
            for item in self.figures[key]:
                self.graph.DeleteFigure(item)
            self.figures[key] = []
    
    def _bring_nodes_to_front(self):
        for n in self.figures['nodes']:
            self.graph.BringFigureToFront(n)
        for t in self.figures['text']:
            self.graph.BringFigureToFront(t)

    def _distance(self, coor_a, coor_b):
        return math.sqrt( ( coor_a[0] - coor_b[0] ) ** 2 + ( coor_a[1] - coor_b[1] ) ** 2)

    def _find_node(self, coor, tree):
        if tree.node and self._distance(coor, (tree.x, tree.y)) < (NODE_SIZE * 2):
            return tree
        check_left = self._find_node(coor, tree.children[0]) if (len(tree.children) > 0 and tree.children[0]) else None
        check_right = self._find_node(coor, tree.children[1]) if (len(tree.children) > 1 and tree.children[1]) else None
        node_exists = check_left if check_left else check_right
        return node_exists

if __name__ == "__main__":
    Graphics()
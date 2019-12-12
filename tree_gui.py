import PySimpleGUI as sg
import calculator as calc
from collections import defaultdict

SPACING = 50

class Graphics:

    def __init__(self):
        sg.change_look_and_feel('GreenMono')

        layout = [      
           [sg.Graph(canvas_size=(1000, 400), graph_bottom_left=(0,0), graph_top_right=(1000, 400), key='graph')],      
           [sg.Text('Enter Expression:'), sg.Input(size=(10, 1), justification='left', key='Expression'), sg.Button('Make Tree'), sg.Button('Clear'), sg.Button('Exit')]]

        self.window = sg.Window('Syntax Tree', layout)
        self.window.finalize()
        self.graph = self.window['graph']
        self.parser = calc.InputParser()
        self.figures = {'nodes' : [], 'text' : [], 'lines':[]}

        event, values = self.window.read()

        while True:
            event, values = self.window.read()
            if event in (None, 'Make Tree'):
                if str(values['Expression']).lower() == 'exit':
                    break
                self._clear_graph()
                try:
                    tree = self.make_syntax_tree(values)
                    result = self.evaluate_tree(tree)
                    self.draw_tree(tree)
                    self._bring_nodes_to_front()
                except:
                    result = "I am unable to evaluate that expression."
                self.pop_up(result)
            if event in (None, 'Exit'):
                break
            if event in (None, 'Clear'):
                self._clear_graph()
        
        self.window.close()
        
    def pop_up(self, output):
        sg.popup('Result: ', str(output))

    def make_syntax_tree(self, values):
        return self.parser.parse_input(str(values['Expression']))

    def evaluate_tree(self, root):
        return self.parser.evaluate(root)
    
    def draw_tree(self, tree):
        draw_tree = self._set_coordinates(tree)
        self._render_tree(draw_tree)

    def _render_tree(self, tree):
        if not tree.value: # or tree.visited:
            return
        self._draw_node(tree)
        current_coor = (tree.x, tree.y)
        tree.visited = True
        for child in tree.children:
            if child.value:
                self._draw_branch(current_coor, (child.x, child.y))
            self._render_tree(child)


    def _draw_node(self, node):
        circle = self.graph.DrawCircle((node.x, node.y), 20, fill_color = 'white')
        self.figures['nodes'].append(circle)
        text = self.graph.DrawText(str(node.value), (node.x, node.y))
        self.figures['text'].append(text)

    def _draw_branch(self, coor_a, coor_b):
        """
        Draw a straight line between the (x_1, y_1) and (x_2, y_2)
        """
        line = self.graph.DrawLine(coor_a, coor_b)
        self.figures['lines'].append(line)

    def _set_coordinates(self, tree):
        """
        Set the coordinates of each node in the tree
        """
        draw_tree = DrawTree(tree)
        self._setup_tree(draw_tree)
        self._add_mods(draw_tree)
        return draw_tree
    
    def _setup_tree(self, tree, depth=350, nexts=None, offset=None):
        global SPACING

        if nexts is None:
            nexts = defaultdict(lambda: 0)
        if offset is None:
            offset = defaultdict(lambda: 0)
        for child in tree.children:
            self._setup_tree(child, depth - SPACING, nexts, offset)
        tree.y = depth

        if not tree.children:
            place = nexts[depth]
            tree.x = place
        elif len(tree.children) == 1:
            place = tree.children[0].x - SPACING
        else:
            place = (tree.children[0].x + tree.children[1].x) / 2
        
        offset[depth] = max(offset[depth], nexts[depth]-place)

        if tree.children:
            tree.x = place + offset[depth]
        
        nexts[depth] += (2 * SPACING)
        tree.offset = offset[depth]

    def _add_mods(self, tree, modsum = 0):
        tree.x = tree.x + modsum
        modsum += tree.offset

        for child in tree.children:
            self._add_mods(child, modsum)
    
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

        
class DrawTree(object):
    def __init__(self, tree, depth = 0):
        self.x = -1
        self.y = depth
        self.offset = 0
        self.visited = False
        if tree is None:
            self.value = None
            self.children = []
        else:
            self.value = tree.value
            self.children = [DrawTree(child, depth + 10) for child in tree]


if __name__ == "__main__":
    Graphics()
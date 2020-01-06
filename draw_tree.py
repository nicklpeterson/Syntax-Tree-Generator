import math
from operator import lt, gt

class DrawTree(object):

    def __init__(self, root, node_width, initial_depth, parent = None):
        self.x = 100
        self.y = initial_depth
        self.parent = parent
        self.spacing = node_width + 30
        self.node = root
        self.mod = 0
        self.children = []
        if root.left:
            self.children.append(DrawTree(root.left, self.spacing, initial_depth - 50, parent = self))
        if root.right:
            self.children.append(DrawTree(root.right, self.spacing, initial_depth - 50, parent = self))
        if not self.parent:
            self._initialize()
    
    def _initialize(self):
        """
        Initializes a DrawTree
        """
        self._post_order_traversal(self)
        add_mods(self)

    def _post_order_traversal(self, root):
        """
        Assign an x value to each node

        :param root: The root of a draw tree
        """
        if not root:
            return
    
        for child in root.children:
            self._post_order_traversal(child)

        last_child = len(root.children) - 1
        sibling_position = 0
        if root.parent and root.parent.children and root.parent.children[0] != root:
            for i, child in enumerate(root.parent.children):
                sibling_position = i if child == root else 0
        
        # Assign an x value to each right node
        if sibling_position != 0:
            root.x = root.parent.children[sibling_position - 1].x + self.spacing

        if root.children:
            last_child = len(root.children) - 1
            middle = (root.children[0].x + root.children[last_child].x) / 2
            if not root.parent or sibling_position == 0:
                root.x = middle
            else:
                offset = middle - root.x
                if offset > 0:
                    root.mod += middle - root.x
                elif offset < 0:
                    dist = root.children[last_child].x - root.children[0].x
                    shift = root.x + dist / 2 - root.children[last_child].x
                    for child in root.children:
                        child.mod += shift

        if sibling_position != 0:
            root.mod += self._push_right(root.parent.children[0], root)

    def _push_right(self, left, right):
        """
        Shift the right subtree to the right far enough to avoid overlap.
        Return the amount of the shift

        :param left: The root of a DrawTree
        :param right: The root of a DrawTree
        """
        wl = self._contour(left, lt)
        wr = self._contour(right, gt)
        return max(x-y for x,y in zip(wl, wr)) + self.spacing

    def _shift_right_children(self, tree, shift):
        """
        shift a node and all of it's children right

        :param shift: The amount to shift to the right
        """
        if not tree:
            return
        tree.x += shift
        for child in tree.children:
            self._shift_right_children(child, shift)

    def _contour(self, tree, comp, level = 0, cont = None):
        """
        Return the contour of a DrawTree. 
        Left contour if comp is lt and right contour if comp is gt

        :param tree: DrawTree Node
        :param comp: A comparison function.
        :param level: The current depth of the tree. Only used by recursive calls.
        :param cont: The contour of the tree
        """
        if not cont:
            cont = [tree.x]
        elif len(cont) < level + 1:
            cont.append(tree.x)
        elif comp(cont[level], tree.x):
            cont[level] = tree.x

        for child in tree.children:
            self._contour(child, comp, level + 1, cont)
        return cont
    
def add_mods(tree, modsum = 0):
    """
    Adjust the tree to prevent overlap

    :param tree: The root of a DrawTree
    :param modsum: An accumulator used to track the sum of mods
    """
    if not tree:
        return
    modsum += tree.mod
    tree.x = tree.x + modsum
    for child in tree.children:
        add_mods(child, modsum)
class Node:
    def __init__(self):
        self.data = None
        self.left_child = None
        self.right_child = None

    def insert(self, index, code, byte):
        if index == len(code):
            self.data = byte
        else:
            if code[index] == '0':
                if not self.left_child:
                    self.left_child = Node()
                self.left_child.insert(index + 1, code, byte)
            else:
                if not self.right_child:
                    self.right_child = Node()
                self.right_child.insert(index + 1, code, byte)

    def find_code(self, byte):
        node = self
        i = 0
        while True:
            if not node.left_child and not node.right_child or i == len(byte):
                return node, byte[i:]

            node = node.left_child if byte[i] == '0' else node.right_child
            i += 1

    '''def truncate(self):
        def recursive_delete(node):
            if not node:
                return

            node.left_child = recursive_delete(node.left_child)
            node.right_child = recursive_delete(node.right_child)

            if not node.left_child and node.right_child:
                node = node.right_child
            if node.left_child and not node.right_child:
                node = node.left_child

            return node

        self.left_child = recursive_delete(self.left_child)
        self.right_child = recursive_delete(self.right_child)'''

    '''def print_tree(self, value):
        if self.left_child:
            self.left_child.print_tree('0')
        if value == 'root':
            print(value)
        elif not self.right_child and not self.left_child:
            print(f'leaf = {value}, {self.data}')
        else:
            print(f'node = {value}')
        if self.right_child:
            self.right_child.print_tree('1')'''

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree import NodeMixin

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from anytree import NodeMixin, RenderTree


class MyBaseClass(object):  # Just an example of a base class
    foo = 4


class MyClass(MyBaseClass, NodeMixin):  # Add Node feature
    def __init__(self, name, length, width, parent=None, children=None):
        super(MyClass, self).__init__()
        self.name = name
        self.length = length
        self.width = width
        self.parent = parent
        if children:  # set children only if given
            self.children = children


def start():
    """
        udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    jan = Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)
    for pre, fill, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))
    # DotExporter(udo).to_picture("udo.png") DotExporter(dan, nodeattrfunc = lambda node: "fixedsize=true, width=1,
    # height=1, shape=diamond", edgeattrfunc = lambda parent, child: "style=bold").to_picture("dan.png")
    :return:
    """

    my0 = MyClass('GodLord', 0, 0)
    my1 = MyClass('Immortality', 1, 0, parent=my0)
    my3 = MyClass('organ replacement', 0, 0, parent=my1)
    my2 = MyClass('Omniscience', 0, 2, parent=my0)

    for pre, fill, node in RenderTree(my0):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.length, node.width)
    return 0


# Use a breakpoint in the code line below to debug your script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()
    variables = [0 for _ in range(10)]
    print(type(variables))
    print(variables)
    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
    }
    print(thisdict)
    child1 = {
        "name": "Emil",
        "year": 2004
    }
    child2 = {
        "name": "Tobias",
        "year": 2007
    }
    child3 = {
        "name": "Linus",
        "year": 2011
    }

    myfamily = {
        "child1": child1,
        "child2": child2,
        "child3": child3
    }


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


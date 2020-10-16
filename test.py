import datetime
import os, fnmatch
from anytree import NodeMixin, RenderTree
from anytree.exporter import DotExporter
import dataset

index_indent = []
prev_parentIndex = 0
nodes = []
apiKey = ""
current_day = datetime.datetime.today().isoweekday()

# TODO Add ablity to change "Utility?" based on what you completed
# TODO Alarm and/or time optimaztion function
# TODO Create frontend and use backend of RemNote
# TODO Keep track of when I worked on them


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def cleanText(txt):
    # Removes the ugly characters after copying and pasting from Remnote
    txtList = []
    for line in txt:
        # print(line)
        stripped_line = line.strip()
        txtList.append(stripped_line[2:])
    return txtList


def cleanData(dirtyList):
    # This separtes the data entered into strings and numbers
    # Stores data in nested list
    tmp = []
    for list in dirtyList:
        numbers = [[int(i) for i in list.split() if i.isdigit()]]
        strings = ''.join([i for i in list if not i.isdigit()]).strip()

        tmp.append([strings, numbers])
        # print(numbers)
    return tmp


def setup():
    file_name = find('*.txt', '/home/tom/PycharmProjects/UtilityMax')[0]

    with open(file_name, 'r+') as file:
        data = cleanData(cleanText(file))
    # print(data)

    with open(file_name) as fp:
        lines = fp.readlines()

    index = 0
    for line in lines:
        if index != len(data):
            spaceNum = len(line) - len(line.lstrip())
            # print(data)
            data[index][1].append(spaceNum)
            index += 1
    # print("Data:", data)
    return data


def switch(argument):
    switcher = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }
    return switcher.get(argument, "Invalid month")


class Node(NodeMixin):  # Add Node feature
    def __init__(self, name, utility, usefulnes, cashGain=0, dateWorked=-1, parent=None, children=None, completed=True):
        super(Node, self).__init__()
        self.name = name
        self.utility = utility
        self.parent = parent
        self.usefulnes = usefulnes
        self.cashGain = cashGain
        self.dateWorked = dateWorked

        if children:  # set children only if given
            self.children = children
        self.completed = completed

    def getDate(self):
        return switch(self.dateWorked)


def highestNum():
    """
    This is the highest indentation value
    :return:
    """
    highNum = 0
    numList = []

    for list in index_indent:
        # print(list)
        if list[1] >= 0:
            numList.append(list[1])
    for num in numList:
        if highNum < num:
            highNum = num
    return highNum


def find_index(highNum):
    tmp = []
    for item in index_indent:
        # print(item)
        tmp.append(item[1])

    return tmp.index(highNum)


def closest(lst, K):
    # print(lst)
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def next(highNum, child_index):
    global prev_parentIndex  # previous parent indenx

    tab = highNum - 4
    indexList = []
    # print("Index_indent:", index_indent)
    for lst in index_indent:
        # print("lst:",lst)
        if lst[1] == tab:  # lst[1] is the tabsValues
            indexList.append(lst[0])
            # print("IndexList:",indexList)
    # print(indexList)
    # if number stays same then has same parent as previous
    # else run closest

    # print("PrevIndex:", prev_parentIndex)
    # print("ChildIndex:", child_index)

    # check the what the parent of childIndex -1 is and if it is equal to previous Parent Index then return
    # prev_parentIndex

    if nodes[child_index - 1].parent is not None:
        return prev_parentIndex
    else:
        prev_parentIndex = closest(indexList, child_index)
        return prev_parentIndex

    # return closest(indexList, child_index)


def setParent(data):
    global nodes
    for i in range(len(nodes)):
        indentNum = data[i][1][1]
        # print(data)
        index_indent.append([i, indentNum])

    # print(indentList)
    # print(index_indent)

    for x in range(len(index_indent) - 1):
        highNum = highestNum()
        child_index = find_index(highNum)

        # nextHighest_num = next(highNum,child_index)  # edge-case NO 0's
        # parent_index = find_index(nextHighest_num)
        parent_index = next(highNum, child_index)

        nodes[child_index].parent = nodes[parent_index]

        # parent = nodes[parent_index].name
        # child = nodes[child_index].name
        # print("Parent:", parent, "\nChild:", child, "\n")

        # print("Parent:",parent_index, "\nChild:",child_index)
        index_indent[child_index][1] = -1

        # print(index_indent[child_index])
    # print(index_indent)


def printTree():
    for pre, fill, node in RenderTree(nodes[0]):
        treestr = u"%s%s" % (pre, node.name)
        print(treestr.ljust(8), node.completed)

    DotExporter(nodes[0]).to_picture("nodes.png")


def choose():
    """
    Picks the task with the highest utility
    :return:
    """
    highestUtility = 0
    name = None

    for choice in nodes:
        if highestUtility < choice.utility:
            highestUtility = choice.utility
            name = choice.name

    print("Miguel you must work on:", name)


def calcUtility(dataPoint):
    # TODO Create a function called cacluate execped utlity based on parameters
    # TODO How to decide on utility value of bottom level childs. Should the parent have the sum of the child?

    return 0


def setStorage(nodes):
    db = dataset.connect('sqlite:///GodLord.db')

    table = db['GodLord']
    for node in nodes:
        table.insert(dict(name=node.name,
                          cashGain=node.cashGain,
                          usefulness=node.usefulnes,
                          utility=node.utility
                          ))


def trueFalse(args):
    if args == 0:
        return True
    else:
        return False
    pass

def sortBy(godLord_data):
    usefulSort = []
    for dataPoint in godLord_data:
        if trueFalse(dataPoint[1][0][2]):
            usefulSort.append([dataPoint[0], dataPoint[1][0][0]])

    sorted_list = sorted(usefulSort, key=lambda x: x[1])
    # TODO Actually have a top 3
    # display top 3
    # sorted_list.reverse()
    for lst in sorted_list:
        print(lst[0])


if __name__ == "__main__":

    godLord_data = setup()

    for dataPoint in godLord_data:
        nodes.append(Node(name=dataPoint[0],
                          utility=calcUtility(dataPoint),

                          usefulnes=dataPoint[1][0][0],
                          cashGain=dataPoint[1][0][1],
                          completed=trueFalse(dataPoint[1][0][2])  # should be 0 or 1
                          ))
        # print(dataPoint)
    sortBy(godLord_data)
    # print(godLord_data[0])
    # print(sorted(godLord_data, key=lambda x: x[1][0]))

    setParent(godLord_data)
    # setStorage(nodes)

    # printTree()

    # choose()

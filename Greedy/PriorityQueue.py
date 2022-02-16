class PriorityQueue:
    def __init__(self):
        self.__values = {}

    def __str__(self):
        out = ''
        for el in self.__values:
            out += str(el)
            out += ':'
            out += str(self.__values[el])
            out += '\n'
        return out[:-1]

    def isEmpty(self):
        return len(self.__values) == 0

    def pop(self):
        topPriority = None
        topObject = None
        for obj in self.__values:
            objPriority = self.__values[obj]
            if topPriority is None or topPriority > objPriority:
                topPriority = objPriority
                topObject = obj
        del self.__values[topObject]
        return topObject, topPriority

    def add(self, obj, priority):
        self.__values[obj] = priority

    def contains(self, val):
        return val in self.__values

    def getObjPriority(self, obj):
        return self.__values[obj]

    def update(self, key, value):
        if key not in self.__values:
            raise Exception("Not in dict.")
        self.__values[key] = value
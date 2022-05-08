import os

class Formater:
    """
    Format a file of a certain extension into another extension
    """

    funcDict = {}

    def __init__(self, file):
        """
        file: the path to a file that contains the conversion informations
        """
        with open(file) as f:
            for line in f.readlines():
                source = None
                target = None
                header_line = 0
                ignore_prefix = ''

                for element in line.split("|"):
                    type, args = element.split(":")
                    
                    if type == "format":
                        source,target = args.split(",")

                    elif type == "header":
                        header_line = int(args)

                    elif type == "ignore":
                        ignore_prefix = args

                self.funDict[source] = createFormatFunction(source, target, header_line, ignore_prefix)




    def format(self, path):
        """
        format a file according to the conversion method of the formater (see the file used to initialize the formater)
        """

        if not os.path.isfile(path):
            print("Not a file")
            return -1

        name,extension = path.split(".")

        if extension != self.source:
            print("Source format doesn't correspond")
            return -2

        with open(path) as f:
            data = f.read()
            return self.funcDict[extension](data)

##############################################################################################

def findNthOccurences(l, n, element):
    """
    Find the index of the n-th occurrence of element in l
    """


    size = len(element)
    count = 0

    for i in range(0, len(l), size):
        if l[i:i+size] == element:
            count +=1
            
        if count == n:
            return i
    
    return -1

def createFormatFunction(source, target, header_line=0, ignore_prefix='', replace=[]):
    """
    Create a function to format a file to a certain target format
    """
    def result(path):
        """
        Format function that will be returned by createFormatFunction
        """
        name, extension = path.split(".")

        if extension != source:
            return -1
        elif extension == target:
            #nothing to do
            return 0

        with open(path) as f:
            data = f.read()

        data = data[findNthOccurences(data, header_line, "\n")::] #Ignore the lines before the headers

        for replacement in replace:
            old,new = replacement.split("->")

            data = data.replace(old, new)

        with open(name+"."+target, "w") as f:
            f.write(data)

        return 0
    
    return result 
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

                self.funDict[source] = createFormatFunction(target, header_line, ignore_prefix)




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

def createFormatFunction(target, source='', header_line=0, ignore_prefix='', replace=[]):
    """
    Create a function to format a file to a certain target format
    """
    pass
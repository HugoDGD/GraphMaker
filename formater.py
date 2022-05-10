import os
from pydoc import doc
import re

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

                sep = ','

                header_line = 0
                x_column = 0
                
                ignore_prefix = ''
                replace = []

                for element in line.split("|"):
                    if element == '\n' or element == '': continue

                    type, args = element.split(":")
                    
                    if type == "format":
                        source,target = args.split(",")

                    elif type == "sep":
                        sep = args

                    elif type == "header":
                        header_line = int(args)

                    elif type == "x_column":
                        x_column = int(args)

                    elif type == "ignore":
                        ignore_prefix = args
                    
                    elif type == "replace":
                        replace = args.split(" + ")

                self.funcDict[source] = createFormatFunction(source, target, sep, header_line, x_column, ignore_prefix, replace)




    def format(self, path):
        """
        format a file according to the conversion method of the formater (see the file used to initialize the formater)
        """

        if not os.path.isfile(path):
            print("Not a file")
            return -1

        name,extension = path.split(".")

        if extension in ("data","cart_bd_data", "pol_bd_data"): #already formatted (WIP do a attribute that contains all the target of format function)
            return path

        return self.funcDict[extension](path)

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
            
        if count >= n:
            return i
    
    return -1

# def replaceWithWildCard(data, old, new):
#     oldLen = len(old)

#     iOld = old.find("(.*)")

#     match = re.search(old,data)

#     result = ""
#     lastIndex=0
#     while match != None:
#         index = match.start()

#         newNew = new.replace("(.*)",data[index+iOld:index+oldLen-iOld+4])
#         newNewLen = len(newNew)

#         result += data[lastIndex:index]+newNew
#         lastIndex = index+newNewLen
#         match = re.search(old,data)

#     return result

def createFormatFunction(source, target, sep, header_line=0, x_column=0, ignore_prefix='', replace=[]):
    """
    Create a function to format a file to a certain target format
    """
    def result(path):
        """
        Format function that will be returned by createFormatFunction
        return the path to the created file (-1 if it failed)
        """
        name, extension = path.split(".")

        if extension != source:
            return -1
        elif extension == target:
            #nothing to do
            return path

        with open(path) as f:
            data = f.read()
        

        if header_line != 0:
            data = data[findNthOccurences(data, header_line-1, "\n")+1::] #Ignore the lines before the headers

        if x_column != 0:
            newData = ""
            for line in data.split():
                newData += line[findNthOccurences(line, x_column, sep)+1::]+"\n"

            data = newData

        data = data.replace(sep, ",")

        for replacement in replace:
            old,new = replacement.split("->")
            data = re.sub(str(old), str(new), data)

        with open(name+"."+target, "w") as f:
            f.write(data)

        return name+"."+target
    
    return result 

if __name__ == "__main__":
    f = Formater("format_conversion.txt")

    f.format("Data/integrateur3.cart_bd_lt")

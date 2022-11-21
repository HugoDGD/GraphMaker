import os
import pandas as pd
import numpy as np

def decodeData(path):
    return pd.read_csv(path, delimiter=",", header=0) 

def decodePolBodeData(path):
    data = pd.read_csv(path, delimiter=",", header=0)

    count=0
    for i,col in enumerate(data.columns):
        if col.startswith("Phase"):
            if count == 0:
                data.rename(columns = {col:"Phase"}, inplace = True)
            else:
                data.rename(columns = {col:"Phase."+str(count)}, inplace = True)

            count+=1 
    return data
    
def decodeCartBodeData(path):
    data = pd.read_csv(path, delimiter=",", header=0) 

    i=0
    count=0
    while i<len(data.columns):
        col = data.columns[i]
        print(col)
        if col.startswith("Real"):

            # data.columns[i] = "Magnitude"
            if count == 0:
                data.rename(columns = {data.columns[i]:"Magnitude"}, inplace = True)
            else:
                data.rename(columns = {data.columns[i]:"Magnitude."+str(count)}, inplace = True)

            # data.columns[i+1] = "Phase"
            if count == 0:
                data.rename(columns = {data.columns[i+1]:"Phase"}, inplace = True)
            else:
                data.rename(columns = {data.columns[i+1]:"Phase."+str(count)}, inplace = True)

            imgColumn = data.iloc[:,i]+1j*data.iloc[:,i+1]

            data.iloc[:,i] = 20*np.log10(np.abs(imgColumn)) #Magnitude
            data.iloc[:,i+1] = np.rad2deg(np.angle(imgColumn)) #Phase

            i+=2
            count+=1
        else:
            i+=1

    return data

class FileDecoder:
    """
    Decode a formated file and create a panda dataframe
    """

    func = {}

    def __init__(self, func={"data": decodeData, "cart_bd_data": decodeCartBodeData, "pol_bd_data": decodePolBodeData}):
        self.func = func

    def decode(self, path):
        if not os.path.isfile(path):
            print("Path is not a file")
            return -1

        name, extension = path.split(".")

        with open(path) as f:
            return self.func[extension](path)



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    decoder = FileDecoder()

    df = decoder.decode("Data/integrateur3.cart_bd_data")
    df.plot(x=0)

    plt.show()
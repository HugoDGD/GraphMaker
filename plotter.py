import matplotlib.pyplot as plt
import decoder as d
import formater as f

def bodePlot(df):
    fig, ax = plt.subplots(figsize=(10,5))
    
    ax2 = ax.twinx()
    
    magnitudes = df.columns[1::2]
    phases = df.columns[2::2]

    df.plot(x=0, y=magnitudes, ax=ax, loglog=True)
    df.plot(x=0, y=phases, ax=ax2, linestyle="dotted", logx=True)


    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    
    ax2.set_ylim(bottom=0)

def plot(df):
    df.plot(x=0)

class Plotter:

    func = {}
    decoder = None
    formater = None

    def __init__(self, func={"data": plot, "bode":bodePlot}, decoderFunc=None, formaterFile="format_conversion.txt"):
        self.func = func

        if decoderFunc == None:
            self.decoder = d.FileDecoder()
        else:
            self.decoder = d.FileDecoder(decoderFunc)

        self.formater = f.Formater(formaterFile)

    def plot(self,path):
        filename = self.formater.format(path)

        if filename == -1:
            return -1

        name, extension = filename.split(".")

        df = self.decoder.decode(filename)

        type = None
        if extension == "data":
            type = "data"
        elif extension in ("cart_bd_data","pol_bd_data"):
            type = "bode"
        else:
            return -2

        self.func[type](df)

        return 0

if __name__ == "__main__":
    import sys

    pelotter = Plotter()

    for file in sys.argv[1:]:
        print(pelotter.plot(file))

    plt.legend()
    plt.show()
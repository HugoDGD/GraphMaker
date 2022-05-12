import matplotlib.pyplot as plt
import decoder as d
import formater as f

def bodePlot(df, visuals=None):

    df.rename(columns={old:new for old,new in zip(df.columns[1:], visuals["labels"])}, inplace=True)
    print(df.columns)

    fig, ax = plt.subplots(figsize=(10,5))
    
    ax.set_title(visuals["title"])
    
    ax2 = ax.twinx()
    ax2.set_ylabel(r"$\angle V_{out}$")


    
    magnitudes = df.columns[1::2]
    phases = df.columns[2::2]

    df.plot(x=0, y=magnitudes, ax=ax, loglog=True)
    df.plot(x=0, y=phases, ax=ax2, linestyle="dotted", logx=True)

    if visuals["x_axis"] != None:
        ax.set_xlabel(visuals["x_axis"])
    if visuals["x_lim"] != None:
        ax.set_xlim(visuals["x_lim"])

    if visuals["y_axis"] != None:
        ax.set_ylabel(visuals["y_axis"])
    if visuals["y_lim"] != None:
        ax.set_ylim(visuals["y_lim"])

    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")
    
    # ax2.set_ylim(bottom=0)

def plot(df):
    df.rename(column={old:new for old,new in zip(df.columns, visuals["labels"])}, inplace=True)

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

    def plot(self,path, visuals=None):
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

        self.func[type](df,visuals)

        plt.show()

        return 0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('f', type=str,
                        help='The file to plot')
    parser.add_argument('-t', '--title', type=str, default=None,
                        help='Title of the figure')

    parser.add_argument('-x', '--x_axis', type=str, default=None,
                        help='Set the name of the x axis')
    parser.add_argument('--x_lim', nargs='+', type=float, default=None,
                        help='Limit of the x axis')

    parser.add_argument('-y','--y_axis', type=str, default=None,
                        help='Set the name of the y axis')
    parser.add_argument('--y_lim', nargs='+', type=float, default=None,
                        help='Limit of the x axis')

    parser.add_argument('-l', '--labels', nargs='+', type=str, default=None,
                        help='Labels of the signals')
    

    args = parser.parse_args()
    
    visuals = {"title":args.title, "x_axis":args.x_axis, "x_lim":args.x_lim, "y_axis":args.y_axis, "y_lim":args.y_lim, "labels":args.labels}

    pelotter = Plotter()
    pelotter.plot(args.f, visuals)
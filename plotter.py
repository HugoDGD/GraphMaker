import matplotlib.pyplot as plt
import decoder as d
import formater as f

def bodePlot(df, visuals=None):

    if visuals["labels"] != None:
        df.rename(columns={old:new for old,new in zip(df.columns[1:], visuals["labels"])}, inplace=True)

    fig, ax = plt.subplots(figsize=(10,5))
    
    ax.set_title(visuals["title"], fontsize=20)
    
    ax2 = ax.twinx()
    ax2.set_ylabel(r"$\angle V_{out}$", fontsize=24)
    
    magnitudes = df.columns[1::2]
    phases = df.columns[2::2]

    if len(magnitudes != 0):
        df.plot(x=0, y=magnitudes, ax=ax, loglog=True, fontsize=16)
    if len(phases != 0):
        df.plot(x=0, y=phases, ax=ax2, linestyle="dotted", logx=True, fontsize=16)

    if visuals["x_axis"] != None:
        ax.set_xlabel(visuals["x_axis"], fontsize=24)
    if visuals["x_lim"] != None:
        ax.set_xlim(visuals["x_lim"])

    if visuals["y_axis"] != None:
        ax.set_ylabel(visuals["y_axis"], fontsize=24)
    if visuals["y_lim"] != None:
        ax.set_ylim(visuals["y_lim"])

    if len(magnitudes != 0):
        ax.legend(loc="upper left", fontsize=24)
    if len(phases != 0):
        ax2.legend(loc="upper right", fontsize=24)
    
    # ax2.set_ylim(bottom=0)

    # ax.set_xticks(fontsize=12)
    # ax.set_yticks(fontsize=12)
    # ax2.set_yticks(fontsize=12)

def plot(df, visuals=None):
    if visuals["labels"] != None:
        df.rename(columns={old:new for old,new in zip(df.columns[1:], visuals["labels"])}, inplace=True)

    ax = df.plot(x=0,fontsize=16)

    ax.set_title(visuals["title"], fontsize=20)

    if visuals["x_axis"] != None:
        ax.set_xlabel(visuals["x_axis"], fontsize=24)
    if visuals["x_lim"] != None:
        ax.set_xlim(visuals["x_lim"])

    if visuals["y_axis"] != None:
        ax.set_ylabel(visuals["y_axis"], fontsize=24)
    if visuals["y_lim"] != None:
        ax.set_ylim(visuals["y_lim"])

    ax.legend(loc="upper right", fontsize=24)

    # ax.set_xticks(fontsize=12)
    # ax.set_yticks(fontsize=12)


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

        if visuals["remove"] != None:
            df.drop(df.columns[visuals["remove"]], inplace=True, axis=1)

        type = None
        if extension == "data":
            type = "data"
        elif extension in ("cart_bd_data","pol_bd_data"):
            type = "bode"
        else:
            return -2

        self.func[type](df,visuals)

        # Show the major grid lines with dark grey lines
        plt.grid(visible=True, which='major', color='#666666', linestyle='-')

        # Show the minor grid lines with very faint and almost transparent grey lines
        plt.minorticks_on()
        plt.grid(visible=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        plt.show()

        return 0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Plot a graph.')
    parser.add_argument('f', metavar="FILENAME", type=str,
                        help='The file to plot')
    parser.add_argument('-t', '--title', type=str, default=None,
                        help='Title of the figure')

    parser.add_argument('-x', '--x_axis', type=str, default=None,
                        help='Set the name of the x axis')
    parser.add_argument('--x_lim', nargs='+', type=float, default=None,
                        help='Limits of the x axis (list of 2 floats)')

    parser.add_argument('-y','--y_axis', type=str, default=None,
                        help='Set the name of the y axis')
    parser.add_argument('--y_lim', nargs='+', type=float, default=None,
                        help='Limits of the y axis (list of 2 floats)')

    parser.add_argument('-l', '--labels', nargs='+', type=str, default=None,
                        help='Labels of the signals in the same order than the input file headers (without the x axis)')

    parser.add_argument('-r', '--remove', nargs='+', type=int, default=None,
                        help='Indexes of signal that will be removed (0 is the index of the x-axis). The signals will be renamed after the removing so name them accordingly')
    

    args = parser.parse_args()
    
    visuals = {"title":args.title, "x_axis":args.x_axis, "x_lim":args.x_lim, "y_axis":args.y_axis, "y_lim":args.y_lim, "labels":args.labels, "remove":args.remove}

    pelotter = Plotter()
    pelotter.plot(args.f, visuals)
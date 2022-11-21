# GraphMaker

## Table of Contents
* [Dependencies](#dependencies)
* [Features](#features)
* [Supported Formats](#supported-formats)
* [Usage](#usage)

## Dependencies
* pandas
* matplotlib
* numpy

## Features
* a formater to convert data formats into a standard one
* a decoder to decode the standard data format and get a pandas dataframe
* a plotter to plot the dataframe into a matplotlib graph (serve as main)

## Supported Formats
* **.csv**: A csv with headers on the first line and the data in columns below them

* **.pisko**: A voltage graph from [Picoscope](https://www.picotech.com/downloads)

* **.scp**: a voltage graph from [Scopy](https://wiki.analog.com/university/tools/m2k/scopy)
* **pol_bd_scp**: a polar Bode diagram from Scopy

* **.lt**: a voltage graph from [LTspiceXVII](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html)
* **.cart_bd_lt**: a cartesian Bode diagram from LTspice

More formats can be added via "format_conversion.txt"

## Usage
You first have to rename your file with the format according to were they come from (it will tell the program how to convert them)

Then you just have to execute **plotter.py** with the filename as input.

### Visuals args 
```bash
plotter.py [-h] [-t TITLE] [-x X_AXIS] [--x_lim X_LIM [X_LIM ...]] [-y Y_AXIS] [--y_lim Y_LIM [Y_LIM ...]] [-l LABELS [LABELS ...]] [-r REMOVE [REMOVE ...]]
                  FILENAME

Plot a graph.

positional arguments:
  FILENAME              The file to plot

optional arguments:
  -h, --help            show this help message and exit

  -t TITLE, --title TITLE

                        Title of the figure

  -x X_AXIS, --x_axis X_AXIS
                        Set the name of the x axis

  --x_lim X_LIM [X_LIM ...]
                        Limits of the x axis (list of 2 floats)

  -y Y_AXIS, --y_axis Y_AXIS
                        Set the name of the y axis

  --y_lim Y_LIM [Y_LIM ...]
                        Limits of the y axis (list of 2 floats)

  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        Labels of the signals in the same order than the input file headers (without the x axis)

  -r REMOVE [REMOVE ...], --remove REMOVE [REMOVE ...]
                        Indexes of signal that will be removed (0 is the index of the x-axis). The signals will be renamed after the removing so name them
                        accordingly
```

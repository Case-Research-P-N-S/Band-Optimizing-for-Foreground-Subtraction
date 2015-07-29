# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

#def plot1(xaxis, *args):
#    ax = plt.subplot(1, 1, 1)    
#    for i, val in enumerate(args):
#        name = 'curve{}'.format(i+1)
#        name, = ax.plot(xaxis, val, label = name)
#    plt.title("Measured and Best Fit Function")
#    handles, labels = ax.get_legend_handles_labels()
#    plt.legend(handles, labels, loc='upper right')
#    return ax
#    
#xaxis = range(100)
#y1 = [2*y for y in xaxis]
#y2 = [y**1.01 for y in xaxis]
#
#plotty = plot1(xaxis, y1, y2)


def my_plotter(xaxis, *args, **kwargs):
    """ A helper function to make a graph
    Parameters
    ----------
    ax : Axes
        The axes to draw to
    xaxis : array
       The x data
    *args : array
       The y data
    param_dict : dict
       Dictionary of kwargs to pass to ax.plot
    """
    fig, ax = plt.subplots(1, 1)
    for i, val in enumerate(args):
        name = 'curve{}'.format(i+1)
        name, = ax.plot(xaxis, val, label=name)
    plt.title("Measured and Best Fit Function")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper right')
    return fig

xaxis = range(100)
data2 = [y*2 for y in xaxis]
data4 = [y**1.1 for y in xaxis]

test = my_plotter(xaxis, data2, data4)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(test)
ax2.plot(test)


import matplotlib.pyplot as plt
import numpy as np

# #def plot1(xaxis, *args):
# #    ax = plt.subplot(1, 1, 1)    
# #    for i, val in enumerate(args):
# #        name = 'curve{}'.format(i+1)
# #        name, = ax.plot(xaxis, val, label = name)
# #    plt.title("Measured and Best Fit Function")
# #    handles, labels = ax.get_legend_handles_labels()
# #    plt.legend(handles, labels, loc='upper right')
# #    return ax
# #    
# #xaxis = range(100)
# #y1 = [2*y for y in xaxis]
# #y2 = [y**1.01 for y in xaxis]
# #
# #plotty = plot1(xaxis, y1, y2)

# def my_plotter(ax, xaxis, *args, **kwargs):
#     """ A helper function to make a graph
#     Parameters
#     ----------
#     ax : Axes
#         The axes to draw to
#     xaxis : array
#        The x data
#     *args : array
#        The y data
#     param_dict : dict
#        Dictionary of kwargs to pass to ax.plot
#     """
#     for i, val in enumerate(args):
#         name = 'curve{}'.format(i+1)
#         name, = ax.plot(xaxis, val)
#     ax.title("Measured and Best Fit Function")
#     handles, labels = ax.get_legend_handles_labels()
#     ax.legend(handles, labels, loc='upper right')
#     return ax

# xaxis = range(100)
# data2 = [y*2 for y in xaxis]
# data4 = [y**1.1 for y in xaxis]

# fig, ax1 = plt.subplots(1, 1)
# test = my_plotter(ax1, xaxis, data2, data4)

# plt.savefig("lineplots.png")

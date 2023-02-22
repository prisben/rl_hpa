import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize=16)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(col_labels, fontsize=12)
    ax.set_yticklabels(row_labels, fontsize=12)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    #ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("white", "black"),
                     threshold=-400, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw, fontsize=7)
            texts.append(text)

    return texts


states = ["lat<250ms, pods =1","lat<250ms, 2<=pods<=4","lat<250ms,pods>5",
          "250ms<=lat<500ms, pods =1","250ms<=lat<500ms, 2<=pods<=4","250ms<=lat<500ms,pods>5",
          "500ms<=lat<750ms, pods =1","500ms<=lat<750ms, 2<=pods<=4","500ms<=lat<750ms,pods>5",
          "750ms<=lat<=1000ms, pods =1","750ms<=lat<=1000ms, 2<=pods<=4","750ms<=lat<=1000ms,pods>5",
          "lat>1000ms, pods =1","lat>1000ms, 2<=pods<=4","lat>1000ms,pods>5"]
actions = ["10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"]

path="TRA/training_TRA/"

qtable0 = np.zeros([15, 10])
qtable00 = np.load(path+"0/QTable.npy")
qtable1 = np.load(path+"1/QTable.npy")
qtable2 = np.load(path+"2/QTable.npy")
qtablem = np.load(path+"599/QTable.npy")
qtablen = np.load(path+"1199/QTable.npy")

fig, ax = plt.subplots()

im, cbar = heatmap(qtable0, states, actions, ax=ax,
                   cmap="hot", cbarlabel="Q-Value")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.tight_layout()
plt.title("Q-Table, 0 iterations", fontsize=15)
plt.show()

fig, ax = plt.subplots()

im, cbar = heatmap(qtable1, states, actions, ax=ax,
                   cmap="hot", cbarlabel="Q-Value")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.tight_layout()
plt.title("Q-Table, 2 iterations")
plt.show()

fig, ax = plt.subplots()

im, cbar = heatmap(qtable2, states, actions, ax=ax,
                   cmap="hot", cbarlabel="Q-Value")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.tight_layout()
plt.title("Q-Table, 3 iterations")
plt.show()

fig, ax = plt.subplots()

im, cbar = heatmap(qtablem, states, actions, ax=ax,
                   cmap="hot", cbarlabel="Q-Value")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.tight_layout()
plt.title("Q-Table, 600 iterations")
plt.show()

fig, ax = plt.subplots()

im, cbar = heatmap(qtablen, states, actions, ax=ax,
                   cmap="hot", cbarlabel="Q-Value")
texts = annotate_heatmap(im, valfmt="{x:.1f}")
fig.tight_layout()
plt.title("Q-Table, 1200 iterations", fontsize=15)
plt.show()



set_steps = list(range(0, 1200))
reward_list = []


THRS_LIST = {
     0: 10,
     1: 20,
     2: 30,
     3: 40,
     4: 50,
     5: 60,
     6: 70,
     7: 80,
     8: 90,
     9: 100,
 }


pods = []
thrs = []
rows_training = []

for i in list(range(0, 1200)):
    dict = {}
    filename = path+str(i) + "/k8s_historical_states_discrete.csv"
    df = pd.read_csv(filename, header=None)
    pods.append(int(str(df[0]).split()[1]))
    thrs.append(int(str(df[5]).split()[1]))
    filename = str(i) + "/avg_lat.txt"
    with open(filename, "r") as f:
        for line in f:
            lat = float(line.strip())
    dict = {'Iteration': i, 'Service Latency [ms]': lat, 'Replicas': int(str(df[0]).split()[1]), 'Threshold [%]': THRS_LIST[int(str(df[5]).split()[1])]}
    rows_training.append(dict)


print(rows_training[0])

avg_lat_list = []
SLA = [1000]*1200
for i in list(range(0, 1200)):
    filename = path+str(i) + "/avg_lat.txt"
    with open(filename, "r") as f:
        for line in f:
            avg_lat_list.append(float(line.strip()))


thrs = list(map(lambda x: THRS_LIST[x], thrs))

fig,ax = plt.subplots()
ax.plot(set_steps, pods, linestyle='-', color="red")
# set x-axis label
ax.set_xlabel("ITERATIONS", fontsize=18)
# set y-axis label
ax.set_ylabel("REPLICAS", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(set_steps, avg_lat_list, linestyle='-', color="blue")
ax2.set_ylabel("LATENCY [ms]", color='blue', fontsize=18)
plt.axhline(1000, color='limegreen', linewidth=5, label='SLA')
#plt.title("TRAINING REPLICAS & LATENCY", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.axis(ymin=0, xmin=0, xmax=set_steps[-1])
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
#ax.set_xticks(np.arange(len(x_axis_cpu)), fontsize=18)
plt.grid()
plt.show()


fig,ax = plt.subplots()
ax.plot(set_steps, thrs, linestyle='-', color="red")
# set x-axis label
ax.set_xlabel("ITERATIONS", fontsize=18)
# set y-axis label
ax.set_ylabel("CPU USAGE THRESHOLD [%]", color='red', fontsize=18)
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(set_steps, avg_lat_list, linestyle='-', color="blue")
ax2.set_ylabel("LATENCY [ms]", color='blue', fontsize=18)
plt.axhline(1000, color='limegreen', linewidth=5, label='SLA')
#plt.title("TRAINING THRESHOLDS & LATENCY", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.axis(ymin=0, xmin=0, xmax=set_steps[-1])
plt.yticks(fontsize=18)
plt.legend(fontsize=18)
#ax.set_xticks(np.arange(len(x_axis_cpu)), fontsize=18)
plt.grid()
plt.show()


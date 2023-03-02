from tkinter import * 
import networkx as nx
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 

# plot function is created for plotting the graph in tkinter window 
def plot(): 
    # read edges and nodes
    edges = pd.read_csv("edges.csv", header=0)
    nodes = pd.read_csv("nodes.csv", header=0)
    nodes = nodes.drop_duplicates()

    # create network graph
    G = nx.from_pandas_edgelist(edges, 'source', 'target', edge_attr=['weight'])

    source = [s for s, t in G.edges() if t == 'b']
    target = [t for s, t in G.edges() if s == 'b']

    values = []
    for n in G.nodes:
        if n in source:
            values.append('#CD5454')
        elif n in target:
            values.append('#8FCD54')
        else:
            values.append('#748DB1')

    # Specify the edges you want here
    red_edges = [('a', 'b'), ('c', 'b'),
                ('d', 'b'), ]
    blue_edges = [edge for edge in G.edges() if edge not in red_edges]

    # Need to create a layout when doing separate calls to draw nodes and edges
    pos = {'a': (20, 30), 'c': (20, 40), 'd': (20, 50), 'b': (30, 40), 'e': (
        40, 30), 'f': (40, 40), 'g': (40, 50), 'h': (40, 60)}  # nx.spring_layout(G)
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    width = stats.rankdata([G[u][v]['weight'] for u, v in G.edges()])


    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                        node_color=values, node_size=500)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges,
                        edge_color='r', arrows=True, width=width)
    nx.draw_networkx_edges(G, pos, edgelist=blue_edges,
                        edge_color='b', arrows=True, width=width)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # The figure that will contain the plot 
    fig = Figure(figsize = (5, 5), 
                 dpi = 100) 
  
    y = [i**2 for i in range(101)] 
    plot1 = fig.add_subplot(111) 
    plot1.plot(y) 
  
    fig = plt.figure(1)
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = window)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   window) 
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 
  
# the main Tkinter window 
window = Tk() 
  
# setting the title  
window.title('Plotting in Tkinter') 
  
# dimensions of the main window 
window.geometry("500x500") 
  
# button that displays the plot 
plot_button = Button(master = window,  
                     command = plot, 
                     height = 2,  
                     width = 10, 
                     text = "View network") 
  
l1 = Label(master = window,
         text="CSV file path")
l2 = Label(master = window,
         text="ID")

e1 = Entry(master = window)
e2 = Entry(master = window)

# place the button  
# in main window 

l1.pack()
e1.pack()
l2.pack()
e2.pack()
plot_button.pack() 

# run the gui 
window.mainloop() 

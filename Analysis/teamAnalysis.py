import pandas as pd
import ijson
import plotly.plotly as py
from plotly.graph_objs import *
import matplotlib.pyplot as plt
import networkx as nx
import pickle

def dumpTeamPkl(x): #Creates a pickle file of a list of the teammate pairs and weighted values for the input file, X
    df = pd.read_pickle(x)
    listOfVals = []
    df['Teammates'] = df['Teammates'].apply(lambda x: x.sort_values('Stat', ascending = False))
    pd.Series(df.index).apply(lambda x: pd.Series(df.loc[x]['Teammates'].index).apply(lambda y: listOfVals.append((x, y, df.loc[x]['Teammates'].loc[y]['Stat']))))
    with open('./Pickle_Files/OU-1695_teammates.pkl', 'wb') as f:
        pickle.dump(listOfVals, f)
    return listOfVals

def generateGraph(data =""): #Generates a graph and maps each teammate to each other, assuming only a positive correlation
    #MAJOR ISSUE: Data is bi-directional but graph is not. In other words, increase in freq of poke1 based on appearence of poke2
    #is different than increase in freq of poke2 based on poke1
    if data == "":
        with open('./Pickle_Files/OU-1695_teammates.pkl', 'rb') as f:
            data = pickle.load(f)
    df = pd.DataFrame.from_records(data, columns = ['Teammate 1', 'Teammate 2', 'Stat'])
    filteredDf = df[(df.Stat > 0.0)]
    filteredDf['Stat'] = filteredDf['Stat'].apply(lambda x: float(x))
    subset = filteredDf[['Teammate 1', 'Teammate 2', 'Stat']]
    edges = [tuple(x) for x in subset.values]
    first_list = list(filteredDf['Teammate 1'])
    second_list = list(filteredDf['Teammate 2'])
    G = nx.Graph()
    G.add_nodes_from(list(set(first_list + list(set(second_list) - set(first_list)))))
    for i,j,k in edges:
        if(k >= 1000):
            print('%s & %s: %s' % (i, j, k))
        G.add_edge(i,j,length = (1.0/k), weight = 1.0/k)
    return(G)

def getShortedPath(G, poke1, poke2): #Returns the shortest path between two pokemon
    prevPoke = poke1
    currentPoke = poke2
    data = []
    generator = nx.all_shortest_paths(G, source = poke1, target = poke2, weight = 'weight')
    for j in generator:
        pokemon = list(j)
        for i in pokemon:
            currentPoke = i
            if(i != poke1):
                data.append((prevPoke, currentPoke, G[prevPoke][currentPoke]['length']))
                prevPoke = currentPoke
    return data
def plotGraph(G): #Plots a given graph, G
    pos = nx.spring_layout(G)
    print(pos)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(node)
    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                     title='<br>Network graph made with Python',
                     titlefont=dict(size=16),
                     showlegend=False,
                     hovermode='closest',
                     margin=dict(b=20, l=5, r=5, t=40),
                     annotations=[dict(
                         text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                         showarrow=False,
                         xref="paper", yref="paper",
                         x=0.005, y=-0.002)],
                     xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                     yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    py.plot(fig)
if __name__ == "__main__":
    G = generateGraph()
    data = getShortedPath(G, 'Kingdra', 'Gigalith')
    for i,j,k in data:
        print('%s & %s: %s' %(i,j,1.0/k))






import pandas as pd
import ijson
import plotly.plotly as py
from plotly.graph_objs import *
import matplotlib.pyplot as plt
import networkx as nx
import pickle

def getUsage(df, poke): #Returns usage of pokemon given dataframe and pokemon
    return df[(df.index == poke)].usage


if __name__ == "__main__":
    df = pd.read_pickle('./Pickle_Files/OU-1695.pkl')
    print(getUsage(df, 'Medicham-Mega'))
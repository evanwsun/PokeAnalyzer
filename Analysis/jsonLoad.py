import pandas as pd
import ijson

filename = '../Data/2018-03/chaos/gen7ou-1695.json'

def pklDatabase(filename, savename): #Loads a database given a filename into a pickle
    frames = {}
    with open(filename, 'r') as f:
        database = (ijson.items(f, 'data'))
        database = dict(list(database)[0])
        percent = 0
        print(database)
        frames['Pokemon'] = list(database.keys()) # Gets all pokemon in a list
        for i in list(dict(list(database.values())[0]).keys()): # Gets all columns
            frames[i] = []
        for key in database.keys(): # Processes the data for each pokemon
            print(percent * 1.0/len(database.keys()))
            percent +=1
            columns = database[key]
            dicto = dict(columns)
            for key1, value1 in dicto.items():
                if((key1 != 'usage') and (key1 != 'Viability Ceiling') and (key1 != 'Raw count')):
                    dicto[key1] = dict(value1)
                    newDat = pd.DataFrame(([i, j] for i, j in dicto[key1].items()), columns=[str(key1), 'Stat'])
                    newDat = newDat.set_index(key1)
                    frames[key1].append(newDat)
                else:
                    frames[key1].append(value1)

    dataframe = pd.DataFrame.from_dict(frames, orient = 'columns')
    dataframe = dataframe.set_index('Pokemon')
    print(list(dataframe.index))
    dataframe.to_pickle(savename + '.pkl')

if __name__ == "__main__":
    pklDatabase(filename, 'Pickle_Files/OU-1695')




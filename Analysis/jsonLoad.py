import pandas as pd
import ijson

filename = 'sample.json'


if __name__ == "__main__":
    with open(filename, 'r') as f:
        objects = ijson.items(f, 'data.Swellow')
        columns = list(objects)
        #print(columns)
        dicto = dict(columns[0])
        keys = []
        frames = []
        dataframe = pd.DataFrame(columns = ['Pokemon', 'Moves'])
        for key, value in dicto.items():
            if((key != 'usage') and (key != 'Viability Ceiling') and (key != 'Raw count')):
                dicto[key] = dict(value)
                frames.append(pd.DataFrame(([i, j] for i, j in dicto[key].items()), columns=[str(key), 'Stat']))
            else:
                frames.append(value)
            keys.append(key)
        data = {'Pokemon': ['Swellow']}
        data.update({keys[i]:[frames[i]] for i in range(len(keys))})
        data1 = pd.DataFrame(data, index = [0])
        dataframe = dataframe.append(data1, ignore_index=True)
        print(dataframe['Teammates'][0])

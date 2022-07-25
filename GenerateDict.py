import pandas as pd 

def generateDict (df, col):
    d = {}

    for i in range(len(df)):
        if d.get(df.loc[i, "Material"]) == None:
            d[df.loc[i, "Material"]] = {}
        d[df.loc[i, "Material"]][df.loc[i, "Batch"]] = str(df.loc[i, col])
        print(df.loc[i, "Material"], type(df.loc[i, "Material"]))
        print(df.loc[i, "Batch"], type(df.loc[i, "Batch"]))
        print(df.loc[i, "Storage location"], type(df.loc[i, "Storage location"]))
    return d 
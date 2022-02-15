import pandas as pd
import pickle
import time

def g_scr():
    d_iter = pd.read_csv("../patent_databases/uspatentcitation.tsv", sep="\t",
                        usecols=["patent_id", "citation_id"],
                        chunksize=1000000, low_memory=False)
    print("\nCreating graph...")
    start = time.time()
    graph_dict = {}
    i = 0
    for chunk in d_iter:
        hfsize = int(len(chunk.index)/4)
        chunk = chunk.loc[:hfsize].copy(deep=True)
        for row in chunk["patent_id"]:
            if graph_dict.__contains__(row):
                graph_dict[row].append(chunk["citation_id"][i])
            else:
                l = []
                l.append(chunk["citation_id"][i])
                graph_dict[row] = l
            i = i + 1
    end = time.time()
    print(i)
    print("\nGraph creation took", int(end - start),
        "secs, finishing up pickling...")

    x_pickled = open("../generated_data/ind.ptcdb.graph","wb")
    pickle.dump(graph_dict, x_pickled)
    x_pickled.close()

g_scr()

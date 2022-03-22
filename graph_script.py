import pandas as pd
import pickle
import time
import random

def g_scr():
    d_iter = pd.read_csv("../patent_databases/uspatentcitation.tsv", sep="\t",
                        usecols=["patent_id", "citation_id"],
                        chunksize=250000, low_memory=False)
    print("\nCreating graph and selecting indices...")
    start = time.time()
    graph_dict = {}
    indices_dict = {}
    i = 0
    for chunk in d_iter:
        # chunk = chunk.loc[:int(len(chunk.index)/4)].copy(deep=True)
        rand_indices = random.sample(list(chunk["patent_id"]), k=100)#int(len(chunk.index)/100)) # 1000/1 of chunk even smaller
        rand_indices.sort()
        print(chunk.head())
        chunk = chunk.set_index("patent_id")
        #print(chunk.head())
        for index in rand_indices:
            try:
                located = chunk.loc[index]["citation_id"]
            except Exception as e:
                pass
            cites_in_index = []
            if isinstance(located, str):
                #print("str")
                cites_in_index = [located]
            else:
                #print("list")
                cites_in_index = located.to_list()
            if index not in indices_dict.keys():
                for cite in cites_in_index:
                    if rand_indices.count(cite) == 0:
                        #print(len(rand_indices))
                        #print(rand_indices.count(cite))
                        #print(cite)
                        rand_indices.append(cite)
                    else:
                        pass
                indices_dict[index] = i
                graph_dict[index] = cites_in_index
                i = i + 1
            else:
                for cite in cites_in_index:
                    graph_dict[index].append(cite)
                    #print(len(cites_in_index))
                    #print(type(cite))
                    #print(rand_indices.count(cite))
                    if rand_indices.count(cite) == 0:
                        rand_indices.append(cite)
                    else:
                        pass
        print("check_g-", i)


    end = time.time()
    print("\nGraph creation took", int(end - start),
        "secs...")

    return indices_dict, graph_dict

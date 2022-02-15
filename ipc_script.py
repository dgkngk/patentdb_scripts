import pandas as pd
import numpy as np
import pickle
import random
import time

def ipc_scr(test_indices, train_indices):
    d_iter = pd.read_csv("../patent_databases/ipcr.tsv", sep="\t",
                    usecols=["patent_id", "section"],
                    chunksize=250000, low_memory=False)

    ipc_nda = np.zeros(shape=(250000, 8), dtype=int)

    i = 0
    for chunk in d_iter:
        hfsize = int(len(chunk.index)/4)
        chunk = chunk.loc[:hfsize].copy(deep=True)
        for row in chunk["section"]:
            if (row == "A"):
                ipc_nda[i][0] = 1
            elif (row == "B"):
                ipc_nda[i][1] = 1
            elif (row == "C"):
                ipc_nda[i][2] = 1
            elif (row == "D"):
                ipc_nda[i][3] = 1
            elif (row == "E"):
                ipc_nda[i][4] = 1
            elif (row == "F"):
                ipc_nda[i][5] = 1
            elif (row == "G"):
                ipc_nda[i][6] = 1
            elif (row == "H"):
                ipc_nda[i][7] = 1
            i = i + 1

    print(len(ipc_nda))
    print(type(ipc_nda))

    #test_indices = random.sample(range(7814196), k=3907098) # half
    #train_indices = random.sample(test_indices, k=390709) # 5%

    all_pickled = open("../generated_data/ind.ptcdb.ally","wb")
    pickle.dump(ipc_nda, all_pickled)
    all_pickled.close()

    y_pickled = open("../generated_data/ind.ptcdb.y","wb")
    train = ipc_nda[train_indices, :]
    pickle.dump(train, y_pickled)
    y_pickled.close()

    ty_pickled = open("../generated_data/ind.ptcdb.ty","wb")
    test = ipc_nda[test_indices, :]
    pickle.dump(test, ty_pickled)
    ty_pickled.close()



import random
import time
import pickle
import os
import dask.dataframe as dd
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from ipc_script import ipc_scr
from graph_script import g_scr

if os.path.exists("../generated_data/ptdb.tsv"):
    os.remove("../generated_data/ptdb.tsv")

d_iter = pd.read_csv("../patent_databases/patent.tsv",
                     sep="\t",
                     usecols=["id", "abstract", "title"],
                     chunksize=250000,
                     low_memory=False)

tfidf = TfidfVectorizer()


indices_dict, graph_dict = g_scr()
node_dict= {}
indices_list = []

start = time.time()

i = 0
for chunk in d_iter:
    chunk["node_data"] = chunk["title"].astype(
        str) + "," + chunk["abstract"].astype(str)
    chunk.drop(["title", "abstract"], axis=1, inplace=True)

    for row in chunk["id"]:
        i = i + 1
        if row in indices_dict.keys():
            indices_list.append(row)
            node_dict[row]= chunk["node_data"][i]
    print(type(chunk))
    print(chunk.head())
    print(chunk.shape)

print("Graph checking started...") # refactoring the graph
print(len(indices_list))
print(len(indices_dict.keys()))

copy_dict = indices_dict.copy()

for ind in copy_dict.keys():
    if ind not in indices_list:
        indices_dict.pop(ind, None)
print("Pruned.")
i = 0
for ind in indices_dict.keys():
    indices_dict[ind] = i
    i = i + 1
print("Reindexed.")

result_graph = {}
for ind in indices_dict.keys():
    l = []
    for cite in graph_dict[ind]:
        if cite in indices_dict.keys():
            l.append(indices_dict[cite])

    result_graph[indices_dict[ind]] = l

print("Refactored.")
node_data = []
indexes = []

for key in node_dict.keys():
    node_data.append(node_dict[key])
    indexes.append(indices_dict[key])

print("Graph checked.")

print("\nRead operation complete in ", int(time.time() - start),
      " sec, creating sparse matrix...")


ttime = time.time()
tfs = pd.Series(data=node_data, index=indexes)
result = tfidf.fit_transform(tfs)

print(result)
#print(d_iter)
print(len(tfidf.vocabulary_))
print(result.shape)
print(type(result))

print("\ntf-idf evaluation took", int(time.time() - ttime),
      "secs, pickling data...")

# pickling
# random.shuffle(indices_list)
test_indices = random.sample(indexes, k=int(len(indexes)/2))
train_indices = random.sample(indexes,
                              k=int(len(test_indices) / 10))  # 5%

all_pickled = open("../generated_data/ind.ptcdb.allx", "wb")
pickle.dump(result, all_pickled)
all_pickled.close()

x_pickled = open("../generated_data/ind.ptcdb.x", "wb")
train = result.tocsr()[train_indices, :]
pickle.dump(train, x_pickled)
x_pickled.close()

tx_pickled = open("../generated_data/ind.ptcdb.tx", "wb")
test = result.tocsr()[test_indices, :]
pickle.dump(test, tx_pickled)
tx_pickled.close()

#index = open("../generated_data/ind.ptcdb.test.index", "w")
    #for i in indices_dict.keys():
        #index.write(str(indices_dict[i]) + "\n")
    #index.close()

index = open("../generated_data/ind.ptcdb.test.index", "w")
for i in test_indices:
    index.write(str(i) + "\n")
index.close()

ipc_scr(test_indices, train_indices, indices_dict)

end = time.time()

print("pick2")
x_pickled = open("../generated_data/ind.ptcdb.graph","wb")
pickle.dump(result_graph, x_pickled)
x_pickled.close()


print("\nProcessing took", int(end - start), "sec to execute")


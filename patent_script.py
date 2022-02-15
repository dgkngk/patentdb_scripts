import pandas as pd
import dask.dataframe as dd
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import time
import pickle
from ipc_script import ipc_scr
#from graph_script import g_scr


d_iter = pd.read_csv("../patent_databases/patent.tsv", sep="\t",
                     usecols=["id", "abstract", "title"],
                     chunksize=1000000, low_memory=False)

tfidf = TfidfVectorizer()


start = time.time()

for i, chunk in enumerate(d_iter):
    hfsize = int(len(chunk.index)/4)
    chunk = chunk.loc[:hfsize].copy(deep=True)
    chunk["node_data"] = chunk["title"].astype(
        str) + "," + chunk["abstract"].astype(str)
    chunk.drop(["title", "abstract"], axis=1, inplace=True)
    print(type(chunk))
    print(chunk.head())

    mode = 'w' if i == 0 else 'a'
    header = i == 0

    chunk.to_csv("../generated_data/ptdb.tsv", sep='\t',
                 header=header, mode=mode)

print("\nGeneration complete in ", int(time.time() - start),
      " sec, creating sparse matrix...")

ttime = time.time()

dd_tsv = dd.read_csv("../generated_data/ptdb.tsv", sep='\t',
                     blocksize='64mb', low_memory=False)
result = tfidf.fit_transform(dd_tsv["node_data"])

#print(d_iter)
print(len(tfidf.vocabulary_))
print(result.shape)
print(type(result))

print("\ntf-idf evaluation took", int(time.time() - ttime),
      "secs, pickling data...")

# pickling

test_indices = random.sample(range(250000), k=125000) # half
train_indices = random.sample(test_indices, k=12500) # 5%

all_pickled = open("../generated_data/ind.ptcdb.allx","wb")
pickle.dump(result, all_pickled)
all_pickled.close()

x_pickled = open("../generated_data/ind.ptcdb.x","wb")
train = result.tocsr()[train_indices, :]
pickle.dump(train, x_pickled)
x_pickled.close()

tx_pickled = open("../generated_data/ind.ptcdb.tx","wb")
test = result.tocsr()[test_indices, :]
pickle.dump(test, tx_pickled)
tx_pickled.close()

index = open("../generated_data/ind.ptcdb.test.index", "w")
for i in test_indices:
    index.write(str(i)+"\n")
index.close()

ipc_scr(test_indices, train_indices)
#g_scr()

end = time.time()
print("\nProcessing took", int(end - start), "sec to execute")

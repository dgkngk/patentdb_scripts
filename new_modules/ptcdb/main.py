import os

from refactor_data import data_refactorizer

filelist = [
    "./olddata/ind.ptcdb.graph", "./olddata/ind.ptcdb.allx",
    "./olddata/ind.ptcdb.ally"
]

for f in filelist:
    if not os.path.exists(f):
        exit()

rfd = data_refactorizer(filelist)

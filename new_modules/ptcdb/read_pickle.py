import pickle

class data_reader:
    def __init__(self, pickfiles):
        self.picklist = []
        for f in pickfiles:
            try:
                with open(f, 'rb') as readfile:
                    pick = pickle.load(readfile)
                    self.picklist.append(pick)
            except Exception as e:
                print("encountered:",e)

    def get_picks(self):
        return self.picklist




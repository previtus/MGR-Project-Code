# DataOperations.py
import pickle

''' todo: return false/true and take into account fails  '''

def SaveDataFile(name, Segments):
    with open(name, 'wb') as f:
        pickle.dump(Segments, f)
        print "Saved |", len(Segments), "| segments."

def LoadDataFile(name):
    Segments = []
    with open(name) as f:
        Segments = pickle.load(f)

    print "Loaded |", len(Segments), "| segments."
    return Segments


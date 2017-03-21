import cPickle as pickle

def load_classifiers ():
    try:
        classifiers_list = pickle.load(open("classifiers_list.pickle", "rb"))
    except (OSError, IOError) as e:
        classifiers_list = []
        pickle.dump(classifiers_list, open("classifiers_list.pickle", "wb"))

    return classifiers_list

def save_classifiers (classifiers_list):
    pickle.dump(classifiers_list, open("classifiers_list.pickle", "wb"))

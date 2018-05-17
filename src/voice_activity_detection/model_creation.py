import numpy as np
import pandas as pd
from sklearn import tree
import random
import copy
from sklearn.tree import _tree
# from xml.etree.ElementTree import Element,SubElement,tostring
# from xml.etree import ElementTree
# from xml.dom import minidom
import json


EXTRACTED_FEATURES_NUMPY_FILE = "/Users/siva/Documents/speaker_recognition/numpy_files/voice_activity_detection_test_mar_15.npy"
JSON_FILE_PATH = "/Users/siva/Documents/speaker_recognition/"
JSON_FILE_NAME = "voice_activity_detection.json"

def load_data():
    voice_noise_data = np.load(EXTRACTED_FEATURES_NUMPY_FILE).item()
    voice_noise_df = pd.DataFrame.from_dict(voice_noise_data)
    voice_noise_df.replace([np.inf,-np.inf,np.nan],0)
    voice_noise_df.dropna()

    voice_noise_df["audio"] = voice_noise_df["audio"].astype('category')
    voice_noise_df["audio"] = voice_noise_df["audio"].cat.codes

    data = voice_noise_df.loc[:,voice_noise_df.columns != "audio"].as_matrix()
    labels = voice_noise_df["audio"].as_matrix()

    full_data = np.hstack((data,np.expand_dims(labels,axis = 1)))
    random.shuffle(full_data)
    data = full_data[:,0:-1]
    labels = full_data[:,-1]

    nan_indices = np.where(np.isnan(data))
    all_indices_ = np.ones(len(data),dtype = "bool")
    all_indices_[nan_indices[0]] = False
    data_ = copy.deepcopy(data[all_indices_,:])
    labels_ = copy.deepcopy(labels[all_indices_])
    return (data_,labels_)

def build_model(data,labels):
    classifier = tree.DecisionTreeClassifier(max_depth=3)
    classifier = classifier.fit(data, labels)
    return classifier

def tree_to_json_final(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    json_file = {}

    def recurse(node, depth, json_file):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            json_file["feature"] = name
            json_file["threshold"] = threshold
            json_file["decision"] = None
            print("{}if {} <= {}:".format(indent, name, threshold))
            try:
                temp = json_file["left"]
            except:
                json_file["left"] = {}
            recurse(tree_.children_left[node], depth + 1, json_file["left"])
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            try:
                temp = json_file["right"]
            except:
                json_file["right"] = {}
            recurse(tree_.children_right[node], depth + 1, json_file["right"])
        else:
            print("{}return {}".format(indent, tree_.value[node]))
            json_file["decision"] = str(np.argmax(tree_.value[node]) == 1)
            json_file["threshold"] = 0.0
            json_file["feature"] = None
            json_file["left"] = None
            json_file["right"] = None
            return json_file

    recurse(0, 1, json_file)
    print(json.dumps(json_file, sort_keys=True, indent=4))
    with open(JSON_FILE_NAME, "w") as file:
        json.dump(json_file, file)

def main():
    data,labels = load_data()
    print("*****************loaded data************")
    tree = build_model(data,labels)
    print("*********built the classifier***********")
    tree_to_json_final(tree,["RMS","ZCR","bandwidth","nwpd","rse",\
                                "spectral_centroid","spectral_flux",\
                                "spectral_rolloff"])
    print("*********created json file****************")


if __name__ == "__main__":
    main()
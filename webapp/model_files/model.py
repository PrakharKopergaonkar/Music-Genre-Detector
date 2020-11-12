import os
import pickle
import random 
import operator
import math

import random
import scipy.io.wavfile as wav
from python_speech_features import mfcc
import numpy as np

def loadDataset(filename, split):
    dataset = []
    training_Set = []
    testing_Set = []
    with open(filename, 'rb') as f:
        while True:
            try:
                dataset.append(pickle.load(f))
            except EOFError:
                f.close()
                break
            for x in range(len(dataset)):
                if(random.random() < split):
                    training_Set.append(dataset[x])
                else:
                    testing_Set.append(dataset[x])
    return dataset

class Model:
    def distance(self,instance1, instance2, k):
        distance =0 
        mm1 = instance1[0] 
        cm1 = instance1[1]
        mm2 = instance2[0]
        cm2 = instance2[1]
        distance = np.trace(np.dot(np.linalg.inv(cm2), cm1)) 
        distance+=(np.dot(np.dot((mm2-mm1).transpose() , np.linalg.inv(cm2)) , mm2-mm1 )) 
        distance+= np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
        distance-= k
        return distance
    
    def getNeighbors(self,instance, k,dataset):
        distances = []
        for x in range (0,len(dataset)):
            dist = self.distance(dataset[x], instance, k)+ self.distance(instance, dataset[x], k)
            distances.append((dataset[x][2], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(0,k):
            neighbors.append(distances[x][0])
        return neighbors
    
    def nearestClass(self,neighbors):
        classVote = {}
        for x in range(0,len(neighbors)):
            response = neighbors[x]
            if response in classVote:
                classVote[response]+=1 
            else:
                classVote[response]=1
        sorter = sorted(classVote.items(), key = operator.itemgetter(1), reverse=True)
        return sorter[0][0]
    
    
    


# dataset = loadDataset("my.dat",0.66)

def predict_genre(filename,dataset,model):
        result = {1: 'blues', 2: 'classical', 3: 'country', 4: 'disco', 5: 'hiphop', 6: 'jazz', 7: 'metal', 8: 'pop', 9: 'reggae', 10: 'rock'}
        (rate,sig) = wav.read(filename)
        mfcc_feat = mfcc(sig,rate ,winlen=0.020, appendEnergy = False)
        covariance = np.cov(np.matrix.transpose(mfcc_feat))
        mean_matrix = mfcc_feat.mean(0)
        feature = (mean_matrix , covariance , 10)
        pred=model.nearestClass(model.getNeighbors(feature , 5,dataset))
        return result[pred]
    
# Save mode
with open("model.bin", "wb") as f_out:
    knn = Model()
    pickle.dump(knn,f_out)
    f_out.close()

# with open("model.bin", "rb") as f_in:
#     model = pickle.load(f_in)
#     dataset = loadDataset("my.dat",0.66)
#     print(predict_genre("../../testing_file/test.wav",dataset,model))

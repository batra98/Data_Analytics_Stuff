import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier
from sklearn.metrics import f1_score

class Submission():
    def __init__(self, train_data_path, test_data_path):
        self.train_data = pd.read_csv(train_data_path, header=None)
        self.test_data = pd.read_csv(test_data_path)

    def predict(self):
        # Split the training data into x and y
        X_train,y_train = self.train_data.iloc[:,:-1], self.train_data.iloc[:,-1]
        
        # Train the model
        classifier = RandomForestClassifier(random_state = 1)
        classifier.fit(X_train, y_train)
        # print(f1_score(classifier.predict(X_train),y_train,average = 'weighted'))

        
        # Predict on test set and save the prediction
        submission = classifier.predict(self.test_data)
        submission = pd.DataFrame(submission)
        submission.to_csv('submission.csv',header=['quality'],index=False)


# s = Submission('./train.csv','./test.csv')
# s.predict()
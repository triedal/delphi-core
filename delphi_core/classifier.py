"""This module provides the class used to classify PE files."""

from feature_miner import PEMiner
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from config import cfg
import logging


CLASSIFICATION_TYPES = {
    'malware': 1,
    'benign': 0
}

class Classifier(object):
    """Classifier used to predict malware."""
    def __init__(self):
        self.clf = DecisionTreeClassifier()
        self.__train_model()

    def __train_model(self):
        """Trains classification model."""
        miner = PEMiner()
        df = miner.get_feature_set()

        # x: all but "Type" column
        # y: only "Type" column
        x_train, x_test, y_train, y_test = train_test_split(df[df.columns.difference(['Type'])], df['Type'],
                                                            test_size=cfg['test_size'], random_state=42)

        # Convert 'malware' and 'benign' to ints
        y_train = y_train.apply(lambda x: CLASSIFICATION_TYPES[x])
        y_test = y_test.apply(lambda x: CLASSIFICATION_TYPES[x])

        self.clf.fit(x_train, y_train)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    clf = Classifier()
    
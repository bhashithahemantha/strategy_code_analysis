import numpy as np
import pandas as pd
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from data_extraction import get_data
import encoding_data as ed

from dython.model_utils import roc_graph
from dython.nominal import associations
data = ed.data_encoding(pd.DataFrame(get_data()))
print(type(data))
print(data.head())
print(data.columns.values)


# def roc_graph_example():
#     # Based on sklearn examples (as was seen on April 2018):
#     # http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
#     iris = datasets.load_iris()
#     X = iris.data
#     y = label_binarize(iris.target, classes=[0, 1, 2])
#     random_state = np.random.RandomState(0)
#     n_samples, n_features = X.shape
#     X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=0)
#     classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=random_state))
#     y_score = classifier.fit(X_train, y_train).decision_function(X_test)
#     roc_graph(y_test, y_score)

# def associations_example():
#     iris = datasets.load_iris()
#     X = pd.DataFrame(data=iris.data, columns=iris.feature_names)
#     y = pd.DataFrame(data=iris.target, columns=['target'])
#     df = pd.concat([X, y], axis=1)
#     associations(df,nominal_columns=['target'])


def associations_example():
    df = pd.DataFrame(data=data, columns=data.columns.values)
    associations(df,nominal_columns=data.columns.values)

associations_example()
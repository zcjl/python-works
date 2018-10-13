# Compare Algorithms
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV

# load dataset
filename = 'test_data.csv'
names = ['a', 'b', 'c', 'd', 'tag']
dataframe = read_csv(filename, names=names, header=0)
array = dataframe.values
X = array[:, 0:4]
Y = array[:, 4]
Y = Y.astype('bool')
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.1, random_state=42)

clf = LogisticRegressionCV(random_state=None)
clf.fit(X_train, y_train)

print clf.score(X_test, y_test)

print clf.predict([[1, 1, 1, 8]])

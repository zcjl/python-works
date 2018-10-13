# Compare Algorithms
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# load dataset
filename = 'test_data.csv'
names = ['a', 'b', 'c', 'd', 'tag']
dataframe = read_csv(filename, names=names, header=0)
array = dataframe.values
X = array[:, 0:4]
Y = array[:, 4]
Y = Y.astype('bool')
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=.4, random_state=42)

clf = DecisionTreeClassifier(random_state=0)
clf.fit(X_train, y_train)

print clf.score(X_test, y_test)

print clf.predict([[8, 8, 8, 3]])


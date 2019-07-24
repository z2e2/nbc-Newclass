import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import sys
labeled_dict = pickle.load(open('labeled.pkl', 'rb'))

fold_idx = int(sys.argv[1])

# bootsrap ANCHOR TAXA
y = []
x = []
with open('2005-{}.csv'.format(fold_idx)) as f:
    header = f.readline()
    header = header.strip(',\n').split(',')[1:]
    for line in f:
        line = line.strip(',\n')
        label = line.split(',')[0].split('/')[-2]
        if label in labeled_dict[2005][fold_idx]:
            y.append(0)
            x.append([float(item) for item in line.split(',')[1:]])
        elif label in labeled_dict[2010][fold_idx]:
            y.append(1)
            x.append([float(item) for item in line.split(',')[1:]])
X = np.array(x)
y = np.array(y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=20, max_depth=2,
                             random_state=0)
clf.fit(X_train, y_train)  

pred = clf.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score, flush = True)
print(clf.feature_importances_, flush = True)


print(confusion_matrix(y_test, pred), flush = True)

anchor_taxa = []
for idx, item in enumerate(clf.feature_importances_):
    if item > 0.001:
        # print(header[idx], item)
        anchor_taxa.append(header[idx])
anchor_taxa = set(anchor_taxa)

# TRAIN ON ANCHOR TAXA 
y = []
x = []
with open('2005-{}.csv'.format(fold_idx)) as f:
    header = f.readline()
    header = header.strip(',\n').split(',')[1:]
    taxa_index = []
    for idx, taxon in enumerate(header):
        if taxon in anchor_taxa:
            taxa_index.append((taxon, idx))
    taxa_index = [item[1] for item in sorted(taxa_index)]
    for line in f:
        line = line.strip(',\n')
        label = line.split(',')[0].split('/')[-2]
        if label in labeled_dict[2005][fold_idx]:
            y.append(0)
            x_tmp = np.array([float(item) for item in line.split(',')[1:]])
            x_tmp = x_tmp[taxa_index]
            x.append(x_tmp)
        elif label in labeled_dict[2010][fold_idx]:
            y.append(1)
            x_tmp = np.array([float(item) for item in line.split(',')[1:]])
            x_tmp = x_tmp[taxa_index]
            x.append(x_tmp)
X = np.array(x)
y = np.array(y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=20, max_depth=2,
                             random_state=0)
clf.fit(X_train, y_train)  
pred = clf.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score, flush = True)
print(confusion_matrix(y_test, pred), flush = True)
# TEST
YEAR = [2005, 2010, 2015, 2019]
for i in range(4):
    y = []
    x = []
    year = YEAR[i]
    with open(str(year) + '-{}.csv'.format(fold_idx)) as f:
        header = f.readline()
        header = header.strip(',\n').split(',')[1:]
        taxa_index = []
        for idx, taxon in enumerate(header):
            if taxon in anchor_taxa:
                taxa_index.append((taxon, idx))
        taxa_index = [item[1] for item in sorted(taxa_index)]
        for line in f:
            line = line.strip(',\n')
            label = line.split(',')[0].split('/')[-2]
            if label in labeled_dict[year][fold_idx]:
                y.append(0)
                x_tmp = np.array([float(item) for item in line.split(',')[1:]])
                x_tmp = x_tmp[taxa_index]
                x.append(x_tmp)
            else:
                y.append(1)
                x_tmp = np.array([float(item) for item in line.split(',')[1:]])
                x_tmp = x_tmp[taxa_index]
                x.append(x_tmp)
    X = np.array(x)
    y = np.array(y)
    pred = clf.predict(X)
    score = metrics.accuracy_score(y, pred)
    print(year, flush = True)
    print("accuracy:   %0.3f" % score, flush = True)
    print(confusion_matrix(y, pred), flush = True)

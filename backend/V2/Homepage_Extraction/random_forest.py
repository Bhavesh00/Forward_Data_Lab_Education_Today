import pandas
import pickle
from sklearn import model_selection, preprocessing, metrics, ensemble
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer


# load the dataset
data = open('corpus').read()
labels, texts = [], []
for i, line in enumerate(data.split("\n")):
    content = line.split()
    if content[-1] not in ['0', '1', '2', '3', '4', '5', '6']:
        print(content[-1])
    labels.append(content[-1])
    texts.append(" ".join(content[:-1]))
print("Total item:", len(texts), len(labels))

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

# split the dataset into training and validation datasets
train_x, test_x, train_y, test_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

# label encode the target variable
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
test_y = encoder.fit_transform(test_y)

# word level tf-idf
TFIDF = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}')
TFIDF.fit(trainDF['text'])
train_fe = TFIDF.transform(train_x)
test_fe = TFIDF.transform(test_x)


# print(TFIDF.vocabulary_)


def train_model(classifier, feature_vector_train, label, feature_vector_valid):
    # fit the training dataset on the classifier
    rf = classifier.fit(feature_vector_train, label)

    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    return metrics.accuracy_score(predictions, test_y), rf, predictions


# RF on Word Level TF IDF Vectors
accuracy, classifier, prediction = train_model(ensemble.RandomForestClassifier(), train_fe, train_y, test_fe)
print("RF, WordLevel TF-IDF: ", accuracy)

print(confusion_matrix(prediction, test_y))
print(classification_report(prediction, test_y))
print(accuracy_score(prediction, test_y))

# Save classification model and vectorizer model

with open('Models/text_classifier', 'wb') as picklefile:
    pickle.dump(classifier, picklefile)

with open('Models/vectorizer', 'wb') as picklefile:
    pickle.dump(TFIDF, picklefile)

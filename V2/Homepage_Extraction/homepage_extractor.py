from parse_data import get_connection, get_raw_data, process_data
import pickle

'''
Go through a page. 
Extract information: 
    -Biography
    -Education
    -Awards
    -Research interests
'''
def extract_homepage(homepage_url):
    MODE = 'all'
    # Create a connection to the url and get HTML
    soup = get_connection(homepage_url)
    # Parse the raw text from HTML
    raw_data = get_raw_data(soup)
    # Do preprocessing on raw data extracted
    data = process_data(raw_data,mode=MODE)

    # Load both models
    model, vector = load_model()
    # Make predictions
    test_vec = vector.transform(data)
    prediction = model.predict(test_vec)

    # Present prediction
    print("Prediction:", prediction)
    res = prediction.tolist()
    for i in range(1, len(res) - 1):
        if res[i] == 0:
            if res[i - 1] == res[i + 1] and res[i - 1] in [1, 2, 3, 4]:
                res[i] = res[i - 1]

    # Post-processing based on predictions
    print("Post-Process", res)
    for i in range(len(data)):
        if MODE == 'edu':
            if res[i] == 1:
                print(data[i], '1')
        elif MODE == 'bio':
            if res[i] == 2:
                print(data[i], '2')
        elif MODE == 'research':
            if res[i] == 3:
                print(data[i], '3')
        elif MODE == 'award':
            if res[i] == 4:
                print(data[i], '4')
        elif MODE == 'all':
            if res[i] == 1:
                print(data[i], '1')
            if res[i] == 2:
                print(data[i], '2')
            if res[i] == 3:
                print(data[i], '3')
            if res[i] == 4:
                print(data[i], '4')



def load_model():
    with open('Forward_Data_Lab_Education_Today/V2/Homepage_Extraction/text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)

    with open('Forward_Data_Lab_Education_Today/V2/Homepage_Extraction/vectorizer', 'rb') as vect:
        tfidf_vect = pickle.load(vect)
    return model, tfidf_vect
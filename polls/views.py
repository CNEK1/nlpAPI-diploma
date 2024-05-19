from django.http import JsonResponse 
import pickle
from bs4 import BeautifulSoup
import nltk
import json
from django.views.decorators.csrf import csrf_exempt

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

mlp = pickle.load(open('./models/nlp_model.sav', 'rb'))
vectorizer = pickle.load(open('./models/vectorizer.sav', 'rb'))
scaler = pickle.load(open('./models/scaler.sav', 'rb'))

def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = nltk.stem.PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)
@csrf_exempt
def index(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a GET request"})
    elif request.method == "POST":
        try:
            text = json.loads(request.body)
            text = text["text"]
            text = BeautifulSoup(text,features="html.parser").text
            text = preprocess(text)
            print(text)
            text = vectorizer.transform([text])
            text = scaler.transform(text)
            prediction = mlp.predict(text)
            prediction = {"prediction": prediction.tolist()}

            return JsonResponse(prediction, safe=True) 
        except Exception as e:
            error = json.dumps({'error': str(e)})
            return JsonResponse(error, content_type='application/json', status=400) 
    else:
        return JsonResponse({"message": "This method is not supported"}, status=405) 

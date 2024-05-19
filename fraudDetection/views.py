from django.shortcuts import render
from django.http import JsonResponse
import pickle
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt

# Load your trained MLP model
mlp_model = pickle.load(open('./models/fraud_detection_model.sav', 'rb'))
scaler = pickle.load(open('./models/scaler_fraud_.sav', 'rb'))

# Define any necessary preprocessing steps for your model's input
def preprocess(input_data):
    # Convert input data to DataFrame
    new_data = pd.DataFrame(input_data)
    print(input_data)
    # If 'type' is categorical, convert it to numerical codes as done during training
    if 'type' in new_data.columns and new_data['type'].dtype == 'object':
        new_data['type'] = new_data['type'].astype('category').cat.codes
    # Convert the DataFrame to a numpy array
    return new_data.to_numpy()

@csrf_exempt
def index(request):
    if request.method == "GET":
        return JsonResponse({"message": "This is a GET request"})
    elif request.method == "POST":
        try:
            # Parse the incoming data based on the expected format
            data = json.loads(request.body)
            # Preprocess the features
            features = preprocess(data)
            # Predict using the MLP model
            prediction = mlp_model.predict(features)
            prediction = {"prediction": prediction.tolist()}

            return JsonResponse(prediction, safe=True)
        except Exception as e:
            error = json.dumps({'error': str(e)})
            return JsonResponse(error, content_type='application/json', status=400)
    else:
        return JsonResponse({"message": "This method is not supported"}, status=405)
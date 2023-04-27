from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
from ml.support import transform_input_tensor, give_input_tensor

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        model = joblib.load('ml/model.pkl')
        encoders = joblib.load('ml/encoders.pkl')
        features = joblib.load('ml/features.pkl')
        input_data = {
            "VehicleType": request.POST.get("vehicletype"),
            "Model": request.POST.get("model"),
            "Kilometer": int(request.POST.get("kilometer")),
            "NotRepaired": request.POST.get("notrepaired"),
            "NumberOfPictures": int(request.POST.get("numpictures")),
            "FuelType": request.POST.get("fueltype"),
            "RegistrationYear": int(request.POST.get("regyear")),
            "RegistrationMonth": int(request.POST.get("regmonth")),
            "Gearbox": request.POST.get("gearbox"),
            "Brand": request.POST.get("brand"),
            "PostalCode": int(request.POST.get("postalcode")),
            "Power": int(request.POST.get("power")),
            "DateCrawled": request.POST.get("datecrawled"),
            "DateCreated": request.POST.get("datecreated"),
            "LastSeen": request.POST.get("lastseen")
        }
        print("Input data:", input_data)

        input_data = transform_input_tensor(input_data, encoders)
        print("Transformed input data:", input_data)

        data_tensor = give_input_tensor(features, input_data)
        print("Data tensor shape:", data_tensor.shape)

        prediction = model.predict(data_tensor.reshape(1,-1))[0]
        print("Prediction:", prediction)

        return render(request, 'index.html', {'prediction': prediction, 'predict_price': True})
    else:
        return render(HttpResponse('Not Found'))

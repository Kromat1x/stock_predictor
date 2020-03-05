from flask import Flask, request, render_template, redirect
from flask_api import status
from flask_wtf.csrf import CSRFProtect
from .utils.forms import PaymentForm, StockPriceForm
from .utils.gateway_factory import Gateway
from .ml.lstm import StockPredictor
from keras import backend as K

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
csrf = CSRFProtect()
csrf.init_app(app)

"""
The ProcessPayment method takes care of POST and GET
requests made on the root of the URL.
If the method is GET, then the form will be rendered.
A GET call is needed for the client to receive the
CSRF_token (more on that in the README).

If the method is POST, we validate the data.
The data is validated using flask's built-in
validators, but also my own validators implemented
in validators.py.

If the data is validated, the dictionary obtained is
processed, therefore we get an integer representing
the amount of money. Having the amount, we instantiate
a gateway using the gateway factory: we simply give the
amount as a parameter and the correct gateway will be used.

In case of validation errors, the form is rendered again,
now showing the errors so that the user can correct the
input.
"""
@app.route('/', methods=['POST', 'GET'])
def ProcessPayment():
    form = PaymentForm()
    processed_result = dict()

    if request.method == "GET":
        return render_template('payment_form.html', form=form)
    elif request.method == "POST":
        
        if form.validate():
            result = (request.form).to_dict(flat=False)
            for key, value in result.items():
                processed_result[key] = value[0]
            
            gateway_process = Gateway()
            result = gateway_process.process_transaction(int(processed_result['amount']))
            
            if result[0]:
                return "Payment processed succesfully on the " + result[1], status.HTTP_200_OK
            else:
                return "Payment failed on the " + result[1], status.HTTP_400_BAD_REQUEST
        else:
            
            if len(form.errors) > 0:
                return render_template('payment_form.html', form=form), status.HTTP_400_BAD_REQUEST
            else:
                return render_template('payment_form.html', form=form), status.HTTP_200_OK


"""
The MakePrediction method is similar to the one above
but it has a simpler form, only a date field.
For this method also, a GET call is needed first for
the form to be rendered and also for the client to
receive the CSRF_token (more on that in the README).

For the POST method, the date is validated as follows:
The model is trained on a set of dates and can predict
only dates that are past that set, it cannot predict past
values because that would make no sense and provide no value.

Therefore, the date is received from the form, the StockPredictor
class is instantiated and then the prediction can be made.
* In this state of the project, I have provided a trained model file
and a dataframe file, both needed for prediction. If these two
were to be deleted, the model needs to be trained again.
An example of training can be found at line 98.
"""
@app.route('/predict', methods=['POST', 'GET'])
def MakePrediction():
    form = StockPriceForm()
    processed_result = dict()

    if request.method == "GET":
        return render_template('stock_form.html', form=form)
    elif request.method == "POST":
        if form.validate():
            result = (request.form).to_dict(flat = False)
            for key, value in result.items():
                processed_result[key] = value[0]
            
            predictor = StockPredictor(split_value=24, backward_batch_size=4, model_name="stock_model.h5", dataframe_file="df.pkl")
            # predictor.train('ml/dow_jones_index.csv')
            predicted_result = predictor.predict(processed_result['predictionDate'])
            K.clear_session()
            return "Predicted closing price: " + str(predicted_result), status.HTTP_200_OK
        else:
            if len(form.errors) > 0:
                return render_template('stock_form.html', form=form), status.HTTP_400_BAD_REQUEST
            else:
                return render_template('stock_form.html', form=form), status.HTTP_200_OK

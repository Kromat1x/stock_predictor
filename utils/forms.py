from flask_wtf import FlaskForm
from datetime import date, datetime
from wtforms import StringField, TextField, DateField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError
from .validators import validateExpirationDate, validateCardNumber

class PaymentForm(FlaskForm):
    creditCardNumber = StringField('Credit Card Number', [DataRequired(), validateCardNumber()])
    cardHolder = StringField('Card Holder Name', [DataRequired()])
    expirationDate = DateField('Expiration Date', [DataRequired(), validateExpirationDate(date=date.today(),message="Expiration date cannot be in the past.")], default=date.today())
    securityCode = StringField('Security Code', [Length(min=3, max=3, message="The security code must have exactly 3 digits."), Optional()])
    amount = DecimalField('Amount', [DataRequired(), NumberRange(min=0, message="The amount must be positive.")])
    submit = SubmitField("Submit")

class StockPriceForm(FlaskForm):
    predictionDate = DateField('Prediction Date', [DataRequired(), validateExpirationDate(date=datetime.strptime("07/01/2011", '%m/%d/%Y').date(), message="Date must be greater than 01/07/2011")])
    submit = SubmitField("Sumbit")
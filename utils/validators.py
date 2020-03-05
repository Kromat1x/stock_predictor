from wtforms.validators import ValidationError
from datetime import date

"""
Validates if the date gate from the field
is greater than the date given as an parameter,
in this case everything is fine.
If the date from the field is older than the one
chosen for the comparison, then an error is raised.
"""
class validateExpirationDate(object):
    def __init__(self, date, message):
        self.date = date
        self.message = message
    
    def __call__(self, form, field):
        if (field.data <= self.date):
            raise ValidationError(self.message)


class validateCardNumber(object):
    """
    In the future you may add the possibility to process cards from
    multiple issuers. This can be done in ways such as:
    - Providing a drop-down list for the user to choose and also 
    the user has the possiblity to see the accepted issuers
    - Detect the issuer directly from the card number or, in case
    the card number does not match any issuer, you probably do not
    accept that type of card
    For this proof of concept, we will consider only VISA cards
    """
    def __init__(self, network="VISA"):
        self.network = "VISA"

    def __call__(self, form, field):

        # Transfrom the string of digits into a list of integers
        list_of_digits = [int(i) for i in field.data]
        # Verify if the issuer is the correct one
        if not (self.network == "VISA" and list_of_digits[0] == 4):
            raise ValidationError("Invalid card issuer")
        # Drop the last digit and remember it 
        list_of_digits = list_of_digits[:-1]
        last_digit = list_of_digits[-1]
        # Reverse the list
        list_of_digits.reverse()
        # Multiply by 2 the digits in odd positions (x is a tuple in the map below)
        list_of_digits = list(map(lambda x: x[1] * 2 if x[0] % 2 == 0 else x[1], enumerate(list_of_digits)))
        # Substract 9 from the numbers bigger than 9
        list_of_digits = list(map(lambda x: x - 9 if x > 9 else x, list_of_digits))
        sum_of_digits = sum(list_of_digits)
        sum_of_digits += last_digit

        if sum_of_digits % 10 != 0:
            raise ValidationError("Invalid card number")
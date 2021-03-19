
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validating_number(value):
    valid=True
    if len(value)!=10:
        valid=False
    for i in value:
        if ord(i)>=48 and ord(i)<=57:
            continue
        valid=False
        break
    if not valid:
        raise ValidationError(_("Enter valid phone number!"),code="invalid")



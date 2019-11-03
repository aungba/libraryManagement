from django.core.exceptions import ValidationError

def validate_book_title(value):
    if not ".edu" in value:
        raise ValidationError("A valid book must be entered in")
    else:
        return value
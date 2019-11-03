from django.forms import ModelForm
from .models import BookLoan

class BookLoanForm(ModelForm):
    class Meta:
        model = BookLoan
        fields = ['book_id','borrower','rent_date','due_date','return_date', 'book_borrower']

    def clean(self):
        super(BookLoanForm, self).clean()
        return self.cleaned_data
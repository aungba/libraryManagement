from django import forms
from django.forms import ModelForm
import re

from .models import Book

class DateInput(forms.DateInput):
    input_type = 'date'

class RadioInput(forms.RadioSelect):
    input_type = 'radio'

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_title','book_author','book_publisher','book_summary','book_release_date','book_category','book_status']
        widgets = {
            'book_release_date': DateInput(),
            'book_status': RadioInput()
        }


    def clean(self):
        super(BookForm, self).clean()

        title = self.cleaned_data.get('book_title')
        checkTitle(title,self)
        checkAuthor(self.cleaned_data.get('book_author'), self)
        

        return self.cleaned_data

def checkTitle(title,self):
    if title is not None:
        if len(title) < 5:
            self.errors['book_title'] = self.error_class([
                'Minimum 5 characters required'
            ])
        if title == 'aaaaa':
            self.errors['book_title'] = self.error_class([
                    'Good'
                ])

def checkAuthor(author,self):
    if author is not None:
        pattern = re.compile('(?![0-9]*$)[a-zA-Z0-9]+')
        if len(author) < 5:
            self.errors['book_author'] = self.error_class([
                'Minimum 5 characters required for author name'
            ])
        if not pattern.match(author):
            self.errors['book_author'] = self.error_class([
                'Pattern must be alphanumeric'
            ])
        

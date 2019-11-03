from django.forms import ModelForm
from .models import Category

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_text']

    def clean(self):
        super(CategoryForm, self).clean()
        return self.cleaned_data
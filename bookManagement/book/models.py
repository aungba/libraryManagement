from django.db import models
from .custom_validator import validate_book_title
from django.contrib.auth.models import User

class Category(models.Model):
    category_text = models.CharField(max_length = 200)

    def __str__(self):
        return self.category_text

class BookLoan(models.Model):
    book_id = models.IntegerField()
    borrower = models.CharField(max_length=200)
    rent_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField()
    book_borrower = models.CharField(max_length=200)
    is_return = models.BooleanField(default=False)

    def __str__(self):
        return self.borrower

class Book(models.Model):

    BOOK_CHOICES = (
    (True, 'Available'),
    (False, 'Closed')
)
    book_title = models.CharField(max_length=200, blank = False, null = False)
    book_author = models.CharField(max_length=200, blank = False, null = False)
    book_publisher = models.CharField(max_length=200, blank = False, null = False)
    book_summary = models.TextField(blank= False, null= False)
    book_release_date = models.DateField(blank= False, null= False)
    book_category = models.ForeignKey(Category, on_delete= models.CASCADE)
    latest_book_loan = models.ForeignKey(BookLoan, blank=True,null=True, on_delete= models.CASCADE)
    status = models.BooleanField (default= True , null= False)
    book_status = models.BooleanField(choices=BOOK_CHOICES , default=True)

    def __str__(self):
        return self.book_title







# Create your models here.

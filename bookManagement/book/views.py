from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import *
from django.urls import reverse_lazy
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as dj_login
from django.views.generic import ListView, CreateView, UpdateView
from .models import Book, BookLoan, Category
from .forms import BookForm
from .loan_form import BookLoanForm
from django.views import View
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .category_form import CategoryForm
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
  #  return render(request,'book/login.html')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                log.info('User was successfully logged in .<username> = %s , <password> = %s ', username , password)
                return HttpResponseRedirect('/')
    return render(request,'book/login.html')

#Create your views here.
@login_required(login_url='/login')
def main(request):
    return render(request, 'book/main.html')


# class bookCreateView(LoginRequiredMixin,CreateView):
#     login_url = '/login'
#     redirect_field_name = 'redirect_to'
#     model = Book
#     form_class = BookForm
#     template_name = 'book/book.html'
#     success_url = reverse_lazy('bookList')
#     log.info('Book registration was successful')

@login_required(login_url='/login')
def book_add(request):
    template = 'book/book.html'
    form = BookForm(request.POST or None)
    if form.is_valid():
        model_instance = form.save(commit=False)
        model_instance.timestamp = timezone.now()
        model_instance.save()
        return HttpResponseRedirect('/')
        
    context = {'form': form}
    return render(request, template, context)
            

@login_required(login_url='/login')
def book_list(request, template_name='book/bookList.html'):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, template_name, data)

@login_required(login_url='/login')
def book_edit(request, pk, template_name='book/bookEdit.html'):
    book= get_object_or_404(Book, pk=pk)
    log.info('Getting book was successful , book_id : %d , book : %s ', pk, str(book))
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        log.info('Book editing was successful , book : ', str(form))
        return redirect('bookList')
    return render(request, template_name, {'form':form})

class book_delete(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self, request, pk):
        data = dict()
        book = Book.objects.get(pk=pk)
        if book:
            book.delete()
            log.info('Book deleting was successful , book_id : %d ', pk)
            data['message'] = "Book deleted!"
        else:
            log.error('Book deleting was failed , book_id : %d ', pk)
            data['message'] = "Error!"
        return JsonResponse(data)

@login_required(login_url='/login')
def book_borrow(request, pk , template_name='book/book_loan.html'):
    book = get_object_or_404(Book, pk=pk)
    users = User.objects.all()

    if request.POST:
        select_val = request.POST['Customer']
        rent_date = datetime.datetime.today()
        due_date = rent_date + datetime.timedelta(days=14)
        return_date = due_date
        model = BookLoanForm({
            'book_id': pk,
            'borrower': request.user,
            'rent_date': rent_date,
            'due_date': due_date,
            'return_date': return_date,
            'book_borrower': select_val
        }) 
        if model.is_valid():
            print('ok')
            model.save()
            aaa= BookLoan()
            loan_obj = BookLoan.objects.latest('id')
            latest_id = loan_obj.id


            book = get_object_or_404(Book, pk=pk)
            book.status = False
            book.latest_book_loan = loan_obj
            book.save()
            log.info('Book lending was successful , book_id : %d ', pk)
            return redirect('bookList')
    return render(request, template_name, {'book': book, 'users': users})

class bookList(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        book = list(Book.objects.all().values(
            'id',
            'book_title',
            'book_author',
            'book_publisher',
            'book_status',
            'book_release_date',
            'status',
            'book_category__category_text',
            'latest_book_loan__due_date'))
        data = {}

        for item in book:
            if item.get('status'):
                item['latest_book_loan__due_date'] = ''

        data['books'] = book
        log.info('Retrieving book list was successful, bookList = %s ', str(book))
        return JsonResponse(data)


class bookReturn(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self, request, bookId):
        data = {}
        book = Book.objects.get(pk=bookId)
        if book:
            book.status = True
            book.save()
            book_loan = BookLoan.objects.get(book_id=bookId)
            if book_loan:
                book_loan.is_return = True
                book_loan.save()
                log.info('book returning was successful, book_id : %d , book : %s ', bookId, str(book))
                data['message'] = 'Book Updated'
            else:
                data['message'] = 'Book Updated Error'
                log.error('book returning was failed')
        return JsonResponse(data)

@login_required(login_url='/login')
def categoryList(request, template_name='book/categoryList.html'):
    category = Category.objects.all()
    data = {}
    data['object_list'] = category
    log.info('Retrieving category list was successful , categoryList : %s ', str(category))
    return render(request, template_name, data)

@login_required(login_url='/login')
def category_edit(request, pk, template_name='book/categoryEdit.html'):
    category = get_object_or_404(Category, pk=pk)
    log.info('Getting cateory was successful , category_id : %d , catetory : %s ', pk, str(cateory))
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        log.info('category editing was successful , catetory : %s ', str(category))
        return redirect('categoryList')
    return render(request, template_name, {'form':form})


class categoryCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Category
    form_class = CategoryForm
    template_name = 'book/category_register.html'
    success_url = reverse_lazy('categoryList')
    log.info('Category creating was successful, category : %s ', str(form_class))


class check_user(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self, request, username):
        data = {}
        count = list(BookLoan.objects.filter(book_borrower__contains = username).filter(is_return = False).values())
        
        data['count'] = len(count)
        log.info('Borrowed user count checking was successful, count : %d ', count)
        return JsonResponse(data)

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

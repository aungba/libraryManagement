# libraryManagement

### Overview ###
This is a libarary management application using django.
User can borrow the book and the total limited number of borrowed book is 3.
User can't borrow the book which was already borrowed by other person and the status was false.
User can also search the book with title, author or publisher and so on.

### Env Setup ###
* Python 3.7
* Visual Studio IDE
* Django==2.2.6
* django-crispy-forms==1.8.0

### Running the program ###
* Go to under project folder and call cmd. And run the following command step by step:
  * python manage.py makemigrations  // to generate the migration file
  * python manage.py migrate // to migrate into sqlite db
  * python manage.py createsuperuser // create admin user that is needed to use to login
  * python manage.py runserver // open the brower and call localhost:8000

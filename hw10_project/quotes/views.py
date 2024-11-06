from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Quote, Author
from .forms import AuthorForm, QuoteForm


def hello(request):
    return HttpResponse("Hello from the quotes app!")


def quote_list(request):
    quotes = Quote.objects.all() # тут отримую всі цитати з бази
    return render(request, 'quotes/quote_list.html', {'quotes': quotes}) # передаю всі отримані цитати на рендер


@login_required(login_url='/users/login/') # оці аргументи в дужках - щоб неавторизованим при спробі зайти на сторінку add-author/ видавало повідомлення, шо ніззя, йди реєструйся
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quote_list')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required(login_url='/users/login/') # оці аргументи в дужках - щоб неавторизованим при спробі зайти на сторінку add-quote/ видавало повідомлення, шо ніззя, йди реєструйся
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quote_list')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})
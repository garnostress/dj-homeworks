from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')
    dates = [book.pub_date.strftime('%Y-%m-%d') for book in books]
    books_info = list(zip(books, dates))
    context = {
        'books_info': books_info,
    }
    return render(request, template, context)


def view_book(request, pub_date):
    books = Book.objects.all().order_by('pub_date')
    dates = [book.pub_date.strftime('%Y-%m-%d') for book in books]
    books_info = list(zip(books, dates))
    paginator = Paginator(list(books), 1)
    template = 'books/books_list.html'
    context = {
        'books_info': books_info,
        'pub_date': pub_date
    }

    if pub_date:
        books = books.filter(pub_date=pub_date)
        dates = [book.pub_date.strftime('%Y-%m-%d') for book in books]
        books_info = list(zip(books, dates))
        book_id = books[0].id
        context['books_info'] = books_info

        next_page = paginator.get_page(book_id).next_page_number() \
            if paginator.get_page(book_id).has_next() else None
        previous_page = paginator.get_page(book_id).previous_page_number() \
            if paginator.get_page(book_id).has_previous() else None

        if next_page:
            next_book = Book.objects.filter(id=next_page)[0]
            next_date = next_book.pub_date.strftime("%Y-%m-%d")
            context['next_date'] = next_date

        if previous_page:
            previous_book = Book.objects.filter(id=previous_page)[0]
            previous_date = previous_book.pub_date.strftime("%Y-%m-%d")
            context['previous_date'] = previous_date

    return render(request, template, context)
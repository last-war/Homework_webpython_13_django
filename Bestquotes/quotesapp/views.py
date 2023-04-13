from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Author, Quote


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})


@login_required
def fill_db(request):
    quotes = Quote.objects.all()
    with open(str(Path(__file__).resolve().parent)+'/static/quotesapp/authors.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        for itr in rez:
            new_author = Author(description=itr['description'][:1000],
                                born_date=datetime.strptime(itr['born_date'], '%B %d, %Y').date(),
                                born_location=itr['born_location'], fullname=itr['fullname'])
            new_author.save()
    # tags
    with open(str(Path(__file__).resolve().parent)+'/static/quotesapp/quotes.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        unique_tags = set()
        for itr in rez:
            for cur_tag in itr['tags']:
                unique_tags.add(cur_tag)
        for unique_tag in unique_tags:
            new_tag = Tag(name=unique_tag)
            new_tag.save()

        for itr in rez:
            new_quote = Quote()
            aut_id = Author.objects.get(fullname=itr['author'])
            new_quote.quote = itr['quote'][0:500]
            new_quote.author = aut_id
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=itr['tags'])
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.save()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})


def detail(request, author_id):
    author_ob = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/detail.html', {"author": author_ob})


def authors(request):
    authors = Author.objects.all()
    return render(request, 'quotesapp/authors.html', {"authors": authors})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = Quote()
            new_quote.quote = request.POST.get('quote')
            new_quote.author = Author.objects.get(fullname=request.POST.get('author'))
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.save()

            quotes = Quote.objects.all()
            return render(request, 'quotesapp/index.html', {"quotes": quotes})
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, "authors": authors, 'form': form})

    return render(request, 'quotesapp/quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})

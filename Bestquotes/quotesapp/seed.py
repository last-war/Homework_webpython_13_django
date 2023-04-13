from datetime import datetime

import json
from models import Tag, Author, Quote


def fill_db():
    with open('static/quotesapp/authors.json', 'r', encoding='utf-8') as fh:
        rez = json.load(fh)
        for itr in rez:
            new_author = Author(description=itr['description'],
                                born_date=datetime.strptime(itr['born_date'], '%B %d, %Y').date(),
                                born_location=itr['born_location'], fullname=itr['fullname'])
            new_author.save()
        """
    
"""

fill_db()
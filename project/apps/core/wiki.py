import requests
from .models import WikiPage

# https://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrsearch=trump&indexpageids=1&gsrlimit=5&prop=pageimages|extracts&pilimit=max&exintro=&explaintext=1&exlimit=max

def search_wikipedia (term, no_results=5, extract_sentences=''):
    # Query params
    atts = {}

    atts['format'] = 'json'
    atts['action'] = 'query'
    atts['generator'] = 'search'
    atts['gsrnamespace'] = '0'
    atts['indexpageids'] = '1' # Include list of page ids
    atts['prop'] = 'pageimages|extracts' # Return content
    atts['explaintext'] = '1' # Remove this to include markup
    atts['exintro'] = '0' # Remove this for entire article
    atts['exlimit'] = 'max' # Extract limit size

    atts['gsrlimit'] = no_results # No. results (default 5)
    # atts['exsentences'] = extract_sentences # Extract limit size (default full)

    atts['gsrsearch'] = term # Search term

    baseurl = 'http://en.wikipedia.org/w/api.php'

    resp = requests.get(baseurl, params = atts)

    data = resp.json()

    page_ids = data['query']['pageids']

    for i in page_ids:
        title = data['query']['pages'][i]['title']
        extract = data['query']['pages'][i]['extract']

        # Dont include disambiguation article in training data
        if "(disambiguation)" not in title:
            wiki_page = WikiPage.objects.get_or_create(
                title = title,
                page_id = i,
                extract = extract
            )

    return page_ids

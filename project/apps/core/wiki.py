import requests
from .models import WikiPage

# https://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrsearch=trump&indexpageids=1&gsrlimit=5&prop=pageimages|extracts&pilimit=max&exintro=&explaintext=1&exlimit=max

def search_wikipedia (term, no_results=5, extract_sentences=''):
    # Query params
    parameters = {}

    parameters['format'] = 'json'
    parameters['action'] = 'query'
    parameters['generator'] = 'search'
    parameters['gsrnamespace'] = '0'
    parameters['indexpageids'] = '1' # Include list of page ids
    parameters['prop'] = 'pageimages|extracts' # Return content
    parameters['explaintext'] = '1' # Remove this to include markup
    parameters['exintro'] = '0' # Remove this for entire article
    parameters['exlimit'] = 'max' # Extract limit size

    parameters['gsrlimit'] = no_results # No. results (default 5)
    parameters['gsrsearch'] = term # Search term

        # parameters['exsentences'] = extract_sentences # Extract limit size (default full)

    baseurl = 'http://en.wikipedia.org/w/api.php'
    resp = requests.get(baseurl, params = parameters)
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

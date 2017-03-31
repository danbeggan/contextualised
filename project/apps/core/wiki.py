import requests
from .models import WikiPage

# https://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrsearch=trump&indexpageids=1&gsrlimit=5&prop=pageimages|extracts&pilimit=max&exintro=&explaintext=1&exlimit=max

def search_wikipedia (term, no_results=5, extract_sentences=''):
    # Query params
    parameters = {}

    parameters['format'] = 'json' # Query format and response type
    parameters['action'] = 'query' # Tell wikipedia this is a query
    parameters['generator'] = 'search' # Type of query
    parameters['gsrnamespace'] = '0'
    parameters['indexpageids'] = '1' # Include list of page ids true
    parameters['prop'] = 'extracts' # What to return - article extract
    parameters['explaintext'] = '1' # No html markup
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

        # Dont include disambiguation articles
        if "(disambiguation)" not in title:
            WikiPage.objects.get_or_create(
                title = title,
                page_id = i,
                extract = extract
            )

    return page_ids

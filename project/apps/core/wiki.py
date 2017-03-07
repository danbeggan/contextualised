import requests

from .models import WikiPage

# https://en.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrsearch=trump&indexpageids=1&gsrlimit=5&prop=pageimages|extracts&pilimit=max&exintro=&explaintext=1&exlimit=max

def search_wikipedia (term):
    atts = {}

    atts['format'] = 'json'   # format=json
    atts['action'] = 'query'  # action=query
    atts['generator'] = 'search'
    atts['gsrnamespace'] = '0'
    atts['indexpageids'] = '1' # Include page ids
    atts['gsrlimit'] = '1' # No. results
    atts['prop'] = 'pageimages|extracts' # Return content
    atts['explaintext'] = '1' # Remove this to include markup
    atts['exintro'] = '' # Remove this for entire article
    atts['exlimit'] = 'max' # Extract limit size

    atts['gsrsearch'] = term # titles=Stanford%20University

    baseurl = 'http://en.wikipedia.org/w/api.php'

    resp = requests.get(baseurl, params = atts)

    data = resp.json()

    pageids = data['query']['pageids']

    wikipage, created = WikiPage.objects.get_or_create(
        title=data['query']['pages'][pageids[0]]['title'],
        pageid=data['query']['pageids'][0],
        extract=data['query']['pages'][pageids[0]]['extract']
    )

    return wikipage

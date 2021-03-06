from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

import json

from .models import WikiPage, Search
from .serializers import SearchSerializer

from .text_processing import TextProcessor
from .classification import Classifier
from .wiki import search_wikipedia
from .pickler import load_classifiers, save_classifiers

classifiers_list = load_classifiers()

class SearchViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Search.objects.all()
        serializer = SearchSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        search = Search.objects.get(pk=pk)
        serializer = SearchSerializer(search)

        return Response(serializer.data)

    # Extract data from reqest, classify, create & return search
    def create(self, request):
        term = request.query_params.get('term', '')
        paragraph = request.query_params.get('paragraph','')

        if term and paragraph:
            term = TextProcessor.remove_punctuation(term)

            # 1 get term lemma
            term_lemma = TextProcessor.get_lemma(term)

            # 2 check if classifier exhists
            classifier = next((x for x in classifiers_list if x.term.lower() == term_lemma), None)

            # 3 NO then create classifier
            if classifier == None:
                # Search wikipedia returns ids for pages & creates models
                wiki_page_ids = search_wikipedia(term_lemma)

                # Creates classifer object
                classifier = Classifier(term, wiki_page_ids)

                classifiers_list.append(classifier)
                save_classifiers(classifiers_list)

            # 4 classify term and paragraph
            wiki_page_id = classifier.classify_text(paragraph)
            wikipage = WikiPage.objects.get(page_id=wiki_page_id)

            search = Search(
                wikipage = wikipage,
                term = term,
                term_lemma = term_lemma,
                paragraph = paragraph
            )
            search.save()

            # Convert object to JSON for response
            serializer = SearchSerializer(search)
            return Response(serializer.data)

        return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    # Use a put
    def update(self, request, pk=None):
        # Get boolean value correct_wiki_returned
        correct_wiki_returned = json.loads(request.query_params.get('correct_wiki_returned', None))
        search = Search.objects.get(pk=pk)

        if correct_wiki_returned != None:
            if correct_wiki_returned:
                # Get the classifer that was used to classifer search
                classifier = next((x for x in classifiers_list if x.term.lower() == search.term_lemma), None)

                # Update classifier to include terms from original search
                classifier.extend_classifier(search.paragraph, search.wikipage.page_id, pk)
                save_classifiers(classifiers_list)

            search.correct_wiki_returned = correct_wiki_returned
            search.save()

            serializer = SearchSerializer(search)

            return Response(serializer.data)
        else:
            return Response({'error': 'search not updated'})

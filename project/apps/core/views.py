from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import WikiPage, Search
from .serializers import SearchSerializer

from .text_processing import TextProcessor
from .classification import Classifier
from .wiki import search_wikipedia

class SearchViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Search.objects.all()
        serializer = SearchSerializer(queryset, many=True)
        return Response(serializer.data)

    # Extract data from reqest, pass to wsd.classify and create & return search
    def create(self, request):
        term = request.query_params.get('term', '')
        paragraph = request.query_params.get('paragraph','')

        if term and paragraph:
            term = TextProcessor.remove_punctuation(term)

            # 1 get term lemma
            term_lemma = TextProcessor.get_lemma(term)

            classifiers_list = []

            # 2 check if classifier exhists
            # 3.1 YES then get classifier [array]
            classifier = next((x for x in classifiers_list if x.value == value), None)

            print '1 @@@@@@@@@@@@@@@@'
            print classifier

            # 3.2 NO then create classifier
            if classifier == None:
                # Search wikipedia returns ids for pages & creates models
                wiki_page_ids = search_wikipedia(term_lemma)
                print '2 @@@@@@@@@@@@@@@@'
                print wiki_page_ids

                # Creates classifer object
                classifier = Classifier(term, wiki_page_ids)
                print '2_1 @@@@@@@@@@@@@@@@'
                print classifier.term

                classifiers_list.append(classifier)

            # 4 classify term and paragraph
            wiki_page_id = classifier.classify_text(paragraph)
            print '3 @@@@@@@@@@@@@@@@'
            print wiki_page_id

            wikipage = WikiPage.objects.get(page_id=wiki_page_id)

            search = Search(
                wikipage = wikipage,
                term = term,
                term_lemma = term_lemma,
                paragraph = paragraph
            )

            search.save()

            serializer = SearchSerializer(search)

            return Response(serializer.data)

        return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

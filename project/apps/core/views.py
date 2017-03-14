from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import Classifier, WikiPage, Search
from .serializers import SearchSerializer

from .text_processing import TextProcessor

class SearchViewSet(viewsets.ViewSet):
    # Static processor for text processing method
    processor = TextProcessor()

    def list(self, request):
        queryset = Search.objects.all()
        serializer = SearchSerializer(queryset, many=True)
        return Response(serializer.data)

    # Extract data from reqest, pass to wsd.classify and create & return search
    def create(self, request):
        term = request.query_params.get('term', '')
        paragraph = request.query_params.get('paragraph','')

        if term and paragraph:
            term = processor.remove_punctuation(term)

            # 1 get term lemma
            term_lemma = get_lemma(term)

            # 2 check if classifier exhists

            # 3.1 YES then get classifier [array]

            # 3.2 NO then create classifier

            # 4 classify term

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

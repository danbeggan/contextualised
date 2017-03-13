from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import WikiPage, Search
from .serializers import SearchSerializer
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

            # Get wikipedia page using paragraph text
            if None is None:
                wikipage = search_wikipedia(term_lemma)

                search = Search(
                    wikipage = wikipage,
                    term = term,
                    term_lemma = term_lemma,
                    paragraph = paragraph
                )

            # Get wikipedia page using disambiguation
            else:
                wikipage = search_wikipedia(term_lemma)

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

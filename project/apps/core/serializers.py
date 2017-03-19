from rest_framework import serializers
from .models import WikiPage, Search

class WikiPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WikiPage
        fields = ('title', 'page_id', 'extract')

class SearchSerializer(serializers.ModelSerializer):
    wikipage = WikiPageSerializer(read_only=True)

    class Meta:
        model = Search
        fields = ('id', 'term', 'term_lemma', 'paragraph', 'wikipage')

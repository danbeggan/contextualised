from rest_framework import serializers
from .models import Disambiguation, WikiPage,  Search

class DisambiguationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disambiguation
        fields = ('synset', 'definition')

class WikiPageSerializer(serializers.ModelSerializer):

    class Meta:
        model = WikiPage
        fields = ('title', 'pageid', 'extract')

class SearchSerializer(serializers.ModelSerializer):
    disambiguation = DisambiguationSerializer(read_only=True)
    wikipage = WikiPageSerializer(read_only=True)

    class Meta:
        model = Search
        fields = ('term', 'term_lemma', 'paragraph', 'disambiguation', 'wikipage')

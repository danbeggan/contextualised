from nltk.wsd import lesk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

from .models import Disambiguation

def classify(term, paragraph):
    wordnet_lemmatizer = WordNetLemmatizer()

    # TODO: add term lemma to the disambiguation object
    term_lemma = wordnet_lemmatizer.lemmatize(term)

    s = lesk(word_tokenize(paragraph), term_lemma)

    if s is None:
        return None, term_lemma
    else:
        # TODO: add lemmas to the disambiguation object
        # lemmas is an array, use .name() to get their values
        lemmas = s.lemmas()

        dis, created = Disambiguation.objects.get_or_create(synset=s.name(), definition=s.definition())
        return dis, term_lemma

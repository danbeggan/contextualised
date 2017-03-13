# from nltk.wsd import lesk
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
#
# from .models import Disambiguation
#
# def classify(term, paragraph):
#     wordnet_lemmatizer = WordNetLemmatizer()
#
#     term_lemma = wordnet_lemmatizer.lemmatize(term)
#
#     s = lesk(word_tokenize(paragraph), term_lemma)
#
#     if s is None:
#         return None, term_lemma
#     else:
#         dis, created = Disambiguation.objects.get_or_create(synset=s.name(), definition=s.definition())
#         return dis, term_lemma

import re

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

class TextProcessor (object):
    # Static
    # Use english stopwords from nltk
    stops = set(stopwords.words("english"))
    tokenizer = RegexpTokenizer(r'\w+')
    wordnet_lemmatizer = WordNetLemmatizer()

    # Takes text (term or paragraph) and removes punctuation
    @classmethod
    def tokenize_text ( cls, text ):
        return cls.tokenizer.tokenize(text)

    # Takes a term of phrase and finds root form
    @classmethod
    def get_lemma ( cls, term ):
        return cls.wordnet_lemmatizer.lemmatize(term)

    # Removes english stopwords from an array of words
    @classmethod
    def remove_stopwords ( cls, words ):
        return [word for word in words if not word in cls.stops]

    # Takes paragraph and returns normalised array
    @classmethod
    def remove_stops_and_lemmatize ( cls, paragraph ):
        # Convert to lower case and split
        words = cls.tokenize_text(paragraph.lower())

        # Remove stopwords
        words = cls.remove_stopwords(words)

        # Lemmatize words
        normalised_words = []
        for word in words:
            normalised_words.append(cls.get_lemma(word))

        # return( " ".join( normalised_words ) )
        return normalised_words

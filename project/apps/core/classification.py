from nltk.classify import NaiveBayesClassifier
from .models import WikiPage, Search
from .text_processing import TextProcessor

class Classifier (object):

    # Initialiser
    def __init__ ( self, term, wiki_page_ids ):
        self.term = term
        self.wiki_page_ids = wiki_page_ids
        # Starts off as wikipedia articles, extend to include search paragraphs
        self.training_data = []
        # Searches is a list of ids of searches used to improve classifier (initially empty)
        self.searches = []

        # Build the classifier
        self.build_classifier()

    # Builds classifier
    def build_classifier( self ):
        # Get the models from database
        wiki_pages = WikiPage.objects.filter(page_id__in=self.wiki_page_ids)

        for page in wiki_pages:
            extract = TextProcessor.remove_stops_and_lemmatize(page.extract)

            data = Classifier.process_for_classifier(extract, page.page_id)

            self.training_data.append(data)

        # Build classifer for class instance
        self.classifier = NaiveBayesClassifier.train(self.training_data)

    # Adds more data to the classifier
    def extend_classifier( self, text, page_id, search_id ):
        text_formatted = TextProcessor.remove_stops_and_lemmatize(text)

        self.searches.append(search_id)
        self.training_data.append(Classifier.process_for_classifier(text_formatted, page_id))

        self.classifier = NaiveBayesClassifier.train(self.training_data)

    # Returns the id of the wikipedia article
    def classify_text( self, text ):
        text = TextProcessor.remove_stops_and_lemmatize(text)
        words = Classifier.words_to_dict(text)

        return self.classifier.classify(words)

    def get_accuracy( self, test_data ):
        return self.classifier.accuracy(test_data)

    # Takes array of words and adds true
    @classmethod
    def words_to_dict( cls, words ):
        return dict([(word, True) for word in words])

    # Processes an array of words to a classification for addition to naive bayes
    @classmethod
    def process_for_classifier( cls, words, classification ):
        return (cls.words_to_dict(words), classification)

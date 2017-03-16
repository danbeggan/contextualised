from nltk.classify import NaiveBayesClassifier

from .text_processing import TextProcessor

class Classifier (object):

    # Initialiser
    def __init__ ( self, term, wiki_page_ids ):
        self.term = term

        # Array of ids for wikipedia pages model
        self.wiki_page_ids = wiki_page_ids

        self.training_data = []

        # Searches is a list of ids of searches used to improve classifier (initially empty)
        self.searches = []

    # Builds classifier
    def build_classifier( self, wiki_pages ):
        # Get the models from database
        # TODO: fix loop
        wiki_pages = WikiPage.objects.filter(id__in=[self.wiki_page_ids])

        for page in wiki_pages:
            # Dont include disambiguation article in training data
            if "(disambiguation)" not in page.title:
                extract = TextProcessor.remove_stops_and_lemmatize(page.extract)

                # TODO: possibly change to id for the classifier label
                data = Classifier.process_for_classifier(extract, page.title)

            self.training_data.append(data)

        # Use the wiki_pages to build classifer
        self.classifier = NaiveBayesClassifier.train(self.training_data)

    # Adds more data to the classifier
    # TODO: need to format data
    def extend_classifier( self, data ):
        self.training_data = self.training_data + data

    def classify_text( self, text ):
        text = TextProcessor.remove_stops_and_lemmatize(text)
        words = Classifier.words_to_dict(text)

        return self.classifier.classify(words)

    # Takes array of words and adds true
    @classmethod
    def words_to_dict( cls, words ):
        return dict([(word, True) for word in words])

    # Processes an array of words to a classification for addition to naive bayes
    @classmethod
    def process_for_classifier( cls, words, classification ):
        return (cls.words_to_dict(words), classification)

from django.db import models

# class Classifier(models.Model):
#     term = models.CharField(max_length=80)
#     training_data = models.TextField()
#
#     class Meta:
#         verbose_name = "Classifier"
#         verbose_name_plural = "Classifiers"
#
#     def __unicode__(self):
#         return self.term

class WikiPage(models.Model):
    title = models.CharField(max_length=80)
    page_id = models.IntegerField()
    extract = models.TextField()

    # Classifer has multiple wiki pages & vice-versa possible
    # classifier = models.ManyToManyField(Classifier)

    class Meta:
        verbose_name = "WikiPage"
        verbose_name_plural = "WikiPages"

    def __unicode__(self):
        return self.title

class Search(models.Model):
    term = models.CharField(max_length=80)
    paragraph = models.TextField()
    term_lemma = models.CharField(max_length=80) # Will be same as classifier used
    correct_wiki_returned = models.BooleanField(default=False) # Update to true after user feedback

    # Foreign keys
    wikipage = models.ForeignKey(WikiPage)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __unicode__(self):
        return self.term

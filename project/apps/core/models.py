from django.db import models

class WikiPage(models.Model):
    title = models.CharField(max_length=80)
    page_id = models.IntegerField()
    extract = models.TextField()

    class Meta:
        verbose_name = "WikiPage"
        verbose_name_plural = "WikiPages"

    def __unicode__(self):
        return self.title

class Search(models.Model):
    term = models.CharField(max_length=80)
    paragraph = models.TextField()
    term_lemma = models.CharField(max_length=80) # Will be same as classifier used
    correct_wiki_returned = models.NullBooleanField(default=None) # Update to true or false after user feedback, default None

    # Foreign keys
    wikipage = models.ForeignKey(WikiPage)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __unicode__(self):
        return self.term

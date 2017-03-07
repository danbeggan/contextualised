from django.db import models

class Disambiguation(models.Model):
    synset = models.CharField(max_length=40)
    definition = models.TextField()

    class Meta:
        verbose_name = "Disambiguation"
        verbose_name_plural = "Disambiguations"

    def __unicode__(self):
        return self.synset

class WikiPage(models.Model):
    title = models.CharField(max_length=80)
    pageid = models.IntegerField()
    extract = models.TextField()

    class Meta:
        verbose_name = "WikiPage"
        verbose_name_plural = "WikiPages"

    def __unicode__(self):
        return self.title

class Search(models.Model):
    term = models.CharField(max_length=80)
    paragraph = models.TextField()
    term_lemma = models.CharField(max_length=80)


    # Foreign keys
    disambiguation = models.ForeignKey(Disambiguation, null=True)
    wikipage = models.ForeignKey(WikiPage)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __unicode__(self):
        return self.paragraph

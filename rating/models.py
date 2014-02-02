from django.utils.translation import ugettext_lazy as __
from django.db import models
from . import enforce_rating
from common.models import Stamps


class Rating(Stamps, models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(help_text=__('This is the question for users to answer'), max_length=255)
    max_value = models.IntegerField(editable=False)
    weight = models.IntegerField(__('Add a weight this rating has for calculating a players rank. E.g. if everything is equal make them all 1, if something is twice as important 2 and 1, or everything 3 and something that matters little a 1'))
    exclusive_options = models.BooleanField(__('Check if you can only select one option, otherwise someone may select as many as they live'))
    ranksets = models.ManyToManyField('RankSet', related_name="ratings")

    def _calc_max(self):
        self.max_value = sum([ option.value for option in self.options.all() ])

    def save(self, *args, **kwargs):
        self._calc_max()
        super(Rating, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class RatingOption(Stamps, models.Model):
    rating = models.ForeignKey('Rating', related_name='options')
    name = models.CharField(max_length=255)
    value = models.IntegerField()
    ranksets = models.ManyToManyField('RankSet')

    def __unicode__(self):
        return self.name


class PlayerRatingManager(models.Manager):
    
    def create(self, *args, **kwargs):
        enforce_rating(kwargs)
        return super(PlayerRatingManager, self).create(*args, **kwargs)


class PlayerRatingSelection(Stamps, models.Model):
    player = models.ForeignKey('common.Player', related_name="ratings_chosen")
    ranksets = models.ForeignKey('RankSet')
    rating = models.ForeignKey('Rating')
    selection = models.ForeignKey('RatingOption')

    objects = PlayerRatingManager()

    def save(self, *args, **kwargs):
        enforce_rating(self)
        return super(PlayerRatingSelection, self).save(*args, **kwargs)


class PlayerRatingComputed(Stamps, models.Model):
    player = models.ForeignKey('common.Player', related_name="ratings_computed")
    ranksets = models.ForeignKey('RankSet')
    total_rating = models.IntegerField(editable=False)


class Ranking(Stamps, models.Model):
    rank = models.PositiveIntegerField()
    player = models.ForeignKey('common.Player')
    rankset = models.ForeignKey('Rankset')

    class Meta:
        unique_together = ['rank', 'player', 'rankset']

    def __unicode__(self):
        return "%d: %s" % (self.rank, self.player)


class RankSet(Stamps, models.Model):
    name = models.CharField(max_length=255)
    season = models.ForeignKey('common.Season', related_name='ranksets')

    def is_answerable(self):
        return True if self.season in self.answerable_for_seasons.all() else False

    def __unicode__(self):
        return self.name

from django.utils.translation import ugettext_lazy as __
from django.db import models
from common.models import Stamps, DirtyFieldsMixin


def enforce_rating(obj):
    if isinstance(obj, dict):
        if obj['selection'].rating != obj['rating']:
            raise Exception('Selection does not match Rating')
    else:
        if getattr(obj, 'selection').rating != getattr(obj, 'rating'):
            raise Exception('Selection does not match Rating')


class Rating(Stamps, models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(help_text=__('This is the question for users to answer'), max_length=255)
    max_value = models.IntegerField(editable=False, default=0)
    weight = models.IntegerField(help_text=__("""Add a weight this rating has for calculating a players rank.
                                              E.g. if everything is equal make them all 1, if something is
                                              twice as important 2 and 1, or everything 3 and something that
                                              matters little a 1"""))
    exclusive_options = models.BooleanField(help_text=__("""Check if you can only select one option,
                                                         otherwise someone may select as many as they live"""))
    ranksets = models.ManyToManyField('RankSet', related_name="ratings")

    def _calc_max(self):
        operation = max if self.exclusive_options else sum
        self.max_value = operation([option.value for option in self.options.all()])

    def __unicode__(self):
        return self.name


class RatingOption(DirtyFieldsMixin, Stamps, models.Model):
    rating = models.ForeignKey('Rating', related_name='options')
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.is_dirty():
            if 'value' in self.get_dirty_fields().keys():
                self.rating._calc_max()
                self.rating.save()
        return super(RatingOption, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class PlayerRatingManager(models.Manager):

    def create(self, *args, **kwargs):
        enforce_rating(kwargs)
        return super(PlayerRatingManager, self).create(*args, **kwargs)


class PlayerRatingSelection(Stamps, models.Model):
    player = models.ForeignKey('common.Player', related_name="ratings_chosen")
    rankset = models.ForeignKey('RankSet')
    rating = models.ForeignKey('Rating')
    selection = models.ForeignKey('RatingOption')

    objects = PlayerRatingManager()

    def save(self, *args, **kwargs):
        enforce_rating(self)
        return super(PlayerRatingSelection, self).save(*args, **kwargs)


class PlayerRatingComputed(Stamps, models.Model):
    player = models.ForeignKey('common.Player', related_name="ratings_computed")
    rankset = models.ForeignKey('RankSet')
    total_rating = models.DecimalField(editable=False, decimal_places=4, max_digits=10)


class PlayerRanking(Stamps, models.Model):
    rank = models.PositiveIntegerField()
    player = models.ForeignKey('common.Player')
    rankset = models.ForeignKey('RankSet')

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

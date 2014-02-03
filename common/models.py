from django.utils.translation import ugettext_lazy as __
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import formats
from django.db.models.signals import m2m_changed, post_save


# Abstract models

class Stamps(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class DirtyFieldsMixin(object):
    """
    Support to be able to tell which fields have been changed since last save on models
    """
    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        post_save.connect(reset_state, sender=self.__class__,
                          dispatch_uid='%s-DirtyFieldsMixin-sweeper' % self.__class__.__name__)
        reset_state(sender=self.__class__, instance=self)

    def _as_dict(self):
        return dict([(f.name, getattr(self, f.name)) for f in self._meta.local_fields if not f.rel])

    def get_dirty_fields(self):
        new_state = self._as_dict()
        return dict([(key, value) for key, value in self._original_state.iteritems() if value != new_state[key]])

    def is_dirty(self):
        # in order to be dirty we need to have been saved at least once, so we
        # check for a primary key and we need our dirty fields to not be empty
        if not self.pk:
            return True
        return {} != self.get_dirty_fields()


def reset_state(sender, instance, **kwargs):
    """
    Used by above mixin
    """
    instance._original_state = instance._as_dict()


# Shared Managers

class ActiveManager(models.Manager):

    def all(self):
        return super(ActiveManager, self).all().filter(is_active=True)

    def filter(self, **kwargs):
        if 'is_active' not in kwargs:
            kwargs['is_active'] = True
        return super(ActiveManager, self).filter(**kwargs)


class ShownManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(ShownManager, self).get_query_set().filter(is_hidden=False)


# Real Models

class Player(Stamps, AbstractBaseUser):
    ON_FIELD_MALE = 1
    ON_FIELD_FEMALE = 2
    GENDER_CHOICES = (
        (ON_FIELD_MALE, 'Male'),
        (ON_FIELD_FEMALE, 'Female'),
        (ON_FIELD_FEMALE, 'MtF Female'),
        (ON_FIELD_MALE, 'FtM Male'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']
    name = models.CharField(__('Full name'), max_length=64)
    email = models.EmailField()
    gender = models.IntegerField(__('I identify my sex as'), choices=GENDER_CHOICES, blank=True, null=True)
    seasons = models.ManyToManyField('Season', related_name="players", through='PlayerSeasons')

    @property
    def display_name(self):
        return "%s (%s)" % (self.name, self.email)

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.name

    def is_superuser(self):
        return False

    def __unicode__(self):
        return self.display_name

    def is_captain(self, team, season):
        return True if self.season_teams.filter(season=season, team=team, is_captain=True).count() > 0 else False


class PlayerSeasons(Stamps, models.Model):
    """
    Through model for created timestamp, ordering for waitlist
    """
    player = models.ForeignKey('Player')
    season = models.ForeignKey('Season')


class OpenSeasonManager(models.Manager):

    def get_query_set(self):
        return super(OpenSeasonManager, self).get_query_set().filter(is_open=True)


class Season(Stamps, models.Model):
    is_active = models.BooleanField(help_text=__('Is currently being played'), default=False)
    is_open = models.BooleanField(help_text=__('Is open for registration'), default=False)
    is_hidden = models.BooleanField(help_text=__('Hidden from players'), default=False)
    name = models.CharField(__('Name of season'), max_length=64)
    starts_on = models.DateField(help_text=__('Purely informational'), blank=True, null=True)
    ends_on = models.DateField(help_text=__('Purely informational'), blank=True, null=True)
    answerable_rankset = models.ForeignKey('rating.RankSet', blank=None, null=True,
                                           related_name="answerable_for_seasons",
                                           help_text=__('The questions for ranking you want players to answer'))
    following_schedule = models.ForeignKey('schedule.Schedule', blank=None, null=True,
                                           related_name="season_schedule",
                                           help_text=__('The actual schedule teams are going to follow'))
    signup_cap = models.PositiveIntegerField(help_text=__('Everyone after this # is on the waitlist'),
                                             null=True, blank=True)

    objects = ShownManager()
    active = ActiveManager()
    open = OpenSeasonManager()
    verbose = models.Manager()

    def __unicode__(self):
        return "%s (%s-%s)" % (self.name, formats.date_format(self.starts_on), formats.date_format(self.starts_on))


class Team(Stamps, models.Model):
    name = models.CharField(max_length=64)
    is_hidden = models.BooleanField(help_text=__('Hidden from players'), default=False)
    seasons = models.ManyToManyField('Season', related_name="teams")

    objects = ShownManager()
    verbose = models.Manager()

    def __unicode__(self):
        return self.name


class TeamPlayerSeason(Stamps, models.Model):
    team = models.ForeignKey('Team', related_name="season_players")
    player = models.ForeignKey('Player', related_name="season_teams")
    season = models.ForeignKey('Season')
    is_captain = models.BooleanField(default=False)

    class Meta:
        # you can only be a player on a team in a season once
        unique_together = ('team', 'player', 'season')

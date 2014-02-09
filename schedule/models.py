from django.utils.translation import ugettext_lazy as __
from django.db import models
from common.models import Stamps


class Game(Stamps, models.Model):
    STATUS_PENDING = 1
    STATUS_SCHEDULED = 2
    STATUS_CANCELLED = 3
    STATUS_PLAYED = 4
    STATUS_FOREFEIT = 5
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_CANCELLED, 'Canceled'),
        (STATUS_PLAYED, 'Played'),
        (STATUS_FOREFEIT, 'Forefeit')
    )
    schedule = models.ForeignKey('Schedule')
    location = models.ForeignKey('Location', related_name="games", blank=True, null=True)
    time = models.DateTimeField(null=True, blank=True)
    home_team = models.ForeignKey('common.Team', related_name="home_games")
    away_team = models.ForeignKey('common.Team', related_name="away_games")
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)


class GameScheduling(Stamps, models.Model):
    ACTION_CHOICES = (
        (1, 'Proposed'),
        (2, 'Accepted'),
        (3, 'Request To Cancel'),
        (4, 'Agreed to Cancel'),
    )
    game = models.ForeignKey('Game', related_name="scheduling_notes")
    team = models.ForeignKey('common.Team')
    action = models.IntegerField(choices=ACTION_CHOICES)


class GameEntry(Stamps, models.Model):
    SPIRIT_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    game = models.ForeignKey('Game', related_name="entries")
    team = models.ForeignKey('common.Team', related_name="game_entries")
    opponent_spirit = models.IntegerField(choices=SPIRIT_CHOICES)
    our_score = models.IntegerField()
    opponent_score = models.IntegerField()


class Location(models.Model):
    name = models.CharField(max_length=255)


class Schedule(Stamps, models.Model):
    name = models.CharField(max_length=64)
    season = models.ForeignKey('common.Season', related_name="schedules")


class Division(Stamps, models.Model):
    schedule = models.ForeignKey('Schedule', related_name="divisions")
    name = models.CharField(max_length=64)
    teams = models.ManyToManyField('common.Team')
    rank = models.IntegerField(help_text=__('1 being the highest'), default=1)


class SchedulePreference(Stamps, models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()


class SchedulePreferenceOption(Stamps, models.Model):
    preference = models.ForeignKey('SchedulePreference', related_name="options")
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)


class PlayerSchedulePreferenceSeason(Stamps, models.Model):
    player = models.ForeignKey('common.Player', related_name="schedule_preference_selections")
    season = models.ForeignKey('common.Season')
    preference = models.ForeignKey('SchedulePreference', related_name="player_schedule_preferences")
    selection = models.ForeignKey('SchedulePreferenceOption')


class TeamSchedulePreferenceSeason(Stamps, models.Model):
    team = models.ForeignKey('common.Team', related_name="team_schedule_preferences")
    season = models.ForeignKey('common.Season')
    preference = models.ForeignKey('SchedulePreference')
    selection = models.ForeignKey('SchedulePreferenceOption')

    class Meta:
        # a team can only have one schedule time
        unique_together = ['team', 'season', 'preference']

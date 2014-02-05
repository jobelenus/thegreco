from schedule.models import Game, GameScheduling, GameEntry, Schedule, Location, SchedulePreference, \
    PlayerSchedulePreferenceSeason, TeamSchedulePreferenceSeason
__all__ = ['Game', 'GameScheduling', 'GameEntry', 'Schedule', 'Location',
           'SchedulePreference', 'PlayerSchedulePreferenceSeason', 'TeamSchedulePreferenceSeason',
           'create_round_robin']


def create_round_robin(schedule, division):
    pass


def enforce_schedule_preference_for_players(season):
    import common
    for player in common.find_players_in_season(season):
        enforce_schedule_preference(player, season)


def enforce_schedule_preference(player, season):
    import common
    """
    If they didn't answer the question, they can meet any schedule
    """
    for player in common.find_players_in_season(season):
        if player.schedule_preference_selections.all().count() == 0:
            for option in season.schedule_preference.options.all():
                player.schedule_preference_selections.create(selection=option, season=season, preference=season.schedule_preference)

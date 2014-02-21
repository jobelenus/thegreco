from schedule.models import Game, GameScheduling, GameEntry, Schedule, Location, SchedulePreference, \
    PlayerSchedulePreferenceSeason, TeamSchedulePreferenceSeason
__all__ = ['Game', 'GameScheduling', 'GameEntry', 'Schedule', 'Location',
           'SchedulePreference', 'PlayerSchedulePreferenceSeason', 'TeamSchedulePreferenceSeason',
           'create_round_robin', 'enforce_schedule_preference_for_players', 'enforce_schedule_preference',
           'get_teams_in_division', 'get_divisions_in_schedule']


def create_round_robin(schedule):
    for division in get_divisions_in_schedule(schedule):
        teams = list(get_teams_in_division(division))
        num_teams = len(teams)
        row = 0
        while row < num_teams:
            team = teams.pop(0)
            for _team in teams:
                Game.objects.create(home_team=team, away_team=_team, schedule=schedule, status=Game.STATUS_SCHEDULED)
            teams.append(team)
            row += 1


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


def get_teams_in_division(division):
    return division.teams.all()


def get_divisions_in_schedule(schedule):
    divisions = schedule.divisions.all()
    if not divisions.count():
        # if there aren't divisions make one
        import common
        division = schedule.divisions.create(name='Created Automatically')
        for team in common.find_teams_for(schedule.season):
            division.teams.add(team)
        divisions = [division]
    return divisions

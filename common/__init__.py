from common.models import Player, Season, TeamPlayerSeason, Team


# Decorators

class PermissionsException(Exception):
    MSG_CAPTAIN_ADD = 'You must be a captain to add other players to a team'
    MSG_CAPTAIN_REMOVE = 'You must be a captain to remove other players from a team'
    MSG_SEASON = 'You cannot add players to a season at this time'
    MSG_PLAYER_MISSING = 'Player is not active for this season'


def captain_or_self_or_superuser(exception_message):
    def actual_decorator(func):
        def newfn(*args, **kwargs):
            if kwargs['user'].is_superuser or \
               kwargs['user'].is_captain(kwargs['team'], kwargs['season']) or \
               kwargs['user'] == kwargs['player']:
                return func(*args, **kwargs)
            else:
                raise PermissionsException(exception_message)
        return newfn
    return actual_decorator


def enforce_kwargs(func):
    def newfn(*args, **kwargs):
        for k, v in kwargs.iteritems():
            if v is None:
                raise Exception('%s cannot be None' % k)
        func(*args, **kwargs)
    return newfn


def active_player_or_open_season(exception_message):
    def actual_decorator(func):
        def newfn(*args, **kwargs):
            if not kwargs['season'].is_open and \
               kwargs['season'] not in kwargs['player'].seasons.all():
                raise PermissionsException(exception_message)
            elif kwargs['season'].is_active is False and kwargs['season'].is_open is False:
                raise PermissionsException(exception_message)
            return func(*args, **kwargs)
        return newfn
    return actual_decorator


# Business logic

def find_teams_for(season):
    return season.teams.all()


def all_seasons():
    return Season.active.all()


def all_open_seasons():
    return Season.open.all()


def find_players_on(team, season):
    return Player.objects.filter(season_teams__team=team, season_teams__season=season)


def find_captains_on(team, season):
    return Player.objects.filter(season_teams__team=team, season_teams__season=season, season_teams__is_captain=True)


def add_player_to_season(player, season):
    player.seasons.add(season)


@enforce_kwargs
@captain_or_self_or_superuser(PermissionsException.MSG_CAPTAIN_ADD)
@active_player_or_open_season(PermissionsException.MSG_SEASON)
def add_player_to_team(user=None, player=None, team=None, season=None, is_captain=False):
    return TeamPlayerSeason.objects.create(player=player, team=team, season=season, is_captain=is_captain)


@enforce_kwargs
@captain_or_self_or_superuser(PermissionsException.MSG_CAPTAIN_REMOVE)
def remove_player_from_team(user=None, player=None, team=None, season=None):
    try:
        return TeamPlayerSeason.objects.filter(player=player, team=team, season=season).delete()
    except TeamPlayerSeason.DoesNotExist:
        pass


def _create_team_captain(user, team, season):
    add_player_to_team(user=user, player=user, team=team, season=season, is_captain=True)

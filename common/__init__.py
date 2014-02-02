from common.models import Player, Season, TeamPlayerSeason


class PermissionsException(Exception):
    pass


def captain_or_self_or_superuser(exception_message):
    def actual_decorator(func):
        def newfn(*args, **kwargs):
            user = args[0]
            player = args[1]
            team = args[2]
            season = args[3]
            if user.is_superuser or user.is_captain(team, season) or user == player:
                return func(*args, **kwargs)
            else:
                raise PermissionsException(exception_message)
        return newfn
    return actual_decorator


def find_teams_for(season):
    return season.teams.all()


def all_seasons():
    return Season.active.all()


def find_players_on(team, season):
    return Player.objects.filter(season_teams__team=team, season_teams__season=season)


def find_captains_on(team, season):
    return find_players_on(team, season).filter(is_captain=True)


@captain_or_self_or_superuser('You must be a captain to add other players to a team')
def add_player_to_team(user, player, team, season, is_captain=False):
    return TeamPlayerSeason.objects.create(player=player, team=team, season=season, is_captain=is_captain)


@captain_or_self_or_superuser('You must be a captain to remove other players from a team')
def remove_player_from_team(user, player, team, season):
    try:
        return TeamPlayerSeason.objects.delete(player=player, team=team, season=season)
    except TeamPlayerSeason.DoesNotExist:
        pass


def _create_team_captain(user, team, season):
    add_player_to_team(user, user, team, season, is_captain=True)

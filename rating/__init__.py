from collections import defaultdict
import logging
logger = logging.getLogger('rating')


import common
from rating.models import PlayerRatingComputed, PlayerRatingSelection, PlayerRanking, RankSet, Rating
__all__ = ['PlayerRatingComputed', 'PlayerRatingSelection', 'PlayerRanking', 'RankSet', 'Rating',
           'get_ratings_for_set', 'get_rating_for_player', 'get_weight_total_for_set',
           'calculate_rating_for_player', 'get_rating_for_player', 'calculate_all_ratings',
           'rank_players_in', 'get_ranked_players_in', 'MissingException']


class MissingException(Exception):
    MSG_RANKING = 'There is no ranking data to use'


def get_ratings_for_set(rankset):
    return rankset.ratings.all()


def get_weight_total_for_set(rankset):
    return float(sum([rating.weight for rating in get_ratings_for_set(rankset)]))


def calculate_rating_for_player(player, rankset, total_weight=None):
    if total_weight is None:
        total_weight = get_weight_total_for_set(rankset)
    try:
        prc = PlayerRatingComputed.objects.get(player=player, rankset=rankset)
    except PlayerRatingComputed.DoesNotExist:
        prc = PlayerRatingComputed(player=player, rankset=rankset)
    ratings = defaultdict(int)
    weightings = defaultdict(int)
    for record in PlayerRatingSelection.objects.filter(player=player, rankset=rankset):
        ratings[record.rating.id] += record.selection.value
        weightings[record.rating.id] = record.selection.rating.weight
    logger.debug(ratings)
    logger.debug(weightings)
    rating = 0
    for rating_id, value in ratings.iteritems():
        logger.debug('%r * (%r/%r)' % (value, weightings[rating_id], total_weight))
        rating += value * (weightings[rating_id] / total_weight)
    logger.debug(rating)
    prc.total_rating = rating
    prc.save()


def get_rating_for_player(player, rankset):
    try:
        return PlayerRatingComputed.objects.get(rankset=rankset, player=player).total_rating
    except PlayerRatingComputed.DoesNotExist:
        return None


def calculate_all_ratings(rankset):
    import common
    total_weight = get_weight_total_for_set(rankset)
    for player in common.find_players_in_season(rankset.season):
        calculate_rating_for_player(player, rankset, total_weight=total_weight)


def rank_players_in(rankset):
    PlayerRanking.objects.filter(rankset=rankset).delete()  # delete everything
    # TODO: improve this into a bulk insert
    rank = 1
    for prc in PlayerRatingComputed.objects.filter(rankset=rankset).order_by('-total_rating'):
        PlayerRanking.objects.create(player=prc.player, rankset=rankset, rank=rank)
        rank += 1


def get_ranked_players_in(rankset, gender=None):
    kwargs = {'rankset': rankset}
    if gender and (gender == common.Player.ON_FIELD_MALE or gender == common.Player.ON_FIELD_FEMALE):
        kwargs.update({'player__gender__in': gender})
    return PlayerRanking.objects.filter(**kwargs).order_by('rank')


def create_teams_from(rankset, serpentine=True):
    ranked = get_ranked_players_in(rankset)
    if ranked.count() == 0:
        raise MissingException(MissingException.MSG_RANKING)
    pick_order = list(rankset.pick_order.all())
    def add_players(ranked_players):
        if not isinstance(ranked_players, list):
            ranked_players = ranked_players.iterator()  # assuming queryset
        while True:
            for pick in pick_order:
                team = pick.team
                try:
                    ranked_player = next(ranked_players)
                except StopIteration:
                    return
                common.add_player_to_season(ranked_player.player, season=rankset.season)
                common.add_player_to_team(user=ranked_player.player, player=ranked_player.player, team=team, season=rankset.season)
            if serpentine:
                pick_order.reverse()
    male_players = get_ranked_players_in(rankset, gender=common.Player.ON_FIELD_MALE)
    add_players(male_players)
    female_players = get_ranked_players_in(rankset, gender=common.Player.ON_FIELD_FEMALE)
    add_players(female_players)

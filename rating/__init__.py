from collections import defaultdict
import logging
logger = logging.getLogger('rating')


from rating.models import PlayerRatingComputed, PlayerRatingSelection, PlayerRanking, RankSet, Rating
__all__ = ['PlayerRatingComputed', 'PlayerRatingSelection', 'PlayerRanking', 'RankSet', 'Rating',
           'get_ratings_for_set', 'get_rating_for_player', 'get_weight_total_for_set',
           'calculate_rating_for_player', 'get_rating_for_player', 'calculate_all_ratings',
           'rank_players_in', 'get_ranked_players_in']


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


def get_ranked_players_in(rankset):
    return PlayerRanking.objects.filter(rankset=rankset).order_by('rank')

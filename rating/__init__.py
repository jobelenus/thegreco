from rating.models import PlayerRatingComputed, PlayerRatingSelection, PlayerRanking
from collections import defaultdict


def get_ratings_for_set(rankset):
    return rankset.ratings.all()


def get_weight_total_for_set(rankset):
    return sum([rating.weight for rating in get_ratings_for_set(rankset)])


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
        weightings[record.rating.id] = record.selection.ratings.weight
    rating = 0
    for rating_id, value in ratings.iteritems():
        rating += value * (weightings[rating_id]/total_weight)
    prc.total_rating = rating
    prc.save()


def calculate_all_ratings(rankset):
    import common
    total_weight = get_weight_total_for_set(rankset)
    for player in common.find_players_in_season(rankset.season):
        calculate_rating_for_player(player, rankset, total_weight=total_weight)


def rank_players_in(rankset):
    rank = 1
    PlayerRatingComputed.filter(rankset=rankset).delete()  # delete everything
    # TODO: improve this into a bulk insert
    for prc in PlayerRatingComputed.objects.filter(rankset=rankset).order_by('-total_rating'):
        rank = PlayerRanking.objects.create(player=prc.player, rankset=rankset, rank=rank)
        rank += 1

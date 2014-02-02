from .models import PlayerRatingComputed, PlayerRatingSelection


def enforce_rating(obj):
    if type(obj) == type({}):
        if obj['selection'].rating != obj['rating']:
            raise Exception('Selection does not match Rating')
    else:
        if getattr(obj, 'selection').rating != getattr(obj, 'rating'):
            raise Exception('Selection does not match Rating')


def get_ratings_for_set(rankset):
    return rankset.ratings.all()


def get_weight_total_for_set(rankset):
    return sum([ rating.weight for rating in rankset.ratings.all() ])


def calculate_rating_for_player(player, rankset, total_weight=None):
    if total_weight is None:
        total_weight = get_weight_total_for_set(rankset)
    try:
        prc = PlayerRatingComputed.objects.get(player=player, rankset=rankset)
    except PlayerRatingComputed.DoesNotExist:
        prc = PlayerRatingComputed(player=player, rankset=rankset)
    rating = 0
    for record in PlayerRatingSelection.objects.filter(player=player, rankset=rankset):
        rating += record.selection.value * (record.selection.rating.weight/total_weight)
    prc.total_rating = rating
    prc.save()

from rest_framework import viewsets, routers, serializers
import common
from django.core.urlresolvers import reverse


class AdminEditURLMixin(object):

    def get_admin_edit_url(self, instance):
        return reverse('admin:%s_%s_change' %
                       (instance._meta.app_label, instance._meta.module_name),
                       args=[instance.id])


class TeamPlayerSeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = common.TeamPlayerSeason
        fields = ('id', 'team', 'player', 'season', 'created_on', 'modified_on')


class PlayerSerializer(AdminEditURLMixin, serializers.ModelSerializer):
    admin_edit_url = serializers.SerializerMethodField('get_admin_edit_url')
    season_teams = TeamPlayerSeasonSerializer(source='season_teams')

    class Meta:
        model = common.Player
        fields = ('id', 'name', 'email', 'gender', 'seasons', 'created_on', 'modified_on', 'season_teams', 'admin_edit_url')


class TeamSerializer(AdminEditURLMixin, serializers.ModelSerializer):
    admin_edit_url = serializers.SerializerMethodField('get_admin_edit_url')
    season_players = TeamPlayerSeasonSerializer(source='season_players')

    class Meta:
        model = common.Team
        fields = ('id', 'name', 'seasons', 'is_hidden', 'created_on', 'modified_on', 'season_players', 'admin_edit_url')


class TeamDetailSerializer(AdminEditURLMixin, serializers.ModelSerializer):
    admin_edit_url = serializers.SerializerMethodField('get_admin_edit_url')
    seasons_not_in = serializers.SerializerMethodField('get_seasons_not_in')

    def get_seasons_not_in(self, instance):
        seasons_not_in = common.Season.objects.exclude(id__in=instance.seasons.all())
        if seasons_not_in:
            ret = [{'id': s.id, 'name': s.name} for s in seasons_not_in]
            ret.append({'id': 0, 'name': 'Choose...'})
            return ret
        else:
            return []

    class Meta:
        model = common.Team
        fields = ('id', 'name', 'seasons', 'is_hidden', 'created_on', 'modified_on', 'seasons_not_in')


class SeasonSerializer(AdminEditURLMixin, serializers.ModelSerializer):
    admin_edit_url = serializers.SerializerMethodField('get_admin_edit_url')
    teams = TeamSerializer(source='teams')

    class Meta:
        model = common.Season
        fields = ('id', 'name', 'created_on', 'modified_on', 'teams', 'players', 'admin_edit_url')


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = common.Player.objects.all()
    serializer_class = PlayerSerializer
    paginate_by = 7


class TeamViewSet(viewsets.ModelViewSet):
    queryset = common.Team.objects.all()
    serializer_class = TeamSerializer
    paginate_by = 7


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = common.Season.objects.all()
    serializer_class = SeasonSerializer
    paginate_by = 7


class TeamDetailSet(viewsets.ModelViewSet):
    model = common.Team
    serializer_class = TeamDetailSerializer


router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'seasons', SeasonViewSet)

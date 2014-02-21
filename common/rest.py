from rest_framework import viewsets, routers, serializers
import common
from django.core.urlresolvers import reverse


class AdminEditURLMixin(object):

    def get_admin_edit_url(self, instance):
        print 'admin:%s_%s_change % ', instance._meta.app_label, instance._meta.module_name, instance.id
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


class SeasonSerializer(AdminEditURLMixin, serializers.ModelSerializer):
    admin_edit_url = serializers.SerializerMethodField('get_admin_edit_url')
    teams = TeamSerializer(source='teams')

    class Meta:
        model = common.Season
        fields = ('id', 'name', 'created_on', 'modified_on', 'teams', 'players', 'admin_edit_url')


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = common.Player.objects.all()
    serializer_class = PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = common.Team.objects.all()
    serializer_class = TeamSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = common.Season.objects.all()
    serializer_class = SeasonSerializer


router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'seasons', SeasonViewSet)

from rest_framework import generics, viewsets, routers, serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
import common


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
            return [{'id': s.id, 'name': s.name} for s in seasons_not_in]
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


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = common.Player.objects.all()
    serializer_class = PlayerSerializer
    paginate_by = 7


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = common.Team.objects.all()
    serializer_class = TeamSerializer
    paginate_by = 7


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = common.Season.objects.all()
    serializer_class = SeasonSerializer
    paginate_by = 7


class TeamDetail(generics.RetrieveUpdateAPIView):
    model = common.Team
    serializer_class = TeamDetailSerializer

    def update(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        season_id = request.DATA.get('season', None)
        if season_id:
            season = common.Season.objects.get(id=season_id)
            common.add_team_to_season(self.object, season)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'seasons', SeasonViewSet)

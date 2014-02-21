from rest_framework import viewsets, routers, serializers
import common


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = common.Team
        fields = ('id', 'name', 'seasons', 'is_hidden', 'created_on', 'modified_on')


class SeasonSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(source='teams')

    class Meta:
        model = common.Season
        fields = ('id', 'name', 'created_on', 'modified_on', 'teams')


class TeamPlayerSeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = common.TeamPlayerSeason
        fields = ('id', 'team', 'player', 'season', 'created_on', 'modified_on')


class PlayerSerializer(serializers.ModelSerializer):
    season_teams = TeamPlayerSeasonSerializer(source='season_teams')

    class Meta:
        model = common.Player
        fields = ('id', 'name', 'email', 'gender', 'seasons', 'created_on', 'modified_on', 'season_teams')
 

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

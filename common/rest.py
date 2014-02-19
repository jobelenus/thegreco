from rest_framework import viewsets, routers, serializers
import common


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = common.Season
        fields = ('id', 'name', 'created_on', 'modified_on')


class PlayerViewSet(viewsets.ModelViewSet):
    model = common.Player


class TeamViewSet(viewsets.ModelViewSet):
    model = common.Team


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = common.Season.objects.all()
    serializer_class = SeasonSerializer


router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'seasons', SeasonViewSet)

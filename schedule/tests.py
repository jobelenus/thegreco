from django.test import TestCase
import schedule
import common


class TestSchedule(TestCase):
    fixtures = ['test', 'make_teams']

    def setUp(self):
        self.schedule = schedule.Schedule.objects.get(id=1)
        self.team1 = common.Team.objects.get(id=2)
        self.team2 = common.Team.objects.get(id=3)
        self.team3 = common.Team.objects.get(id=4)

    def tearDown(self):
        pass

    def test_create_round_robin(self):
        schedule.create_round_robin(self.schedule)
        self.assertEquals(6, schedule.Game.objects.all().count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team1, away_team=self.team2).count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team1, away_team=self.team3).count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team2, away_team=self.team1).count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team2, away_team=self.team3).count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team3, away_team=self.team1).count())
        self.assertEquals(1, schedule.Game.objects.filter(home_team=self.team3, away_team=self.team2).count())

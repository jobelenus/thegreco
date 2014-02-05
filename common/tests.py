from django.test import TestCase
import common


class TestCommon(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.season_old = common.Season.objects.get(id=1)
        self.season_open = common.Season.objects.get(id=2)
        self.season_active = common.Season.objects.get(id=3)
        self.season_womens = common.Season.objects.get(id=4)
        self.player1 = common.Player.objects.get(id=1)
        self.player2 = common.Player.objects.get(id=2)
        self.player3 = common.Player.objects.get(id=3)
        self.no_season_player = common.Player.objects.get(id=4)
        self.team = common.Team.objects.get(id=1)

    def tearDown(self):
        pass

    def test_find_teams_for(self):
        self.assertEquals(self.team, common.find_teams_for(self.season_old)[0])
        self.assertEquals(self.team, common.find_teams_for(self.season_open)[0])

    def test_all_seasons(self):
        self.assertEquals(self.season_active, common.all_seasons()[0])

    def test_all_open_seasons(self):
        self.assertEquals(self.season_open, common.all_open_seasons()[0])

    def test_find_players_on(self):
        self.assertEquals(self.player3, common.find_players_on(self.team, self.season_old)[0])
        self.assertEquals(0, len(common.find_players_on(self.team, self.season_active)))

    def test_find_captains_on(self):
        self.assertEquals(self.player3, common.find_captains_on(self.team, self.season_old)[0])
        self.assertEquals(0, len(common.find_captains_on(self.team, self.season_active)))

    def test_team_add_remove(self):
        common.add_player_to_team(user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, common.TeamPlayerSeason.objects.filter(player=self.player1, season=self.season_open, team=self.team).count())
        common.add_player_to_team(user=self.player2, player=self.player2, season=self.season_open, team=self.team, is_captain=True)
        self.assertTrue(self.player2.is_captain(self.team, self.season_open))
        self.assertEqual(2, len(common.find_players_on(self.team, self.season_open)))
        common.remove_player_from_team(user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, len(common.find_players_on(self.team, self.season_open)))
        common.add_player_to_team(user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(2, len(common.find_players_on(self.team, self.season_open)))
        common.remove_player_from_team(user=self.player2, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, len(common.find_players_on(self.team, self.season_open)))

    def test_gender_rules(self):
        self.assertRaisesMessage(common.PermissionsException, common.PermissionsException.MSG_ELIGIBLE,
                                 common.add_player_to_season, player=self.player1, season=self.season_womens)
        common.add_player_to_season(player=self.player2, season=self.season_womens)

    def test_duplicate_player(self):
        # cannot add a player to a team twice
        common.add_player_to_team(user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, common.TeamPlayerSeason.objects.filter(player=self.player1, season=self.season_open, team=self.team).count())
        self.assertRaisesMessage(common.PermissionsException, common.PermissionsException.MSG_EXISTING,
                                 common.add_player_to_team, user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, common.TeamPlayerSeason.objects.filter(player=self.player1, season=self.season_open, team=self.team).count())

    def test_team_perm(self):
        # cannot add to a team that isn't open or active
        self.assertRaisesMessage(common.PermissionsException, common.PermissionsException.MSG_SEASON,
                                 common.add_player_to_team, user=self.player1, player=self.player1, season=self.season_old, team=self.team)

    def test_remove_player(self):
        self.assertFalse(self.player1.is_superuser())
        self.assertFalse(self.player1.is_captain(self.team, self.season_open))
        common.add_player_to_team(user=self.player1, player=self.player1, season=self.season_open, team=self.team)
        common.add_player_to_team(user=self.player2, player=self.player2, season=self.season_open, team=self.team, is_captain=True)
        # cannot remove another if you are not a captain
        self.assertRaisesMessage(common.PermissionsException, common.PermissionsException.MSG_CAPTAIN_REMOVE,
                                 common.remove_player_from_team, user=self.player1, player=self.player2, season=self.season_open, team=self.team)
        self.assertEqual(2, len(common.find_players_on(self.team, self.season_open)))
        common.remove_player_from_team(user=self.player2, player=self.player1, season=self.season_open, team=self.team)
        self.assertEqual(1, len(common.find_players_on(self.team, self.season_open)))

    def test_player_season_perm(self):
        # cannot add player to a team when they aren't in this season
        common.add_player_to_team(user=self.player2, player=self.player2, season=self.season_open, team=self.team, is_captain=True)
        self.assertRaisesMessage(common.PermissionsException, common.PermissionsException.MSG_SEASON,
                                 common.add_player_to_team, user=self.player2, player=self.no_season_player, season=self.season_open, team=self.team)

    def test_baggage(self):
        pass

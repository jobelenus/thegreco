from django.test import TestCase
import common
import rating
import schedule
import decimal


class TestRating(TestCase):
    fixtures = ['test', 'make_teams']

    def setUp(self):
        self.rankset_empty = rating.RankSet.objects.get(id=1)
        self.rankset_calcd = rating.RankSet.objects.get(id=2)
        self.rankset_teams = rating.RankSet.objects.get(id=3)
        self.rating1 = rating.Rating.objects.get(id=1)
        self.rating2 = rating.Rating.objects.get(id=2)
        self.rating1._calc_max()
        self.rating2._calc_max()
        self.player1 = common.Player.objects.get(id=1)
        self.player2 = common.Player.objects.get(id=2)
        self.preference = schedule.SchedulePreference.objects.get(id=1)

    def tearDown(self):
        pass

    def test_calc_max(self):
        self.assertEquals(3, self.rating1.max_value)
        self.assertEquals(6, self.rating2.max_value)

    def test_get_weight_total_for_set(self):
        self.assertEqual(decimal.Decimal('2.0'), rating.get_weight_total_for_set(self.rankset_empty))

    def test_calculate_rating_for_player(self):
        # testing different kind of options
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating1, selection=self.rating1.options.get(value=1))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=1))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=2))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=3))
        rating.calculate_rating_for_player(self.player1, self.rankset_empty)
        player_rating = rating.get_rating_for_player(self.player1, self.rankset_empty)
        self.assertEqual(decimal.Decimal('3.5'), player_rating)

    def test_calculate_rating_for_player_no_answers(self):
        # make sure it runs with no answers
        rating.PlayerRatingSelection.objects.filter(player=self.player1, rankset=self.rankset_empty).delete()
        rating.calculate_rating_for_player(self.player1, self.rankset_empty)
        player_rating = rating.get_rating_for_player(self.player1, self.rankset_empty)
        self.assertEqual(0, player_rating)

    def test_calculate_rating_for_player_missing_answers(self):
        # make sure it runs with not all questions answered
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating1, selection=self.rating1.options.get(value=3))
        rating.calculate_rating_for_player(self.player1, self.rankset_empty)
        player_rating = rating.get_rating_for_player(self.player1, self.rankset_empty)
        self.assertEqual(decimal.Decimal('1.5'), player_rating)
        rating.PlayerRatingSelection.objects.filter(player=self.player1, rankset=self.rankset_empty).delete()

    def test_calculate_rating_for_player_weights(self):
        # test non-equal weights
        self.rating1.weight = 1
        self.rating1.save()
        self.rating2.weight = 2
        self.rating2.save()
        self.assertEqual(decimal.Decimal('3.0'), rating.get_weight_total_for_set(self.rankset_empty))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating1, selection=self.rating1.options.get(value=1))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=1))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=2))
        rating.PlayerRatingSelection.objects.create(player=self.player1, rankset=self.rankset_empty,
                                                    rating=self.rating2, selection=self.rating2.options.get(value=3))
        rating.calculate_rating_for_player(self.player1, self.rankset_empty)
        player_rating = rating.get_rating_for_player(self.player1, self.rankset_empty)
        self.assertEqual(decimal.Decimal('4.3333'), player_rating)
        # set the weights back
        self.rating1.weight = 1
        self.rating1.save()
        self.rating2.weight = 1
        self.rating2.save()
        self.assertEqual(decimal.Decimal('2.0'), rating.get_weight_total_for_set(self.rankset_empty))

    def test_rank_players_in(self):
        rating.rank_players_in(self.rankset_calcd)
        ranked_players = rating.get_ranked_players_in(self.rankset_calcd)
        self.assertEquals(1, ranked_players[0].rank)
        self.assertEquals(self.player1, ranked_players[0].player)
        self.assertEquals(2, ranked_players[1].rank)
        self.assertEquals(self.player2, ranked_players[1].player)

    def test_create_teams_from_standard(self):
        expected_ranks = {
            # team pick: [player ranks]
            1: set([1, 4, 12, 5, 8]),  # pay attention to the male/female split
            2: set([2, 10, 13, 6, 9]),
            3: set([3, 11, 14, 7]),
        }
        self._test_create_teams_from(expected_ranks, False)

    def test_create_teams_from_serp(self):
        expected_ranks = {
            # team pick: [player ranks]
            1: set([1, 11, 12, 7, 8]),  # pay attention to the male/female split
            2: set([2, 10, 13, 6, 9]),
            3: set([3, 4, 14, 5, ]),
        }
        self._test_create_teams_from(expected_ranks, True)

    def _test_create_teams_from(self, expected_ranks, serpentine):
        rating.create_teams_from(self.rankset_teams, serpentine=serpentine)
        pick_order = self.rankset_teams.pick_order.all()
        for pick in pick_order:
            team = pick.team
            real_ranks = []
            players = common.find_players_on(team, self.rankset_teams.season)
            for player in players:
                player_rank = rating.PlayerRanking.objects.get(rankset=self.rankset_teams, player=player)
                real_ranks.append(player_rank.rank)
            #print set(real_ranks), expected_ranks[pick.rank]
            self.assertEqual(set(real_ranks), expected_ranks[pick.rank])

    def test_create_schedule_pref_teams_serp(self):
        # apply the preference to the season, rest of the data is already in place
        self.rankset_teams.season.schedule_preference = self.preference
        self.rankset_teams.season.save()
        # player 18f, 14f, 9m, 8m, 6m are pref2
        # that is rank: 9, 5, 10, 4, 2
        # team 3 is pref2
        expected_ranks = {
            # team pick: [player ranks]
            1: set([1, 12, 13, 7, 8]),  # pay attention to the male/female split
            2: set([3, 11, 14, 6]),
            3: set([2, 4, 10, 5, 9]),
        }
        self._test_create_teams_from(expected_ranks, True)

    def test_create_schedule_pref_teams_standard(self):
        # apply the preference to the season, rest of the data is already in place
        self.rankset_teams.season.schedule_preference = self.preference
        self.rankset_teams.season.save()
        # player 18f, 14f, 9m, 8m, 6m are pref2
        # that is rank: 9, 5, 10, 4, 2
        # team 3 is pref2
        expected_ranks = {
            # team pick: [player ranks]
            1: set([1, 11, 13, 6, 8]),  # pay attention to the male/female split
            2: set([3, 12, 14, 7]),
            3: set([2, 4, 10, 5, 9]),
        }
        self._test_create_teams_from(expected_ranks, False)

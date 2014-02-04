from django.test import TestCase
import common
import rating
import decimal


class TestCommon(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.rankset_empty = rating.RankSet.objects.get(id=1)
        self.rankset_calcd = rating.RankSet.objects.get(id=2)
        self.rating1 = rating.Rating.objects.get(id=1)
        self.rating2 = rating.Rating.objects.get(id=2)
        self.rating1._calc_max()
        self.rating2._calc_max()
        self.player1 = common.Player.objects.get(id=1)
        self.player2 = common.Player.objects.get(id=2)

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

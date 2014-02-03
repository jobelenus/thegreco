from django.test import TestCase
import rating

class TestCommon(TestCase):
    fixtures = ['test']

    def setUp(self):
        self.rankset_empty = rating.RankSet.objects.get(id=1)
        self.rankset_calcd = rating.RankSet.objects.get(id=2)
        self.rating1 = rating.Rating.objects.get(id=1)
        self.rating2 = rating.Rating.objects.get(id=2)
        self.rating1._calc_max()
        self.rating2._calc_max()

    def tearDown(self):
        pass

    def test_calc_max(self):
        self.assertEquals(3, self.rating1.max_value)
        self.assertEquals(6, self.rating2.max_value)

    def test_get_weight_total_for_set(self):
        self.assertEqual(2, rating.get_weight_total_for_set(self.rankset_empty))

    def test_calculate_rating_for_player(self):
        pass

    def test_rank_players_in(self):
        pass

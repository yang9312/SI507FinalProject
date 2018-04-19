import unittest
import data.data_processing as dp
import data.plot as p
import data.product_info as pi
import json


class TestData(unittest.TestCase):
    def test_product(self):
        fil = open("category_info.json", "r").read()
        fil_dic = json.loads(fil)
        p1 = pi.get_product_data("Skincare", fil_dic["Skincare"])
        self.assertEqual(p1[0]["PrimaryName"], "Advanced Night Repair")
        self.assertEqual(p1[0]["StarRating"], "97%")
        self.assertEqual(p1[0]["SubName"], "Synchronized Recovery Complex II")

    def test_select(self):
        s = pi.select_unique_product()
        self.assertEqual(s[0]["PrimaryName"], "Advanced Night Repair")
        self.assertEqual(s[0]["StarRating"], "97%")
        self.assertEqual(s[0]["SubName"], "Synchronized Recovery Complex II")
        self.assertEqual(s[0]["ProductId"], "26959")
        self.assertEqual(len(s), 302)

    def test_review(self):
        r = pi.get_review_data()
        self.assertEqual(len(r), 15772)
        self.assertEqual(len(r[0]), 6)
        self.assertEqual(r[0]["UserNickname"], "Jianglili1794")
        self.assertEqual(r[0]["Skintype"], "Dry")
        self.assertEqual(r[0]["Rating"], 5)
        self.assertEqual(r[0]["ProductId"], "26959")
        self.assertEqual(r[0]["Age"], "25to34")


class TestDataProcessing(unittest.TestCase):
    def test_TypeRating(self):
        tr1 = dp.TypeRating(suptype="Makeup", target_type="Foundation", rating=16, review_count=20)
        self.assertEqual(tr1.__str__(), "Foundation | 4.0 | 20")
        tr2 = dp.TypeRating(suptype="Makeup", target_type="Foundation", rating=0, review_count=0)
        self.assertEqual(tr2.__str__(), "Foundation | 0 | 0")
        tr3 = dp.TypeRating(suptype="Makeup", target_type="Foundation", rating=0, review_count="Unknown")
        self.assertEqual(tr3.__str__(), "Foundation | NA | Unknown")
        tr4 = dp.TypeRating(suptype="Makeup", target_type="Foundation", rating="a", review_count=3)
        self.assertEqual(tr4.__str__(), "Foundation | NA | 3")

    def test_Customer(self):
        tr1 = dp.Customer(product=None, age=None, skintype=None, using_year=None, rating=None)
        self.assertEqual(tr1.__str__(), "None | None | None | None | None")
        tr2 = dp.Customer(product=26959, age=20, skintype="Dry", using_year="1year", rating=3)
        self.assertEqual(tr2.__str__(), "20 | 20 <= age < 30 | Dry | 1year | 3")
        tr3 = dp.Customer(product=None, age="Unknown", skintype="Dry", using_year="1year", rating=3)
        self.assertEqual(tr3.__str__(), "Unknown | Unknown | Dry | 1year | 3")

    def test_bar_data(self):
        r1 = dp.process_bar_data("esteelauder.db", sup=None)
        self.assertEqual(r1[0].target_type, "Skincare")
        self.assertEqual(r1[1].calculate_average_rating(), 4.62)
        self.assertEqual(r1[2].reviewcount, 4032)
        r2 = dp.process_bar_data("esteelauder.db", sup="makeup")
        self.assertEqual(r2[0].target_type, "Foundation")
        self.assertEqual(r2[1].calculate_average_rating(), 4.66)
        self.assertEqual(r2[2].reviewcount, 378)

    def test_pie_data(self):
        r1 = dp.process_pie_data("esteelauder.db", product= 26959)
        self.assertEqual(r1[0].avg_age(), 29.5)
        self.assertEqual(r1[0].age_group(), "20 <= age < 30")
        self.assertEqual(r1[0].SkinType, "Dry")
        self.assertEqual(r1[0].UsingYear, "1-2years")

class TestPlot(unittest.TestCase):
    def test_bar_plot(self):
        try:
            p.bar_plot("esteelauder.db")
            p.bar_plot("esteelauder.db", sup=None)
            p.bar_plot("esteelauder.db", sup=None, content="Rating")
            p.bar_plot("esteelauder.db", sup=None, content="review")
            p.bar_plot("esteelauder.db", sup=None, content="a")
            p.bar_plot("esteelauder.db", sup="Skincare", content="review")
            p.bar_plot("esteelauder.db", sup="Makeup", content="review")
            p.bar_plot("esteelauder.db", sup="Fragrance", content="review")
            p.bar_plot("esteelauder.db", sup="b", content="a")
        except:
            self.fail()

    def test_pie_plot(self):
        try:
            p.pie_plot("esteelauder.db")
            p.pie_plot("esteelauder.db", product=None, content=None)
            p.pie_plot("esteelauder.db", product=26959, content=None)
            p.pie_plot("esteelauder.db", product=26959, content="Skintype")
            p.pie_plot("esteelauder.db", product=43034, content="Age")
            p.pie_plot("esteelauder.db", product=43034, content="a")
            p.pie_plot("esteelauder.db", product=4, content="Age")
            p.pie_plot("esteelauder.db", product="a", content="Age")
        except:
            self.fail()


if __name__ == '__main__':
    unittest.main()

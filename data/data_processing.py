import sqlite3
from settings import *


class TypeRating():
    def __init__(self, suptype, target_type, rating, review_count):
        self.suptype = suptype
        self.target_type = target_type
        self.rating = rating
        self.reviewcount = review_count

    def calculate_average_rating(self):
        try:
            average_rating = round(self.rating / self.reviewcount * 5, 2) if self.reviewcount != 0 else 0
        except:
            average_rating = "NA"
        return average_rating

    def __str__(self):
        statement = "{} | {} | {}".format(self.target_type, self.calculate_average_rating(), self.reviewcount)
        return statement


class Customer():
    def __init__(self, product=None, age=None, skintype=None, using_year=None, rating=None):
        self.product = product
        self.Age = age
        self.SkinType = skintype
        self.UsingYear = using_year
        self.Rating = rating

    def avg_age(self):
        if self.Age is None:
            return
        self.Age = str(self.Age)
        if "to" in self.Age:
            average_age_lis = self.Age.split("to")
            average_age = (int(average_age_lis[0]) + int(average_age_lis[1])) / 2
        elif "Over" in self.Age:
            average_age = int(self.Age[4:])
        else:
            average_age = self.Age
        return average_age

    def age_group(self):
        avg_age = self.avg_age()
        if avg_age is None:
            return
        age_group = {20: "age < 20", 30: "20 <= age < 30", 40: "30 <= age < 40",
                     50: "40 <= age < 50"}
        sorted_age_group = sorted(age_group.items())
        if avg_age == "Unknown":
            age_category = "Unknown"
            return age_category
        elif float(avg_age) >= 50:
            age_category = "age >= 50"
            return age_category
        else:
            for i in sorted_age_group:
                if i[0] > float(avg_age):
                    age_category = i[1]
                    return age_category

    def __str__(self):
        return "{} | {} | {} | {} | {}".format(self.avg_age(), self.age_group(),
                                               self.SkinType, self.UsingYear, self.Rating)


DBNAME = base_dir + "/data/esteelauder.db"


def process_bar_data(db_name, sup=None):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if sup is not None:
        sup = "Skincare" if sup.lower() == "skincare" else sup
        sup = "Makeup" if sup.lower() == "makeup" else sup
        sup = "Fragrance" if sup.lower() == "fragrance" else sup

    if sup is None:
        query = '''SELECT c.Name, SUM(p.StarRating * p.ReviewCount), SUM(p.ReviewCount)
                   FROM Product AS p
                   JOIN Type AS c
                   ON c.Id = p.SuptypeId
                   GROUP BY p.SuptypeId      
                '''
        cur.execute(query)
        res = cur.fetchall()
    elif sup in ["Skincare", "Makeup", "Fragrance"]:
        query = '''SELECT c.Name, SUM(p.StarRating * p.ReviewCount), SUM(p.ReviewCount)
                   FROM Product AS p
                   JOIN Category AS c
                   ON c.Id = p.SubtypeId
                   WHERE p.SuptypeId = (SELECT t.Id FROM Type AS t
                                        JOIN Product AS pt
                                        ON pt.SuptypeId = t.Id
                                        WHERE t.Name = ?
                    )
                   GROUP BY p.SubtypeId     
                '''
        cur.execute(query, (sup, ))
        res = cur.fetchall()
    else:
        return

    result = []
    for i in res:
        result.append(TypeRating(sup, i[0], i[1], i[2]))
    conn.close()
    return result


def process_pie_data(db_name, product=None):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    if product is None:
        return
    else:
        query = '''SELECT r.Age, r.SkinType, r.UsingYear, r.Rating
                   FROM Review AS r
                   WHERE r.ProductID = (SELECT p.Id
                                        FROM Product AS p
                                        WHERE p.ProductId = ?          
                                        )
                '''
        cur.execute(query, (product, ))
        res = cur.fetchall()

        if res is None:
            return

    result = []
    for i in res:
        result.append(Customer(product, i[0], i[1], i[2], i[3]))
    conn.close()
    return result


def process_scatter_data(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    query = '''SELECT StarRating, ReviewCount
               FROM Product
            '''

    cur.execute(query)
    res = cur.fetchall()
    conn.close()
    return res


def process_table_data(db_name, suptype):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    query = '''SELECT p.ProductId, p.PrimaryName, p.SubName, c.Name, p.StarRating, p.ReviewCount 
               FROM Product AS p
               JOIN Category AS c
               ON c.Id = p.SubtypeId
               WHERE p.SuptypeId = (SELECT t.Id
                                    FROM Type AS t
                                    WHERE t.Name = ?         
                                    )
            '''
    cur.execute(query, (suptype, ))
    res = cur.fetchall()

    result = []
    for i in res:
        i_dic = dict(ProductId=i[0], PrimaryName=i[1], SubName=i[2], SubType=i[3], StarRating=i[4], ReviewCount=i[5])
        result.append(i_dic)
    return result


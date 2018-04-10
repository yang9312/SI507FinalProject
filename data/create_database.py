import sqlite3
import csv
import json
import product_info as p_fil

# create a database
DBNAME = 'esteelauder.db'


def init_db(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    table_lis = ['Type', 'Category', 'Product', 'Review']
    for t in table_lis:
        statement = "DROP TABLE IF EXISTS '{}'".format(t)
        cur.execute(statement)
        conn.commit()

    statement = '''CREATE TABLE 'Type' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT
        );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''CREATE TABLE 'Category' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT,
        'Suptype' INTEGER
        );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''CREATE TABLE 'Product' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'ProductId' INTEGER,
        'PrimaryName' TEXT,
        'SubName' TEXT,
        'StarRating' REAL,
        'ReviewCount' INTEGER,
        'SuptypeId' INTEGER,
        'SubtypeId' INTEGER
        );
        '''
    cur.execute(statement)
    conn.commit()

    statement = '''CREATE TABLE 'Review' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'NickName' TEXT,
        'SkinType' TEXT,
        'Age' TEXT,
        'UsingYear' TEXT,
        'Rating' TEXT,
        'ProductID' INTEGER
        );
        '''
    cur.execute(statement)
    conn.commit()

    conn.close()


def insert_item(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    suptype_lis = ["Skincare", "Makeup", "Fragrance"]
    for suptype in suptype_lis:
        insertion = (None, suptype)
        statement = "INSERT INTO 'Type' VALUES (?, ?)"
        cur.execute(statement, insertion)
        conn.commit()

    with open("category_info.json", "r") as category_fil:
        category_dic = json.loads(category_fil.read())
    for suptype in category_dic:
        for category in category_dic[suptype]:
            for subtype in category_dic[suptype][category]:
                statement = '''INSERT INTO 'Category'
                               VALUES (?, ?, ?)
                            '''
                cur.execute(statement, (None, subtype["SubtypeName"], suptype))
                conn.commit()

    product_lis = p_fil.select_unique_product()
    for p in product_lis:
        insertion = (None, int(p["ProductId"]), p["PrimaryName"], p["SubName"],
                     int(p["StarRating"][:-1])/100, int(p["ReviewCount"]), p["SupType"], p["SubType"])
        statement = '''INSERT INTO 'Product'
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    '''
        cur.execute(statement, insertion)
        conn.commit()

    with open("review_cache.json", "r") as review_fil:
        review_dic = json.loads(review_fil.read())
    for product_id in review_dic:
        for r in review_dic[product_id]:
            insertion = (None, r["UserNickname"], r["Skintype"], r["Age"],
                         r["UsingYear"], int(r["Rating"]), int(r["ProductId"]))
            statement = '''INSERT INTO 'Review'
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                        '''
            cur.execute(statement, insertion)
            conn.commit()

    conn.close()


def update_table(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''UPDATE Category
                   SET Suptype = (
                       SELECT Id FROM Type
                       WHERE Type.Name = Category.Suptype
                   )
                 '''
    cur.execute(statement)
    conn.commit()

    statement = '''UPDATE Product
                   SET SuptypeId = (
                           SELECT Id FROM Type
                           WHERE Type.Name = Product.SuptypeId
                           ),
                       SubtypeId = (
                           SELECT Id From Category
                           WHERE Category.Name = Product.SubtypeId
                           )           
                 '''
    cur.execute(statement)
    conn.commit()

    statement = '''UPDATE Review
                   SET ProductId = (
                       SELECT Id FROM Product
                       WHERE Product.ProductId = Review.ProductId
                   )
                 '''
    cur.execute(statement)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    init_db(DBNAME)
    insert_item(DBNAME)
    update_table(DBNAME)

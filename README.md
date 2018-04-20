# SI507FinalProject - Yang Yang

The program is designed to show the average ratings for different cosmetic catalogs and analyze the relationship of different kinds of customers and products provided by Estee Lauder USA website.
<br>

# Data Source


## Estee Lauder: https://www.esteelauder.com

**Challenge Score:** 8

- crawling and scraping multiple pages (haven’t used before)

**Detail:**
- Products (302) provided by the site belongs to three catalogs: skincare, makeup and fragrance.
- Each catalog has at least 10 sub catalogs (face, eye, lip …).
- Parsing the page of each sub catalog to get the basic information about products (name, rating and review counts).
- Detail information about reviews (customer name, age, skin type and using year) is obtained through the page of each product.

**Local Path:** SI507FinalProject/data
- category_info.json: url for each sub catalog
- Skincare_cache.json: cache file for all skincare products basic information
- Makeup_cache.json: cache file for all makeup products basic information
- Fragrance_cache.json: cache file for all fragrance products basic information
- review_cache.json: cache file for reviews of all products

**Access Instruction:** For project user, nothing is required to do.


## Local Database ##

**Local Path:** SI507FinalProject/data/esteelauder.sqlite

**Table:** 4 tables

***Type***
- 3 rows
- 2 columns: Id (primary key), Name

***Category***
- 76 rows
- 3 columns: Id (primary key), Name, SuptypeId (foreign key)

***Product***
- 302 rows
- 8 columns: Id (primary key), ProductId, PrimaryName, SubName, StarRating, ReviewCount, SuptypeId (foreign key), SubtypeId (foreign key)

***Review***
- 15772 rows
- 7 columns: Id (primary key), NickName, SkinType. Age, UsingYear, Rating, ProductID (foreign key)

<br>


# Required Setup

## Virtual Environment

All that required to run the program is listed in requirements.txt.

## Plot.ly

Plotly API is required for running the program.

- Create an account at https://plot.ly/ and generate API Keys.

- Write one code and run:
    ```{python}
    set_credentials_file(username=<YOUR USERNAME>, api_key=<YOUR API KEY>)
    ```
<br>


# Program Structure

## Files Structure

- **SI507FinalProject**
	- **data**
		- **category_info.py** (get sub category url)
		- **product_info.py** (get product data)
		- **review_info.py** (get review data)
		- **create_database.py** (create database)
		- **data_processing.py** (process data from database)
		- **plot.py** (generate different plots)
		- **test.py** (unittest)
		- **esteelauder.db** (database)
		- **product.csv** (all products)
		- **category_info.json**
		- **Skincare_cache.json**
		- **Makeup_cache.json**
		- **Fragrance_cache.json**
		- **review_cache.json**
	- **static**
		- **esteelauder_picture.jpg**
		- **index.css** (style for index page)
		- **table.css** (style for table page)
		- **plot.css** (style for plot page)
		
	- **templates**
		- **index.html**
		- **table.html**
		- **plot.html**	
	- **settings.py**
	- **.gitignore**
	- **README.md**
	- **requirements.txt** (required modules)
	- **app.py** (running file)
	

## Important Functions

**select_unique_product():** SI507FinalProject/data/product_info.py

>**Description:** The same product can be categorized to different sub types because of different division method. Thus, product information may be duplicate. This function select unique product from all products.

**pie_plot():** SI507FinalProject/data/plot.py

>**Description:** This function can draw pie plots through changing parameters.

## Important Classes

**class TypeRating:** SI507FinalProject/data/data_processing.py

>**Description:** The class modifies formats of selecting product information from database. Function calculate_average_rating() is defined for calculating the average rating of chosen categories.

**class Customer:** SI507FinalProject/data/data_processing.py

>**Description:** The class modifies of selecting review information from database. Functions are defined to deal with Age and make data appropriate for plot.py.

## Online Sources

**Framework:** Flask

**Online JS Sources:** Jquery, Plotly, DataTables

**Online CSS Sources:** BootStrap, DataTables
<br>


# User Guide

## Running

- Get all files

``> git clone https://github.com/yang9312/SI507FinalProject.git`` 

``> cd SI507FinalProject``

- Create a virtual environment

``> virtualenv venv``

``> source venv/bin/activate``

- Install all required modules

 ``> pip3 install -r requirements.txt``

- Create one python file

``> touch plotly.py``
``> open plotly.py``

- Write codes

    ```{python}
    import plotly
    set_credentials_file(username=<YOUR USERNAME>, api_key=<YOUR API KEY>)
    ```
- Run
``> python3 plotly.py``

- Run the program

``> python app.py``

- Copy and paste the url on your browser

  <br>
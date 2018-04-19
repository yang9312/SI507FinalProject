from flask import Flask, render_template, request
from data.data_processing import *
from data.plot import *
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/table/")
def table():
    return render_template('table.html')


@app.route("/table/data/", methods=['GET'])
def table_data():
    suptype = request.args.get('suptype')
    return json.dumps(process_table_data(DBNAME, suptype=suptype))


@app.route("/plot/", methods=['POST', 'GET'])
def plot():
    div = '<div></div>'
    if request.method == 'POST':
        plot_type = request.form['plot-type']
        if plot_type == 'bar':
            suptype = request.form['suptype']
            content = request.form['content']
            suptype = suptype if suptype != 'None' else None
            div = bar_plot(DBNAME, sup=suptype, content=content)
        elif plot_type == 'pie':
            product_id = request.form["product_id"]
            content = request.form["content"]
            div = pie_plot(DBNAME, product=product_id, content=content)
        elif plot_type == 'scatter':
            div = scatter_plot(DBNAME)

    return render_template('plot.html', div=div)


if __name__ == '__main__':
    app.run()

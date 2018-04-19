import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot as off_plot
import data.data_processing as d
from settings import base_dir


DBNAME = base_dir + "/data/esteelauder.db"


def bar_plot(db_name, sup=None, content="rating"):
    data_lis = d.process_bar_data(db_name, sup)
    if data_lis is None:
        return
    x_lis = []
    y_lis = []
    text_lis = []
    base_lis = []
    for i in data_lis:
        x_lis.append(i.target_type)
        if content.lower() == "review":
            y_lis.append(i.reviewcount)
            text_lis.append(str(i.calculate_average_rating()) + " ratings")
        else:
            y_lis.append(i.calculate_average_rating())
            text_lis.append(str(i.reviewcount) + " reviews")
        base_lis.append(0)
    data = [go.Bar(
        x=x_lis,
        y=y_lis,
        text=text_lis,
        base=base_lis,
    )]

    fig_title = "Average Rating" if content.lower() == "rating" else "Review Counts"
    fig_title += " ({}) ".format(sup) if sup is not None else ""

    layout = dict(
        title=fig_title,
        xaxis=dict(tickangle=-45),
    )

    fil_name = "barplot_rating" if content.lower() == "rating" else "barplot_reviewcounts"
    fil_name += "_{}".format(sup) if sup is not None else ""

    fig = dict(data=data, layout=layout)
    #py.plot(fig, filename=fil_name)
    div = off_plot(fig, show_link=False, output_type='div', auto_open=False, include_plotlyjs=False)
    return div


def pie_plot(db_name, product=None, content=None):
    data_lis = d.process_pie_data(db_name, product)
    if data_lis is None:
        return
    dic = {}

    if content is None:
        return
    else:
        if content.lower() == "age":
            for i in data_lis:
                if i.age_group() not in dic:
                    dic[i.age_group()] = 0
                dic[i.age_group()] += 1
        elif content.lower() == "skintype":
            for i in data_lis:
                if i.SkinType not in dic:
                    dic[i.SkinType] = 0
                dic[i.SkinType] += 1
        elif content.lower() == "usingyear":
            for i in data_lis:
                if i.UsingYear not in dic:
                    dic[i.UsingYear] = 0
                dic[i.UsingYear] += 1
        else:
            return

    label_lis = []
    value_lis = []
    for i in dic:
        label_lis.append(i)
        value_lis.append(dic[i])

    trace = go.Pie(labels=label_lis, values=value_lis)
    data = [trace]

    fig_title = "Distribution of {} for Product-{}".format(content, product)
    layout = dict(
        title=fig_title
    )

    fil_name = "pieplot_{}_product{}".format(content, product)
    fig = dict(data=data, layout=layout)
    #py.plot(fig, filename=fil_name)
    div = off_plot(fig, show_link=False, output_type='div', auto_open=False, include_plotlyjs=False)
    return div


def scatter_plot(db_name):
    data_lis = d.process_scatter_data(db_name)
    if data_lis is None:
        return

    x_lis = []
    y_lis = []
    for i in data_lis:
        x_lis.append(i[0])
        y_lis.append(i[1])

    trace = go.Scatter(
        x=x_lis,
        y=y_lis,
        mode='markers'
    )

    data = [trace]

    fig_title = "Relationship"
    layout = dict(
        title=fig_title,
        xaxis= dict(
            title='Rating',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
            ),
        yaxis=dict(
            title='Review Count',
            ticklen=5,
            gridwidth=2,
            )
    )

    fil_name = "scatterplot"
    fig = dict(data=data, layout=layout)
    #py.plot(fig, filename=fil_name)
    div = off_plot(fig, show_link=False, output_type='div', auto_open=False, include_plotlyjs=False)
    return div



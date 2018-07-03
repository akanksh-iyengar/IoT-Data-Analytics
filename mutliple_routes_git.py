import random
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

from bokeh.io import show, output_file
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Button, HoverTool
from bokeh.palettes import RdYlBu3
from bokeh.embed import components
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__,template_folder='./')
@app.route('/')
def the_only_routing():
    return render_template("my_analytics_page.html")

@app.route('/show_bar_graph')
def the_bar_graph_routing():
    x=[]
    y=[]
    p=figure(title="X-axis Gravity Sensor values v/s time",x_axis_label='time',y_axis_label='gravity_x')
    client=Cloudant("<user_id>","<password>",url="<db_url>")
    client.connect()
    myDatabase = client['sample_db']
    result_collection = Result(myDatabase.all_docs,include_docs=True)
    for i in result_collection:
        x.append(i['doc']['payload']['time'])
        y.append(i['doc']['payload']['gravity_x'])
    p.vbar(x=x,top=y,width=0.9)
    script, div = components(p)
    return render_template("mod_chart.html",div=div, script=script)

@app.route('/show_line_graph')
def the_line_graph_routing():
    x=[]
    y=[]
    dict_val={}
    hover=HoverTool()
    p=figure(title="X-axis Gravity Sensor values v/s time",x_axis_label='time',y_axis_label='gravity_x',tools=[hover,"pan","wheel_zoom","box_zoom","reset"])
    client=Cloudant("<user_id>","<password>",url="<db_url>")
    client.connect()
    myDatabase = client['sample_db']
    result_collection = Result(myDatabase.all_docs,include_docs=True)
    for i in result_collection:
        x.append(i['doc']['payload']['time'])
        y.append(i['doc']['payload']['gravity_x'])
        dict_val[i['doc']['payload']['time']]=i['doc']['payload']['gravity_x']
    x.sort()
    y.clear()
    for val in x:
        y.append(dict_val[val])
    print(x)
    print(y)
    p.line(x,y,line_width=2)
    script, div = components(p)
    return render_template("mod_chart.html",div=div, script=script)

@app.route('/show_area_graph')
def the_area_graph_routing():
    x=[]
    y=[]
    dict_val={}
    p=figure(title="X-axis Gravity Sensor values v/s time",x_axis_label='time',y_axis_label='gravity_x')
    client=Cloudant("<user_id>","<password>",url="<db_url>")
    client.connect()
    myDatabase = client['sample_db']
    result_collection = Result(myDatabase.all_docs,include_docs=True)
    for i in result_collection:
        x.append(i['doc']['payload']['time'])
        y.append(i['doc']['payload']['gravity_x'])
        dict_val[i['doc']['payload']['time']]=i['doc']['payload']['gravity_x']
    x.sort()
    wx=x+x[::-1]
    print(wx)
    y.clear()
    for val in x:
        y.append(dict_val[val])
    print(x)
    zeros=[0 for i in range(len(y))]
    wy=y+zeros
    print(y)
    #p.line(x,y,line_width=2)
    p.patch(wx,wy,fill_alpha=1,line_width=2)
    script, div = components(p)
    return render_template("mod_chart.html",div=div, script=script)

app.run(debug=True)

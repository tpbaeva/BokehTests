from bokeh.plotting import line, circle, curplot, xaxis, yaxis, grid, figure, hold
from bokeh.embed import autoload_static
from bokeh.resources import CDN

from flask import Flask, render_template

app = Flask(__name__)


def get_plottag(script_path):
    """ Saves js in script_path and returns tag for embedding in html
    """
    import numpy as np
    import pandas as pd
    import os

    y_data = np.random.randn(100)
    x_data = pd.date_range('31-Aug-2014', periods=len(y_data))

    figure(x_axis_type='datetime', 
           tools='pan,wheel_zoom,box_zoom,reset,previewsave,crosshair', 
           name='test plot')
    hold()
    line(x_data, y_data,
         line_color="#D95B43", line_width=4, alpha=0.7, 
         legend='random', 
         background_fill= '#cccccc')
    circle(x_data, y_data, 
           color='red', fill_color=None, size=6, 
           legend='random')
    curplot().title = 'Test Plot'
    xaxis().axis_label='date'
    yaxis().axis_label='some random numbers'
    grid().grid_line_color='white'
    grid().grid_line_alpha = 0.5

    plotid = curplot()._id
    script_path = os.path.join(script_path, plotid+'.js')
    js, tag = autoload_static(curplot(), CDN, script_path=script_path)
    with open(script_path, 'w') as f:
        f.write(js)
        
    return tag


@app.route('/')
def render_plot():
    tag = get_plottag('./static/js')

    return render_template('plot.html', tag=tag)

if __name__ == "__main__":
    app.run(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
from os.path import dirname
import flask

app = dash.Dash()
image_directory = dirname(__file__)

static_image_route = '/staticfolder/'
list_of_options = ['Word Association','Scatterplot','Word to Vector','Word Trees','Cluster','Sankey']
list_of_images = ['WordAssoc.png','Scatterplot.png','Word2Vec.png','WordTrees.png','Cluster.png','Sankey.png']


app.layout = html.Div([
    html.Div('Text Mining - Oil & Gas',style={'textAlign':'center','font-family':'verdana','font-size':'16px'}),
    html.Div([dcc.Textarea(
        placeholder='Enter Text...',
        value='Enter text here',
        rows=7,
        style={'width': '100%'})], style={'font-family' : 'verdana','font-size' : '12px','width' : '95%', 'display' : 'inline-block'}),

    html.Div([html.Button('Submit', id='button', style={'margin': '4px 2px', 'align-items': 'center','justify-content': 'center',
                                                          'color': 'RED','font-family' : 'verdana','font-size' : '18px',
                                                          'width' : '95%'})]),

    html.Div('Word Count: xxx  | Word List: xx  |',
             style={'height': '40px', 'border-color': 'blue', 'border-style': 'solid', 'border-width': '1px',
                    'font-family': 'verdana', 'font-size': '12px', 'vertical-align': 'top', 'text-align': 'left',
                    'width': '95%', 'display': 'inline-block'}),
    html.Div(' ',
             style={'height': '1px', 'border-style': 'none', 'border-width': '1px',
                    'width': '95%', 'display': 'inline-block'}),
    html.Div('Possible Hazards',
             style={'height': '60px', 'border-color': 'coral', 'border-style': 'solid', 'border-width': '1px', 'font-family': 'verdana',
                    'font-size': '12px', 'vertical-align': 'top', 'text-align': 'left', 'width': '47%',
                    'display': 'inline-block'}),
    html.Div(' ',
             style={'height': '60px', 'border-style': 'none', 'border-width': '1px', 'width': '1%',
                    'display': 'inline-block'}),

    html.Div('Potential Accidents',
             style={'height': '60px', 'border-color': 'coral', 'border-style': 'solid', 'border-width': '1px', 'font-family': 'verdana',
                    'font-size': '12px', 'vertical-align': 'top', 'text-align': 'left', 'width': '47%',
                    'display': 'inline-block'}),

    html.Div([dcc.Dropdown(id='my-dropdown',
        options = [{'label': list_of_options[i], 'value': list_of_images[i]} for i in range(len(list_of_options))],
            value='',placeholder="Select graph",
        style={'width': '100%'}), html.Img(id='image'),html.Div(id='output-container',style={'margin':'auto','max-width':'50%','max-height':'50%'})],
        style={'height':'40px','border-style':'none','border-width': '1px','font-family':'verdana','font-size':'12px',
               'vertical-align': 'top','text-align': 'left','width': '95%', 'display': 'inline-block'}),

  ])

#borrowed from this website: https://github.com/plotly/dash/issues/71

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_image_src(value):
    return static_image_route + value

@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)


if __name__ == '__main__':
    app.run_server()
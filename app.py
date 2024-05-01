from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

DataStructureCSV = pd.read_csv('C:\\Users\\Dharmin\\Downloads\\ConcordiaClasses\\PythonFunProject\\DataStructures.csv')
SortingAlgorithmsCSV = pd.read_csv('C:\\Users\\Dharmin\\Downloads\\ConcordiaClasses\\PythonFunProject\\Sorts.csv')
# Assign numeric values to each time complexity
complexity_order = {'O(1)': 1, 'O(log n)': 2, 'O(n)': 3, 'O(log(n))': 4, 'O(n^2)': 5}

# Convert time complexity strings to numeric values
DataStructureCSV['Complexity Order'] = DataStructureCSV['Speed (Time Complexity)'].map(complexity_order)

# Define the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1(children='Data Structures and Algorithms Time Complexities', style={'textAlign':'center'}),
    dcc.Dropdown(options=[{'label': DataStructure, 'value': DataStructure} for DataStructure in DataStructureCSV.DataStructure.unique()], value='Array', id='dropdown-selection'),
    html.Div(id='data-table-container', style={'margin': '20px'}),
    dcc.Graph(id='datastructureGraph')
])

# Define callback to update the data table
@app.callback(
    Output('data-table-container', 'children'),
    Input('dropdown-selection', 'value')
)
def update_data_table(selected_structure):
    filtered_DataStructureCSV = DataStructureCSV[DataStructureCSV['DataStructure'] == selected_structure]
    table_rows = [
        html.Tr([html.Th('Operation', style={'padding': '10px'}), html.Th('Description', style={'padding': '10px'}), html.Th('Speed (Time Complexity)', style={'padding': '10px'})], style={'background-color': '#f2f2f2'})
    ]
    for index, row in filtered_DataStructureCSV.iterrows():
        table_rows.append(html.Tr([
            html.Td(row['Operation'], style={'padding': '10px'}),
            html.Td(row['Description'], style={'padding': '10px'}),
            html.Td(row['Speed (Time Complexity)'], style={'padding': '10px'})
        ], style={'border-bottom': '1px solid #ddd'}))
    
    return html.Table(table_rows, style={'width': '100%', 'border-collapse': 'collapse'})

# Define callback to update the bar graph
@app.callback(
    Output('datastructureGraph', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_complexity_graph(selected_structure):
    filtered_DataStructureCSV = DataStructureCSV[DataStructureCSV['DataStructure'] == selected_structure]
    
    # Sort the DataFrame based on the numeric values
    filtered_DataStructureCSV = filtered_DataStructureCSV.sort_values(by='Complexity Order')

    # Plot the bar graph with numeric values on the y-axis
    fig = px.bar(filtered_DataStructureCSV, x='Operation', y='Complexity Order', title=f'Time Complexity of Operations for {selected_structure}')

    # Update y-axis labels to show time complexity strings
    fig.update_yaxes(tickvals=[1, 2, 3, 4, 5], ticktext=['O(1)', 'O(log n)', 'O(n)', 'O(log(n))', 'O(n^2)'])
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

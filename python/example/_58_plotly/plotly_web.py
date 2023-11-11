import pandas as pd
from sklearn.datasets import load_iris
import plotly.express as px
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    html_code = '''
    <head>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js" charset="utf-8"></script>
    </head>
    '''

    html_code += get_graph()
    return html_code


def get_graph():
    iris = load_iris()
    iris = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris["Class"] = load_iris().target

    html_code = "<H1>Graph test</H1>"
    fig = px.scatter(iris, x=["sepal length (cm)"], y="Class")
    html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    fig = px.scatter(iris, x=["petal length (cm)"], y="Class")
    html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    return html_code


if __name__ == "__main__":
    app.run(port=8080, debug=True)

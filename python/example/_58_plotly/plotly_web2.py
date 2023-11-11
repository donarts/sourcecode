import pandas as pd
from sklearn.datasets import load_iris
import plotly.express as px
from flask import Flask
from flask import request

app = Flask(__name__)


def get_graph(page_no):
    iris = load_iris()
    iris = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris["Class"] = load_iris().target
    print(iris)
    html_code = f"<H1>Graph test {page_no}</H1>"
    if page_no == 1:
        fig = px.scatter(iris, x=["sepal length (cm)"], y="Class")
        html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    elif page_no == 2:
        fig = px.scatter(iris, x=["petal length (cm)"], y="Class")
        html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    elif page_no == 3:
        fig = px.scatter(iris, x=["sepal width (cm)"], y="Class")
        html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    elif page_no == 4:
        fig = px.scatter(iris, x=["petal width (cm)"], y="Class")
        html_code += fig.to_html(include_plotlyjs=False, full_html=False)
    return html_code


# /get_graph?page=xxx
@app.route("/get_graph")
def ajax_page():
    html_code = '''
    <head>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js" charset="utf-8"></script>
    </head>
    <body>
    '''
    data = request.args.to_dict()
    page = data.get("page")
    if page is not None:
        page_no = int(page)
        html_code += get_graph(page_no)
    else:
        html_code += "<H1>ERROR</H1>"
    html_code += "</body>"
    return html_code


if __name__ == "__main__":
    app.run(port=8080, debug=True)

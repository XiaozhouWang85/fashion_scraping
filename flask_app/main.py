
from flask import Flask, render_template, request, redirect, url_for
from src.config import Config
from src.forms import PageSelect, NavPanel
from src.test_data import SAMPLE_DATA
from src.firestore import query_firestore
from src.request_parse import request_parse

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def homepage():
    return redirect('/items')
    
@app.route("/items", methods=['GET', 'POST'])
def items():

    max_price_items = 10000

    defaults = {
        'maxamount': max_price_items,
        'minamount': 0,
        'date_selection': 'Last 1 day',
        'page': 1
    }

    form_dict = request_parse(request,defaults)

    results_dict, end_query = query_firestore(form_dict)

    if len(results_dict)>0:
        first_doc_id = results_dict[0]["item_ID"]
        last_doc_id = results_dict[-1]["item_ID"]
    else:
        first_doc_id = None
        last_doc_id = None
        end_query = True


    page = int(form_dict['page'])

    nav = NavPanel(
        active_check=form_dict['active_check'],
        maxamount = form_dict['maxamount'],
        minamount = form_dict['minamount'],
        sold_check = form_dict['sold_check'],
        date_selection = form_dict['date_selection']
    )
    nav.first_doc_id.data = first_doc_id
    nav.last_doc_id.data = last_doc_id
    nav.page.data = page

    if nav.validate_on_submit():
        return redirect('/items')

    print(end_query)
    if end_query:
        next_url = None
    else:
        next_url = "blah"

    if page - 1 <= 0:
        prev_url = None
    else:
        prev_url = url_for('items', page=page-1, doc_id=first_doc_id, type='prev')

    pagination = {
        "next_url" : next_url,
        "prev_url" : prev_url,
        "page" : page
    }
    
    return render_template(
        "items.html", title="about page", items=results_dict[:9],
         nav=nav, pagination=pagination, max_price_items=max_price_items )


if __name__ == "__main__":
    app.run(debug=True)
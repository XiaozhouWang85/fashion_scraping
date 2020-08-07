
from flask import Flask, render_template, redirect, request, url_for
from src.config import Config
from src.forms import PageSelect, NavPanel
from src.test_data import SAMPLE_DATA

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def homepage():
    return redirect('/items')
    
@app.route("/items", methods=['GET', 'POST'])
def items():
    page = request.args.get('page', 1, type=int)
    total_pages = 15
    page_form = PageSelect()
    nav = NavPanel()

    page_form.page.choices = [(x+1,x+1) for x in range(max(total_pages,10))]

    if request.method == "POST":
        payload = request.form.to_dict()
        if "page" in payload:
            page = int(payload["page"])

        if "submit" in payload:
            
            maxamount = payload["maxamount"]
            minamount = payload["minamount"]

            if 'active_check' in payload:
                active_check = payload["active_check"]
            else:
                active_check = 'n'

            if 'sold_check' in payload:
                sold_check = payload["sold_check"]
            else:
                sold_check = 'n'

            date_selection = payload["date_selection"]

            print([maxamount,minamount,active_check,sold_check,date_selection])

    if page_form.validate_on_submit():
        return redirect('/items')

    if nav.validate_on_submit():
        return redirect('/items')


    if page + 1 > total_pages:
        next_url = None
    else:
        next_url = url_for('items', page=page+1)

    if page - 1 <= 0:
        prev_url = None
    else:
        prev_url = url_for('items', page=page-1)

    pagination = {
        "next_url" : next_url,
        "prev_url" : prev_url,
        "page" : page,
        "total_pages" : total_pages
    }
    
    return render_template(
        "items.html", title="about page", page_form=page_form, items=SAMPLE_DATA[:9],
         nav=nav, pagination=pagination, )


if __name__ == "__main__":
    app.run(debug=True)
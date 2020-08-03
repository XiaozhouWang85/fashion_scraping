
from flask import Flask, render_template, redirect, request, url_for
from src.config import Config
from src.forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def homepage():
    return render_template("page.html", title="HOME PAGE")

@app.route("/docs")
def docs():
    return render_template("page.html", title="docs page")

@app.route("/about")
def about():
    return render_template("page.html", title="about page")

@app.route("/shop", methods=['GET', 'POST'])
def shop():
    page = request.args.get('page', 1, type=int)
    total_pages = 15

    form = LoginForm()
    if form.validate_on_submit():
        print('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/shop')

    items = [
        {
            'url': "https://www.fashionphile.com/images/product-images/thumb/4d2c0ecb1a126f5aeeead87ed4ed0453/0544db74ed9288b14d39806aff62487d.jpg",
            "text": "A jumper"
        },
        {
            'url': "https://d38r3tbvwkical.cloudfront.net/images/216/picture/216892_1.jpg?c=1595167789",
            "text": "Another jumper"
        },
        {
            'url': "https://www.fashionphile.com/images/product-images/thumb/4d2c0ecb1a126f5aeeead87ed4ed0453/0544db74ed9288b14d39806aff62487d.jpg",
            "text": "a sweater"
        },
        {
            'url': "https://d38r3tbvwkical.cloudfront.net/images/216/picture/216892_1.jpg?c=1595167789",
            "text": "a sweater 2"
        }

    ]

    if page + 1 > total_pages:
        next_url = None
    else:
        next_url = url_for('shop', page=page+1)

    if page - 1 <= 0:
        prev_url = None
    else:
        prev_url = url_for('shop', page=page-1)

    pagination = {
        "next_url" : next_url,
        "prev_url" : prev_url,
        "page" : page,
        "total_pages" : total_pages
    }
    
    return render_template(
        "shop.html", title="about page", form=form, items=items,
         pagination=pagination, )


if __name__ == "__main__":
    app.run(debug=True)
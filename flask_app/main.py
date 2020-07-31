
from flask import Flask, render_template, redirect
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
    form = LoginForm()
    if form.validate_on_submit():
        print('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/shop')
    return render_template("shop.html", title="about page", form=form)


if __name__ == "__main__":
    app.run(debug=True)
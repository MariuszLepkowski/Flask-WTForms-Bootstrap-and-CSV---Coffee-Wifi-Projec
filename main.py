from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import csv
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)',
                           validators=[DataRequired(), URL(message="Invalid URL")]
                           )
    opening_time = StringField('Opening Time e.g. 5:30 AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30 AM', validators=[DataRequired()])
    coffee_rating = StringField('Coffee Rating', validators=[DataRequired()])
    wifi_rating = StringField('WIFI Strength Rating', validators=[DataRequired()])
    power_socket = StringField('Power Socket Availability', validators=[DataRequired()])

    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("Form validated and submitted successfully.")
        if request.method == 'POST':
            new_row = [
                form.cafe.data,
                form.location.data,
                form.opening_time.data,
                form.closing_time.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power_socket.data
            ]

            with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(new_row)
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

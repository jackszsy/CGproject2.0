from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from method import get_recommended_anime,machine_learning,get_url
import os


flag = [1,1]
likelist = []
img_url=[]
ani_name=[]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class IndexForm(FlaskForm):
    previous = SubmitField('Previous')
    like = SubmitField('Like')
    next = SubmitField('Next')

class ResultForm(FlaskForm):
    go1 = SubmitField('Go!')
    go2 = SubmitField('Go!')
    go3 = SubmitField('Go!')
    go4 = SubmitField('Go!')
    go5 = SubmitField('Go!')

class DetailForm(FlaskForm):
    back = SubmitField('Back')

def img_reader_initialization():
    path = 'static\image'
    ani_name = os.listdir(path)
    return ani_name

@app.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    ani_name=img_reader_initialization()

    if flag[0]:
        session['num'] = 0
        flag[0] = 0;

    if session['num'] < 0:
        session['num'] = len(ani_name) - 1
    if session['num'] > len(ani_name) - 1:
        session['num'] = 0

    if form.validate_on_submit():
        if len(likelist) == 10:
            return redirect(url_for('result'))

        if form.previous.data:
            session['num'] -= 1
            return redirect(url_for('index'))
        else:
            if form.like.data:
                likelist.append(ani_name[session.get('num')][0:-4])

                if len(likelist) == 10:
                    return redirect(url_for('result'))

            session['num'] += 1
            return redirect(url_for('index'))
    return render_template('index.html', form=form, anime_name=ani_name[session.get('num')])

@app.route('/result', methods=['GET', 'POST'])
def result():
    form2 = ResultForm()

    anime = machine_learning(likelist)
    if form2.go1.data:
        session['recommended_ani'] = anime[0]
        return redirect(url_for('detail'))
    if form2.go2.data:
        session['recommended_ani'] = anime[1]
        return redirect(url_for('detail'))
    if form2.go3.data:
        session['recommended_ani'] = anime[2]
        return redirect(url_for('detail'))
    if form2.go4.data:
        session['recommended_ani'] = anime[3]
        return redirect(url_for('detail'))
    if form2.go5.data:
        session['recommended_ani'] = anime[4]
        return redirect(url_for('detail'))

    if flag[1]:
        for i in anime:
            img_url.append(get_url(i))
        flag[1] = 0

    return render_template('result.html', form=form2, image_url1 = img_url[0], image_url2 = img_url[1],
                           image_url3 = img_url[2],image_url4 = img_url[3],image_url5 = img_url[4])

@app.route('/detail',methods=['GET','POST'])
def detail():
    form3 = DetailForm()
    if form3.back.data:
        return redirect('result')
    ani = get_recommended_anime(session['recommended_ani'])

    return render_template('detail.html',form = form3,title = ani[0],image_url=ani[1],synopsis=ani[2],
                           type=ani[3],episodes=ani[4],score=ani[5],start_date=ani[6],
                           end_date=ani[7],rated=ani[8],members=ani[9])
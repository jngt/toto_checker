from flask import Flask, render_template, request
from app.scripts.scraping import get_scr_data, cat_pred
from app.scripts.renderer import create_view_form, create_input_form, create_home
from app.scripts.inout import create_pred_list, save_list, load_list

app = Flask(__name__)

@app.route('/')
def index():
    now = request.args.get('id')
    home = create_home(now)
    return render_template('index.html', home=home)

@app.route('/<flag>')
def toto(flag):
    now = request.args.get('id')
    home = create_home(now)
    toto_df = get_scr_data(flag, now)
    pred_list = load_list(flag, now)
    toto_df, n_match = cat_pred(toto_df, pred_list)

    thtml = toto_df.to_html(classes='table', index=False)
    thtml = create_view_form(thtml, flag, n_match, now)
    return render_template('index.html', thtml=thtml, home=home)

@app.route('/<flag>', methods=['POST'])
def post(flag):
    now = request.args.get('id')
    home = create_home(now)
    if request.method == 'POST':
        if request.form['post_value'] == 'INPUT':
            toto_df = get_scr_data(flag, now)
            pred_list = load_list(flag, now)
            toto_df, n_match = cat_pred(toto_df, pred_list)

            thtml = toto_df.to_html(classes='table', index=False)
            thtml = create_input_form(thtml, flag, now)

        elif request.form['post_value'] == 'SAVE':
            toto_df = get_scr_data(flag, now)
            pred_list = create_pred_list(request.form)
            save_list(pred_list, flag, now)
            toto_df, n_match = cat_pred(toto_df, pred_list)

            thtml = toto_df.to_html(classes='table', index=False)
            thtml = create_view_form(thtml, flag, n_match, now)
    return render_template('index.html', thtml=thtml, home=home)

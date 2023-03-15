from flask import Flask, render_template, flash, redirect, url_for, jsonify, request
import os
from forms import uploadForm
import werkzeug
from img_proc import color_palette, api_color
from delete_image import delete_image
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/images'
app.config['SECRET_KEY'] = 'KASJVDHJT8767876UGFGjhvdbjh83'

@app.template_filter('rounding')
def rounding(num: float):
    return round(num, 2)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def test():
    delete_image(app.config['UPLOAD_FOLDER'])
    img_path = './static/sample.jpg'
    colors, tot_pxs = color_palette(img_path, 5)

    print(colors)
    form = uploadForm()
    if form.validate() and form.is_submitted():
        print('form validated')
        f = form.file.data
        filename = werkzeug.utils.secure_filename(f.filename)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(img_path)
        colors, tot_pxs = color_palette(img_path, form.colors.data)
        return render_template('index3.html', img_path=img_path, form=form, colors=colors, tot_pxs=tot_pxs)
    elif form.is_submitted():
        if 'This field is required.' in form.file.errors:
            print('errors in form', form.file.errors)
            flash(f'Select an image')
        else:
            print('errors in form', form.file.errors)
            flash(f'We only accept images')
        return redirect(url_for('test'))

    return render_template('index3.html', img_path=img_path, form=form, colors=colors, tot_pxs=tot_pxs, year=datetime.now().year)

@app.route('/api', methods = ['GET', 'POST'])
def api_response():
    if request.method == 'POST':
        data_recived = request.files['image']
    return jsonify(api_color(data_recived.stream, num_color=int(request.values.get('num_colors'))))


if __name__ == '__main__':
    app.run(debug=True)


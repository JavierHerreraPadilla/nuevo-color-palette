from flask import Flask, render_template, flash, redirect, url_for
import os
from forms import uploadForm
import werkzeug
from img_proc import color_palette
from delete_image import delete_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/images'
app.config['SECRET_KEY'] = 'KASJVDHJT8767876UGFGjhvdbjh83'

@app.template_filter('rounding')
def rounding(num: float):
    return round(num, 2)



@app.route('/', methods=['POST', 'GET'])
def index():
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
        return render_template('index.html', img_path=img_path, form=form, colors=colors, tot_pxs=tot_pxs)
    elif form.is_submitted() and not form.validate():
        print('errors in form', form.file.errors)
        flash(f'ONLY IMAGE-TYPE FILES')
        return redirect(url_for('index'))

    return render_template('index.html', img_path=img_path, form=form, colors=colors, tot_pxs=tot_pxs)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

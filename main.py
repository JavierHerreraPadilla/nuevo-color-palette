from flask import Flask, render_template
import os
from forms import uploadForm
import werkzeug



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static'
app.config['SECRET_KEY'] = 'KASJVDHJT8767876UGFGjhvdbjh83'

@app.route('/', methods=['POST', 'GET'])
def index():
    img_path = './static/images.jpg'
    form = uploadForm()
    if form.validate():
        print('form validated')
        f = form.file.data
        filename = werkzeug.utils.secure_filename(f.filename)
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        print(filename)
    else:
        print('errors in form', form.file.errors)
    return render_template('index.html', img_path=img_path, form=form)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

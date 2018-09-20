from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from utilfunc import get_split_point
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'XOIU01293jkjsjfdg127'

type_ls = [('1', 'equal_count'), ('2', 'equal_interval'), ('3', 'nature_breaks'), ('4', 'standard_deviation')]


class SubForm(FlaskForm):
    values = TextAreaField('输入数组（逗号分隔）')
    type = SelectField(u'分段类型', choices=type_ls)
    count = StringField('分段数', validators=[DataRequired()])
    decimal = StringField('结果位数')
    submit = SubmitField('计算')


class ResultForm(FlaskForm):
    result = StringField('裂点')


@app.route('/', methods=['GET', 'POST'])
def index():
    sub_form = SubForm()
    result_form = ResultForm()

    if sub_form.validate_on_submit():
        data = sub_form.values.data.split(',')
        data = [float(item.strip()) for item in data]
        spilt_type = dict(type_ls).get(sub_form.type.data)
        spilt_count = int(sub_form.count.data)
        result_decimal = int(sub_form.decimal.data)

        result = get_split_point(data, spilt_count, spilt_type, result_decimal)

        result_form.result.data = result

    return render_template('index.html', sub_form=sub_form, result_form=result_form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)
    # app.run(debug=True)


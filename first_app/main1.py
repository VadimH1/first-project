# Я создал класс Форм в файле "login.py" и прописал в нём все наши поля
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_name = StringField("User_name", validators=[DataRequired()])
    user_second_name = StringField("User_second_name", validators=[DataRequired()])
    phone_number = StringField("Phone_number", validators=[DataRequired()])
    password = PasswordField ("Password", validators=[DataRequired()])
    password_confirmation = PasswordField("Password_Confirmation", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    
# А вот тут я завис совсем. Попробовал сделать своё с message,но получается ощибка. 
# Нам надо в наш словарь, в значение внести верные данные, которые будут потом проверятся?
# income_form_data у нас то же, что я сделал с message?
    
from flask import Flask, request, render_template
# from Lesson.login import LoginForm

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        print("Ми викликали GET")
        return render_template("index.html")

    if request.method == "POST":
        print("Ми викликали POST")
        form = LoginForm(request.form) # ImmutableMultiDict([('fname', 'Andy'), ('lname', 'KOOccccc')])
        # import pdb; pdb.set_trace()
        message = ""
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        if user_name == "Vadim" and password == "Hal":
            message = "Correct user_name and password"
        else:
            message = "Wrong user_name or password"
        _data = {
            "fname": form["fname"],
            "lname": form["lname"]
        }
        return render_template("index.html", income_form_data=_data, message=message)


@app.route("/hello")
def hello():
    return "Hello Andy"


if __name__ == "__main__":
    app.run(debug=True)  
    
    
# Шаблон index.html    
<!DOCTYPE html>
<html>
<head>
    <h3><title>My first app</title></h3>
</head>
<body>
        <h1>Sign in</h1>
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    <form action="/" method="POST">
        <label for="fname">User_name:</label><br>
        <input type="text" id="fname" name="fname"><br><br>
        <label for="lname">User_second_name:</label><br>
        <input type="text" id="lname" name="lname"><br><br>
        <label for="phone">Phone_number:</label><br>
        <input type="text" id="phone" name="phone"><br><br>
        <label for="pswrd">Password:</label><br>
        <input type="text" id="pswrd" name="pswrd"><br><br>
        <label for="pswrd_c">Password_Confirmation:</label><br>
        <input type="text" id="pswrd_c" name="pswrd_c"><br><br>
        <input type="submit" value="Submit">
    </form>
    {% if income_form_data %}
        <h1>{{ income_form_data.fname }}</h1><h1>{{ income_form_data.lname }}</h1>
    {% endif %}
</body>
</html>    
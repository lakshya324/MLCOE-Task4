from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    validators,
    SelectField,
    IntegerField,
    RadioField,
)


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=30)])
    email = StringField(
        "Email",
        [
            validators.Email(message="Invalid email address"),
            validators.Regexp(
                ".*@akgec.ac.in$", message="Email must end with @akgec.ac.in"
            ),
        ],
    )
    password = PasswordField("Password", [validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class PredictForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired()])
    gender = RadioField(
        "Gender",
        choices=[(0, "Female"), (1, "Male")],
        validators=[validators.InputRequired()],
    )
    income = IntegerField(
        "Income", validators=[validators.NumberRange(min=1,message='Value Must be greater then 0')]
    )
    co_applicant_income = IntegerField(
        "Co-Applicant Income",
        validators=[validators.NumberRange(min=1,message='Value Must be greater then 0')],
    )
    loan_amount = IntegerField(
        "Loan Amount",
        validators=[validators.NumberRange(min=1, max=56000,message='Value Must be greater then 0 and less than 56000')],
    )
    loan_amount_term = SelectField(
        "Loan Amount Term",
        choices=[
            (15,  "15 days"),
            (30,  "1 Month"),
            (60,  "2 Months"),
            (90,  "3 Months"),
            (120, "4 Months"),
            (180, "6 Months"),
            (240, "8 Months"),
            (300, "10 Months"),
            (360, "1 Year"),
            (540, "1.5 Years"),
        ],
        validators=[validators.InputRequired()],
    )
    credit_history = RadioField(
        "Credit History (Taken a loan yet)",
        choices=[(1, "Yes"), (0, "No")],
        validators=[validators.InputRequired()],
    )
    dependents = SelectField(
        "Dependents",
        choices=[(0, "None"), (1, "1"), (2, "2"), (3, "3+")],
        validators=[validators.InputRequired()],
    )
    education = SelectField(
        "Education",
        choices=[(1, "Graduation"), (0, "Not Graduate")],
        validators=[validators.InputRequired()],
    )
    self_employed = BooleanField("Self Employed")
    married = BooleanField("Married")
    property_area = SelectField(
        "Property Area",
        choices=[(0,"Rural"),(1,"Semi-Urban"),(2,"Urban")],
        validators=[validators.InputRequired()],
    )
    submit = SubmitField("Predict")

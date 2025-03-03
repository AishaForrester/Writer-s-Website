"""An object from this form can be used to send data over to the database. In the event that the 
controller recieves a GET registration request, it will render the signup.html template and sends 
this form object over to the template. The template will then render the form fields with the help of
additional macros. If the controller receives a POST request, it will validate the form object and 
send the data over to the database
Database
controller
signup.html
 """
from app.models import *
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired

class userForm(FlaskForm):
    formSubmitted = False #putting the form in an unsubmitted state
    fname = StringField('Your first name', [validators.DataRequired(),
                                     validators.length(min=1, max=80)])
    lname = StringField('Your last name', [validators.DataRequired(),
                                     validators.length(min=1, max=80)])
    email = StringField('Your email', [validators.DataRequired(),
                                       validators.length(min=10, max=80)])
    password = PasswordField('Your password', [validators.DataRequired(), 
                                               validators.Length(max=70),
                                               validators.EqualTo('confirm', message='Ensure both passwords match')
                                               ])
    confirm = PasswordField('Re-enter password', [validators.DataRequired(),
                                                 validators.Length(max=70),
                                                 validators.EqualTo('password', message='Ensure passwords match')
                                                 ])
    username = StringField('Username', [validators.Length(min=1, max=50),
                                        validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.NumberRange(min=1, max=80)])
    gender = SelectField('Your gender', choices=[('none','--select--'),('Male', 'Male'),
                                                 ('Female', 'Female'), ('Other', 'Other')])
    profile_image = FileField('Upload a profile image(Optional)')
    bio = StringField('Profile Bio (Optional)', validators = [validators.Length(min=0, max=200)])


    def validate_username(form, field):
        user = userAccount.query.filter_by(username=field.data).first()
        if user is not None: #username already exists in the database
            raise ValidationError('Username already exists. Please choose another name')
        
    def validateGender(form, field):
        if field.data == 'none':
            raise ValidationError('Please select an appropriate gender')
    def validFileExtension(filename):
        allowed_extensions = ['jpg', 'jpeg', 'png']
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
        
class LoginForm(FlaskForm):
    username = StringField('Your username', validators = [validators.DataRequired()])
    password = StringField('Your password', validators = [validators.DataRequired()])
    remember_me = BooleanField('Remember me')

class CreateBook(FlaskForm):
    form_submit = False


    title = StringField('Title', validators=[validators.DataRequired()])
    synopsis = StringField('Synopsis', validators=[validators.DataRequired()])
    
    # Use DecimalField for price
    price = DecimalField('Price', places=2, validators=[validators.DataRequired(), validators.NumberRange(min=0, message="Price must be a positive value")])
    
    # Updated genre choices
    genre = SelectField('Genre', choices=[
        ('none', '--select--'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('romance', 'Romance'),
        ('young_adult', 'Young Adult'),
        ('children', 'Children'),
        ('history', 'History'),
        ('travel', 'Travel'),
        ('art', 'Art'),
        ('other', 'Other')  # Option for other genres
    ])
    
    image = FileField('Image', validators=[validators.DataRequired()])

    # Add the hidden project_type field
    # Use StringField for project_type (since it's selected by JavaScript)
    project_type = SelectField('Project Type', 
                               validators=[validators.DataRequired()],
                               choices=[('none', '--select--'),
                                   (    'short_story', 'Short Story'),
                                        ('novel', 'Novel'),
                                        ('poem', 'Poem')])
    
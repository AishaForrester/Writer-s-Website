from app import app, db, login_manager
from flask import abort, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.forms import * #lookk back on this please
from app.models import *
import random, os, datetime #, requests, urlparse
from flask_bcrypt import Bcrypt


"""________________________________Application Routing_________________________"""
#codergirl11, 12345678
@app.route('/')
def home():
    """Serving the website's home page"""
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')


"""___________________________________________API PATHS____________________________________________"""

@app.route('/api/users/signup', methods = ["GET","POST"])
def signup():
    form = userForm() #create the form object
    if request.method == 'POST': #needed for use to communicate with the database and front-end
        print('received post request')
        form.formSubmitted = True
        if form.validate_on_submit(): #form is validated
            if 'profile_image' in request.files:  # Ensure file exists
                file = request.files['profile_image']
                if file.filename != "":
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    filename = None


                if form.bio.data =='':
                    form.bio.data = app.config['DEFAULT_BIO']

                hashed_password = bcryptHash.generate_password_hash(form.password.data).decode('utf-8')
                
                newAccount = userAccount(form.fname.data, form.lname.data,
                                         form.username.data, hashed_password, form.age.data,
                                           form.gender.data, form.bio.data, filename) 
                                   
                try:
                    db.session.add(newAccount)
                    db.session.commit()
                    flash('Thank you for creating a profile with us. Let\'s log you in','success')
                    login_user(newAccount)
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    flash('Something went wrong while creating your account', 'danger')
                    print(f"Error: {e}")

                if form.validate_on_submit():
                    db.session.add(newAccount)
                    db.session.commit()

        else:
            flash("Form validation failed, please check the field and try again", "danger")
    return render_template('signup.html', form=form)
    



@app.route('/api/users/login', methods=["GET", "POST"])
def login():

    #If the user is already authenticated, redirect to profile
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = LoginForm()            #Initializing the login form
    #projectForm = CreateBook()    Initializing the project form
        
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            #Check if the user name exists in the database
            user = userAccount.query.filter_by(username = username).first()

            #If the user is found
            if user:
                #verify the password
                if bcryptHash.check_password_hash(user.password, password):

                   # Handle "remember me" checkbox
                    remember_me = form.remember_me.data  # Simplified check

                    login_user(user, remember=remember_me)
                    

                    #Redirect the user to their profile or the next page
                    next_page = request.args.get('next')
                    
                    if next_page and next_page.startswith('/'):    #If there was a next page, redirect there
                        return redirect(next_page)
                    else:       #otherwise, redirect to the profile
                        flash("You were successfully logged in", "success")
                        return redirect(url_for('profile'))
                        #return redirect('profile.html', username=current_user.username, form=projectForm)
                else:
                    flash('Incorrect password', 'danger')
            else:
                flash('Username not found', 'danger')

    return render_template('login.html', form=form)

@app.route('/api/users/logout', methods=["GET"])
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for("home"))
            
@app.route('/api/users/profile', methods=["GET", "POST"])
@login_required
def profile():
    projectForm = CreateBook() #Initializing the project form

    #Fetching projects from database to send to profile template when it is rendered
    projects_db = Projects.query.order_by(Projects.created_at.desc()).all()
    if len(projects_db) > 10:
        projects_db = projects_db[:10] #slice the first 10

    
    
    if current_user.is_authenticated:
        print(f"Is user authenticated? {current_user.is_authenticated()}")
        if request.method == 'POST':
          
            if projectForm.validate_on_submit():
                print("validated on submission") #debug
                

               # Handling image upload 
                file = request.files.get('image')

                if file and file.filename != "":
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    print(f"Uploading file: {filename}")  # Debugging
                    print(f"Saving to: {file_path}")  # Debugging

                    file.save(file_path)  # Save file
                else:
                    filename = None
                    print("No file uploaded")  # Debugging

                #Get the project type from the hidden input field
                #project_type = request.form.get('project_type')
                #print(f"Project Type from form: {project_type}")

                #Creating a new project instance
                print(f"Project Type: {projectForm.project_type.data}")
                new_project = Projects(
                projectForm.title.data, 
                projectForm.synopsis.data, 
                str(projectForm.genre.data),    # ✅ Ensure genre is a string
                float(projectForm.price.data),  # ✅ Convert to float
                filename,
                str(projectForm.project_type.data) #use the selected project type
                )
                print(f"Title: {projectForm.title.data} ({type(projectForm.title.data)})")
                print(f"Synopsis: {projectForm.synopsis.data} ({type(projectForm.synopsis.data)})")
                print(f"Price: {projectForm.price.data} ({type(projectForm.price.data)})")
                print(f"Genre: {projectForm.genre.data} ({type(projectForm.genre.data)})")
                print(f"Project Type: {projectForm.project_type.data}")
                print('database book object created: ', str(new_project))
                try:
                    #Add the new project to the database and commit
                    db.session.add(new_project)
                    db.session.commit()
                    flash("Project created successfully", "success")

                    #Redirecting to projects and sending a reference of the newly created book object over
                    #it will generate /api/users/projects/5 if project_id is 5
                    return redirect(url_for('projects', project_id=new_project.id))
                
                except Exception as e:
                    db.session.rollback()
                    flash('Something went wrong while creating your new project', 'danger')
                    print(f"Error: {e}")  
          
        return render_template("profile.html", form=projectForm, username=current_user.username, projects = projects_db)
    
    else:
        return redirect(url_for('login')) #redirect to login in the event that they are not authenticated

        
@app.route('/api/users/projects/<int:project_id>', methods=["GET"]) 
@login_required
def projects(project_id):
    """
    ______________________________Explanation of what is happening here________________________________

    When we add the new project (book, poem or short story) object to the database and redirect the user via the
    project view function, we also sent over the project id (unique). The project view function gets this book id and 
    has access to it via the url. As the project view function renders the template, it renders it with the 
    database book object. Therefore, we are able to access the book object that they have just created and 
    make changes it accordingly

    Two ways to get here: 
    1) Create new project (profile view - automatic rediect)  
    2) View existing project(contentsignedin - click the project link)
    """
    
    
    #Get the book_id from the url
    #project_id = request.args.get('project_id', type=int)

    #Getting the id of the project object that was sent over from the profile view function
    project = Projects.query.get_or_404(project_id)  #404 if not found
    print(f"Project sent from the profile: {project}")  # Debugging....works
    

    content_query = None
   #Determine content type based on the project type
    if project.project_type == "novel":

        #retrieves all the chapters associated with the book
        content_query = Chapter.query.filter_by(book_id=project_id).order_by(Chapter.chapter_number.asc())

    elif project.project_type == "short_story":

        #retrieves all the pages associated with the book
        content_query = Page.query.filter_by(story_id=project_id).order_by(Page.page_number.asc())

    elif project.project_type == "poem":

        #retrieve all the poems associated with the book
        content_query = Poem.query.filter_by(poem_id=project_id).order_by(Poem.page_number.asc())

    else:
        content_query = None
    
    #Pagination logic
    page = request.args.get('page', 1, type=int) ## Get current page number from the query string
    per_page = 1
    #paginate the content_query, meaning paginating all the chapter or pages of a given project
    content = content_query.paginate(page=page, per_page=per_page, error_out=False) if content_query else None
    # Fetch the current page object if available
    current_page = content.items[0] if content and content.items else None


    
    return render_template("projects.html", project=project, content=content, current_page=current_page)

   

    


@app.route('/api/users/projects/add-content', methods=['POST'])
@login_required
def add_content():
    print("Received form data:", request.form)  # Debugging print statement

    # Get the project ID correctly from form data
    #project_id = request.args.get('project_id', type=int)
    project_id = request.form.get('project_id', type=int) #grab project_id from form data
    project = Projects.query.get_or_404(project_id)  # Ensure project exists in database

    #Chapter information
    chapter_id = request.form.get("chapter_id")  # Only for chapters
    title = request.form.get('title')  # Only for chapters 
     
    content_text = request.form.get('content', '').strip()  # Get content from form data

    st_id = request.form.get("pageS_id")  
    po_id = request.form.get("poem_id")  
    
    

    try:
        if project.project_type == "novel":
            if chapter_id and chapter_id != "new":  
                # **Update existing chapter**
                chapter = Chapter.query.get(chapter_id)
                if chapter and chapter.book_id == project.id:
                    chapter.title = title
                    chapter.content = content_text
                    db.session.commit()
                    flash("Chapter updated successfully!", "success")
                else:
                    flash("Chapter not found or unauthorized!", "danger")
                    return redirect(url_for('projects', project_id=project_id))
            else:
                # **Create new chapter**
                new_chapter = Chapter(book_id=project.id, title=title, content=content_text)
                db.session.add(new_chapter)
                db.session.commit()
                flash("New chapter added successfully!", "success")
                

        elif project.project_type == "short_story":
            new_page_number = 1  # Default page number

            if st_id and st_id != "new":
                page = Page.query.get(st_id)
                if page and page.story_id == project.id:
                    print(f"Updating page ID {st_id}")  
                    page.content = content_text
                    db.session.commit()
                    flash("Page updated successfully!", "success")
                    new_page_number = page.page_number  
                else:
                    flash("Page not found or unauthorized!", "danger")
                    return redirect(url_for('projects', project_id=project_id))
            else:
                total_pages = Page.query.filter_by(story_id=project.id).count()
                new_page_number = total_pages + 1  

                print("Creating a new page")  
                new_page = Page(story_id=project.id, content=content_text, page_number=new_page_number)
                db.session.add(new_page)
                db.session.commit()
                flash("New page added successfully!", "success")

            return redirect(url_for('projects', project_id=project.id, page=new_page_number))  # ✅ Stay on correct page

        elif project.project_type == "poem":
            new_page_number = 1  

            if po_id and po_id != "new":
                poem = Poem.query.get(po_id)
                if poem and poem.poem_id == project.id:
                    print(f"Updating poem ID {po_id}")  
                    poem.content = content_text
                    db.session.commit()
                    flash("Poem updated successfully!", "success")
                else:
                    flash("Poem not found or unauthorized!", "danger")
                    return redirect(url_for('projects', project_id=project_id))
            else:
                total_pages = Poem.query.filter_by(poem_id=project.id).count()
                new_page_number = total_pages + 1  

                print("Creating a new poem")  
                poem_page = Poem(poem_id=project.id, content=content_text, page_number=new_page_number)
                db.session.add(poem_page)
                db.session.commit()
                flash("New poem added successfully!", "success")

            return redirect(url_for('projects', project_id=project.id, page=new_page_number))  # ✅ Stay on correct page

    except Exception as e:
        db.session.rollback()
        flash(f"Error saving content: {e}", "danger")
        print(f"Error saving content: {e}")  # Debugging log

    return redirect(url_for('projects', project_id=project_id))  # ✅ Default redirect if nothing else applies

@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Projects.query.get_or_404(project_id)  # Ensure project exists

    if project.user_id != current_user.id:  # Check ownership
        flash("Unauthorized action!", "danger")
        return redirect(url_for('projects', project_id=project.id))

    # Delete related content first (to avoid foreign key constraints)
    Chapter.query.filter_by(book_id=project.id).delete()  # Delete all chapters
    Page.query.filter_by(story_id=project.id).delete()  # Delete all pages

    db.session.delete(project)  # Mark project for deletion
    db.session.commit()  # Apply changes to the database

    flash("Project deleted successfully!", "success")
    return redirect(url_for('profile'))  # Redirect to dashboard or another page
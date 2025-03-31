from app import app, db, login_manager
from flask import abort, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.forms import * #lookk back on this please
from app.models import *
import random, os, datetime #, requests, urlparse
from flask_bcrypt import Bcrypt
from flask import current_app
from sqlalchemy.orm import joinedload


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
    projects_forall = Projects.query.order_by(Projects.created_at.desc()).all()
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
                str(projectForm.project_type.data), #use the selected project type
                user_id=current_user.id
                )


                #Add the new project to the database and commit
                db.session.add(new_project)
                db.session.commit()
                flash("Project created successfully", "success")


                #creating the corresponding book object
                new_user_book = userBooks(
                    title= projectForm.title.data,
                    author= current_user.username,
                    genre= projectForm.genre.data,
                    price= projectForm.price.data,
                    description= projectForm.synopsis.data,
                    cover_image= filename,
                    book_format= projectForm.project_type.data,
                    project_id = new_project.id
                )
                

                try:
                    
                    db.session.add(new_user_book)
                    db.session.commit()
                    flash("Book added globally", "success")

                    #Redirecting to projects and sending a reference of the newly created book object over
                    #it will generate /api/users/projects/5 if project_id is 5
                    return redirect(url_for('projects', project_id=new_project.id))
                
                except Exception as e:
                    db.session.rollback()
                    flash('Something went wrong while creating your new project', 'danger')
                    print(f"Error: {e}")  

        #when we get the page, we will display with word count for all projects
        projectwcount = Projects.query.options(
        joinedload(Projects.chapters).joinedload(Chapter.pages),  # Eagerly load chapters and their pages
        joinedload(Projects.poem_content)  # Eagerly load poems
    ).all()
        
        
        # List to store project word counts
        project_word_counts = []  
        for project in projectwcount:
            total_words = 0

            # Count words in all chapters (including pages in chapters)
            for chapter in project.chapters:
                for page in chapter.pages:
                    total_words += count_words(page.content)
                # Count words in all poems
            for poem in project.poem_content:
                total_words += count_words(poem.content)
                print(f"Counting words for poem {poem} - Total words: {total_words}")

                # Store the result for each project
            project_word_counts.append({
                'project_title': project.title,
                'total_words': total_words
            })

            
            top_n_projects = sorted(project_word_counts, key=lambda x: x['total_words'], reverse=True)[:10]
            #removed project_word_counts=project_word_counts from below line of code, place to allow all projects to be shown in graph
            
           # Calculate average word count
            total_word_count = sum(project['total_words'] for project in project_word_counts)
            average_word_count = total_word_count / len(project_word_counts) if project_word_counts else 0

            
        # Pass everything to the template
        return render_template("profile.html", form=projectForm, username=current_user.username,
                               projects=projects_db,
                                allProjects=projects_forall,
                                project_word_counts=top_n_projects,
                                average_word_count=average_word_count,
                                
                            )
    
    else:
        return redirect(url_for('login')) #redirect to login in the event that they are not authenticated

# Function to count words in a given text, helper function
def count_words(text):
    return len(text.split()) if text else 0
      
@app.route('/api/users/projects/<int:project_id>', methods=["GET"]) 
@login_required
def projects(project_id):
    """
    ______________________________Explanation of what is happening here________________________________

    Purpose: To view the contents of a project 

    3 ways to get here: 
    1) Create new project (profile view - automatic rediect)  
    2) View existing project(contentsignedin - click the project link)
    3) Explore page
    """
    
    
    #Get the book_id from the url
    #project_id = request.args.get('project_id', type=int)

    #Getting the id of the project object that was sent over from the profile view function
    project = Projects.query.get_or_404(project_id)  #404 if not found
    print(f"Project sent from the profile: {project.title}")  # Debugging....works
    print(f"Project sent from the profile: {project.id}")  # Debugging....works
    
    

    content_query = None
   #Determine content type based on the project type
    if project.project_type == "novel":

        # Get all chapters for the given book
        chapters = Chapter.query.filter_by(book_id=project_id).order_by(Chapter.chapter_number.asc()).all()
        
        # Get all pages linked to those chapters
        chapter_ids = [chapter.id for chapter in chapters]
        content_query = (
        db.session.query(Page)
        .join(Chapter, Page.chapter_id == Chapter.id)
        .filter(Page.chapter_id.in_(chapter_ids))
        .order_by(Chapter.chapter_number.asc(), Page.page_number.asc())
        ) if chapter_ids else None
    elif project.project_type == "short_story":

        # Retrieves all the standalone pages for a short story
        content_query = Page.query.filter(Page.story_id == project_id, Page.chapter_id.is_(None)).order_by(Page.page_number.asc())

    elif project.project_type == "poem":

        #retrieve all the poems associated with the book
        #content_query = Poem.query.filter_by(poem_id=project_id).order_by(Poem.page_number.asc())
        content_query = Poem.query.filter_by(poem_id=project_id)

    else:
        content_query = None
    
    #Pagination logic 
    page = request.args.get('page', 1, type=int) ## Get current page number from the query string
    per_page = current_app.config.get('ITEMS_PER_PAGE', 1)  # Get the number of items per page from the config
    #paginate the content_query, meaning paginating all the chapter or pages of a given project
    #content = content_query.paginate(page=page, per_page=per_page, error_out=False) if content_query else None
    # Fetch the current page object if available
    #current_page = content.items[0] if content and content.items else None
    if content_query and content_query.count() > 0:  
        content = content_query.paginate(page=page, per_page=per_page, error_out=False)
        current_page = content.items[0] if content.items else None
        current_page_number = content.page if content else None
    else:
        content = None
        current_page = None
        current_page_number = None

    print(current_page)
    print(type(current_page))

    
    return render_template("ProjectPage.html", project=project, content=content, current_page=current_page, current_page_number=current_page_number)

   

    


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
            if chapter_id and chapter_id != "new":  #see story, might be a bug
                # **Update existing chapter**
                chapter = Chapter.query.get(chapter_id)
                if chapter and chapter.book_id == project.id:
                    chapter.title = title 
                    #we do not add the content here because the content is added to the pages
                    db.session.commit()
                    flash("Chapter updated successfully!", "success")

                    #add content to existing page, check please....
                    page = Page.query.filter_by(chapter_id=chapter_id).first()
                    if page:
                        page.content = " " + content_text  # ✅ Append new content instead of overwriting
                        db.session.commit()
                        flash("Content added to the chapter's first page!", "success")
                else:
                    flash("Chapter not found or unauthorized!", "danger")
                    return redirect(url_for('projects', project_id=project_id))
            else: # Create a new chapter
                # Get the next chapter number
                last_chapter = Chapter.query.filter_by(book_id=project.id).order_by(Chapter.chapter_number.desc()).first()
                next_chapter_number = last_chapter.chapter_number + 1 if last_chapter else 1  # Start from 1 if no chapters exist

                # **Create new chapter**
                new_chapter = Chapter(book_id=project.id, title=title, chapter_number=next_chapter_number)
                db.session.add(new_chapter)
                db.session.commit()
                flash("New chapter added successfully!", "success")

                # Find the latest page number in the chapter, new
                """chapter_id = new_chapter.id
                last_page = Page.query.filter_by(chapter_id=chapter_id).order_by(Page.page_number.desc()).first()
                new_page_number = last_page.page_number + 1 if last_page else 1  # Get the next page number"""
                
                #new_page = Page(story_id=project.id, chapter_id=new_chapter.id, content=content_text, page_number=1)



                # Create first page for the chapter page_number was equal to 1
                new_page_number = 1  # Default page number
                new_page = Page(story_id=project.id, chapter_id=new_chapter.id, content=content_text, page_number=new_page_number)
                db.session.add(new_page)
                db.session.commit()
                flash("New page added to the chapter", "success")
                

        elif project.project_type == "short_story":
            new_page_number = 1  # Default page number

            if st_id and st_id != "new":
                page = Page.query.get(st_id)
                if page and page.story_id == project.id:
                    print(f"Updating page ID {st_id}")  
                    #page.content = content_text
                    page.content += " " + content_text  # ✅ Append new content instead of overwriting
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
            #new_page_number = 1  

            if po_id and po_id != "new":
                poem = Poem.query.get(po_id)
                if poem and poem.poem_id == project.id:
                    print(f"Updating poem ID {po_id}")  
                    #poem.content = content_text overwriting the content
                    poem.content = " " + content_text  # ✅ Append new content instead of overwriting
                    db.session.commit()
                    flash("Poem updated successfully!", "success")
                else:
                    flash("Poem not found or unauthorized!", "danger")
                    return redirect(url_for('projects', project_id=project_id))
            else:
                #total_pages = Poem.query.filter_by(poem_id=project.id).count()
                #new_page_number = total_pages + 1  

                print("Creating a new poem")  
                #poem_page = Poem(poem_id=project.id, content=content_text, page_number=new_page_number)
                new_poem = Poem(poem_id=project.id, content=content_text) #omly need content, no page #
                db.session.add(new_poem)
                db.session.commit()
                flash("New poem added successfully!", "success")

            #return redirect(url_for('projects', project_id=project.id, page=new_page_number))  # ✅ Stay on correct page
            return redirect(url_for('projects', project_id=project.id))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error saving content: {e}", "danger")
        print(f"Error saving content: {e}")  # Debugging log

    return redirect(url_for('projects', project_id=project_id))  # ✅ Default redirect if nothing else applies

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Projects.query.get_or_404(project_id)  # Ensures project exists
    try:
        db.session.delete(project)
        db.session.commit()
        flash("Project deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting project: {e}", "danger")
    return redirect(url_for('profile.html'))  # Redirect to main project list





@app.route('/api/users/<string:username>', methods=["GET"])
def myProfile(username):
    #Get the user by username
    user = userAccount.query.filter_by(username=username).first()

    #ensure user is authenticated first
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    projects = Projects.query.filter_by(user_id=current_user.id).all()

    if not user:
        return "User not found", 404
    
    return render_template('myprofile.html', user=user, projects=projects)

@app.route('/api/users/explore-page', methods=["GET"])
def explore():
    allprojects = userBooks.query.all()
    print(allprojects)

    #grouping/ordering
    genres = set(allprojects.genre for allprojects in allprojects) #unique genres

    return render_template('explore.html', projects=allprojects, genres=genres)


def format_date_joined(date):

    """our date will be converted into a string based on the given format Month, Year. This is more visually
    appealing to the user"""
    return date.strftime("%B, %Y")
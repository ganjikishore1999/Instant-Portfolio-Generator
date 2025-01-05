# from flask import Flask, render_template, request
# import os

# app = Flask(__name__, template_folder="templates")

# # Route for the input form
# @app.route('/')
# def index():
#     return render_template('index1.html')

# @app.route('/register')
# def register_user():
#     return render_template('register.html')
# @app.get('/login')
# def login_user():
#     return render_template('login.html')
# @app.get('/home')
# def home_page():
#     return render_template('home.html')


# # Route to generate the portfolio
# @app.route('/portfolio', methods=['POST'])
# def portfolio():
#     # Get user input from the form
#     name = request.form['name']
#     profession = request.form['profession']
#     bio = request.form['bio']
#     skills = request.form.getlist('skills')
#     photo = request.files['photo']

#     # Save the uploaded photo
#     photo_path = None
#     if photo:
#         photo_path = os.path.join('static/images', photo.filename)
#         photo.save(photo_path)

#     # Render the portfolio with the user's details
#     return render_template(
#         'portfolio.html',
#         name=name,
#         profession=profession,
#         bio=bio,
#         skills=skills,
#         photo=photo_path
#     )

# if __name__ == '__main__':
#     app.run(debug=False)

from app import create_app
app = create_app()
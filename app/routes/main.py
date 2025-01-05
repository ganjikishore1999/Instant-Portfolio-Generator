from flask import redirect, render_template, request, Blueprint, url_for

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')
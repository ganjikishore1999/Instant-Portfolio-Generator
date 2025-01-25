import os
import shutil
import json
from flask import (
    Blueprint, 
    flash,
    url_for, 
    render_template, 
    redirect, 
    request
)
from flask_login import login_required, current_user

from ..models import User, db
from app.config import (
    TEMPLATES_HTML_CONFIG_JSON, 
    PORTFOLIO_DATA_DIR,
    UPLOAD_FILES_DIR
)
from app.functions import create_portfolio_config_json

portfolio_bp = Blueprint(
    'portfolio', 
    __name__, 
    template_folder='templates', 
    url_prefix="/portfolio"
)

@portfolio_bp.route('/', methods=['GET', 'POST'])
@login_required
def generate_portfolio():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(request.files)
        print(data)
        portfolio_json =  create_portfolio_config_json(portfolio_data=data)
        base_portfolio_dir = f"{str(os.getcwd())}{PORTFOLIO_DATA_DIR}"
        print(base_portfolio_dir)
        os.makedirs(base_portfolio_dir, exist_ok=True)
        portfolio_data_file_path = f"{base_portfolio_dir}/{current_user.username}.json"
        with open(portfolio_data_file_path, 'w') as file:
            json.dump(portfolio_json, file)

        flash("Portfolio has been created successfully...!", 'success')
        return redirect(url_for('portfolio.generate_portfolio'))
    return render_template('portfolio.html')

@portfolio_bp.route("/view/<string:user_name>", methods=['GET'])
def view_portfolio(user_name):
    if user_name:
        base_dir = str(os.getcwd())
        print(base_dir)
        portfolio_data_file_path = f"{base_dir}{PORTFOLIO_DATA_DIR}/{user_name}.json"
        print(portfolio_data_file_path)
        if os.path.exists(path=portfolio_data_file_path):
            with open(portfolio_data_file_path, 'r') as file:
                data = json.load(file)
    
            return render_template(
                TEMPLATES_HTML_CONFIG_JSON[data['template_name']],
                **data
            )
        else:
            flash("Portfolio not found!", "error")
            return redirect(url_for('main.home_page'))
    else:
        flash("Please provide username to view your portfolio...", "error")
        return redirect(url_for('main.home_page'))


@portfolio_bp.route("/delete/<string:user_name>", methods=['GET'])
@login_required
def delete_portfolio(user_name: str):
    if user_name:
        user_exist = User.query.filter_by(username=user_name).first()
        if not user_exist:
            flash("Portfolio cannot be deleted!", 'error')
            return redirect(
                url_for('main.home_page')
            )
        base_dir = str(os.getcwd())
        print(base_dir)
        portfolio_data_file_path = f"{base_dir}{PORTFOLIO_DATA_DIR}/{user_name}.json"
        print(portfolio_data_file_path)
        uploads_path =  f'{base_dir}/app{UPLOAD_FILES_DIR.format(user_name    =user_name)}'
        print(uploads_path)
        if os.path.exists(uploads_path) and os.path.isdir(uploads_path):
            try:
                shutil.rmtree(uploads_path)
                print("uploades deleted.....")
            except Exception as e:
                print(f"Error occured while deleting uploads..... Error: {str(e)}")
        else:
            print(f"There are no uploads to delete.")
        if os.path.exists(path=portfolio_data_file_path):
            os.remove(portfolio_data_file_path)    
            flash("Portfolio deleted successfully.......!", 'success')
            return redirect(url_for('main.home_page'))
        else:
            flash("Portfolio not found!", "error")
            return redirect(url_for('main.home_page'))
    else:
        flash("Please provide username to delete your portfolio...", "error")
        return redirect(url_for('main.home_page'))

@portfolio_bp.route("/edit/<string:user_name>", methods=['GET'])
def update_portfolio(user_name: str):
    if user_name:
        user_exist = User.query.filter_by(username=user_name).first()
        if not user_exist:
            flash("Portfolio not found....!", 'error')
            return redirect(
                url_for('main.home_page')
            )
        base_dir = str(os.getcwd())
        print(base_dir)
        portfolio_data_file_path = f"{base_dir}{PORTFOLIO_DATA_DIR}/{user_name}.json"
        print(portfolio_data_file_path)
        if os.path.exists(path=portfolio_data_file_path):
            return render_template('edit_portfolio.html')
        else:
            flash("Portfolio not found!", "error")
            return redirect(url_for('main.home_page'))
    else:
        flash("Please provide username to update your portfolio...", "error")
        return redirect(url_for('main.home_page'))

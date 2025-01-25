#data = {'template': 'technical', 'full-name': 'maniram', 'dob': '2025-01-01', 'email': 'mani@gmail.com', 'phone': '8919547891', 'about-me': 'something about maniram', 'skill_1': 'HTML', 'skill_2': 'CSS', 'certificate_name_1': 'HTML5', 'certificate_desc_1': 'Completed HTML5 certification from Simplilearn', 'certificate_name_2': 'CSS', 'certificate_desc_2': 'Completed CSS certification from Simplilearn platform', 'project_name_1': 'Personal Portfolio', 'project_desc_1': 'This project is just to showcase my personal portfolio to others.', 'project_name_2': 'TO Do list', 'project_desc_2': "This will maintain the user's To Do list which will be usefull to user to have a track of their tasks to be done.", "institution-name": "Olive mount global school", "standard": "7"}
import os
from flask_login import current_user
from flask import request

from .config import ALLOWED_FILE_EXTENSIONS, UPLOAD_FILES_DIR

curr_working_dir = str(os.getcwd())

def create_portfolio_config_json(portfolio_data: dict) -> dict:
    portfolio_json = {}
    portfolio_json["template_name"] = portfolio_data["template"]
    portfolio_json["name"] = portfolio_data["full-name"]
    portfolio_json["institution_name"] = portfolio_data["institution-name"]
    portfolio_json["standard"] = portfolio_data["standard"]
    portfolio_json["about"] = portfolio_data["about-me"]
    portfolio_json["contact_details"] = {
        "email": portfolio_data["email"],
        "phone": portfolio_data["phone"]
    }
    if portfolio_data["template"].lower() == 'technical':
        portfolio_json["skills"] = []
        portfolio_json["certifications"] = []
        portfolio_json["projects"] = []

        for key,value in portfolio_data.items():
            if key.startswith("skill_") and value:
                portfolio_json["skills"].append(value)
            elif key.startswith("certificate_name_") and value:
                cert_index = key.split('_')[-1]

                portfolio_json["certifications"].append(
                    {
                        "certificate_name": value,
                        "certificate_description": portfolio_data[f"certificate_desc_{str(cert_index)}"]
                    }
                )
            elif key.startswith("project_name_") and value:
                proj_index = key.split('_')[-1]
                portfolio_json["projects"].append(
                    {
                        "project_name": value,
                        "project_description": portfolio_data[f"project_desc_{str(proj_index)}"]
                    }
                )
    elif portfolio_data["template"].lower() == 'artistic':
        portfolio_json['profile_pic_url'] = process_upload_file(
            file_key='profile-pic',
            key='profile_pic'
        )
        portfolio_json['artworks'] = []
        for key,value in portfolio_data.items():
            if key.startswith('art_name_') and value:
                art_index = key.split('_')[-1]
                portfolio_json['artworks'].append(
                    {
                        "title": value,
                        "image_url": process_upload_file(
                            file_key=f'image_url_{art_index}',
                            key=key
                        ),
                        "description": portfolio_data[f'art_desc_{art_index}']
                    }
                )

    return portfolio_json

def allowed_file(filename):
    """Check if the uploaded file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

def process_upload_file(file_key: str, key: str):
    file = request.files[file_key]
    if file.filename == '':
        raise ValueError("please select a file.....!")

    if file and allowed_file(filename=file.filename):
        file_name = f"{key}.{(file.filename).rsplit('.', 1)[1]}"
        sub_path = UPLOAD_FILES_DIR.format(
            user_name=current_user.username
        )
        upload_file_path = f'{curr_working_dir}/app{sub_path}'
        os.makedirs(upload_file_path, exist_ok=True)
        print(file_name)
        print(upload_file_path)
        file.save(f'{upload_file_path}/{file_name}')
        return f'{sub_path}/{file_name}'
    raise ValueError("Something went wrong during file processing......!")
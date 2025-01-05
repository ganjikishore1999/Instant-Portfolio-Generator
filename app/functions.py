#data = {'template': 'technical', 'full-name': 'maniram', 'dob': '2025-01-01', 'email': 'mani@gmail.com', 'phone': '8919547891', 'about-me': 'something about maniram', 'skill_1': 'HTML', 'skill_2': 'CSS', 'certificate_name_1': 'HTML5', 'certificate_desc_1': 'Completed HTML5 certification from Simplilearn', 'certificate_name_2': 'CSS', 'certificate_desc_2': 'Completed CSS certification from Simplilearn platform', 'project_name_1': 'Personal Portfolio', 'project_desc_1': 'This project is just to showcase my personal portfolio to others.', 'project_name_2': 'TO Do list', 'project_desc_2': "This will maintain the user's To Do list which will be usefull to user to have a track of their tasks to be done.", "institution-name": "Olive mount global school", "standard": "7"}

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
    return portfolio_json

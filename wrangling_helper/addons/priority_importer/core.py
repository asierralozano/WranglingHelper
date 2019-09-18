from wrangling.core.utils import get_excel_data, decode_json
import os


def extract_priority_info(priority_excel):
    info = list()
    excel_dataframe = get_excel_data(priority_excel)
    for row in excel_dataframe.itertuples():
        login = getattr(row, "Login")
        shot = getattr(row, "Shot")
        priority = getattr(row, "Priority")
        info.append({
            "login":login, 
            "shot":shot, 
            "priority":priority
        })
    return info


def generate_priority_rules(priority_excel):
    extracted_info = extract_priority_info(priority_excel)
    priorities_template = decode_json(os.path.join(os.path.dirname(__file__), "priority_template.json"))
    for rule in extracted_info:
        rule_info = {"rule":{"rules":[], "options":{}, "tags":[]}, "info":{}}
        login = rule.get("login")
        shot = rule.get("shot")
        priority = rule.get("priority")

        rule_info["info"]["login"] = login
        rule_info["info"]["shot"] = shot

        user_rule = ["User", "is", login, False]
        shot_rule = ["Name", "contains", shot, False]
        pool_rule = ["Pool", "is", "nukejob", False]

        rule_info["rule"]["rules"].append(user_rule)
        rule_info["rule"]["rules"].append(shot_rule)
        rule_info["rule"]["rules"].append(pool_rule)

        options = priorities_template.get(str(priority))
        rule_info["rule"]["options"] = options

        rule_info["rule"]["tags"].append(("Priority{}".format(priority), "#77dd77"))
        yield rule_info



    



if __name__ == "__main__":
    priority_excel = "C:/Users/asierra/Downloads/priority.xlsx"
    excel_dataframe = extract_priority_info(priority_excel)
    excel_dataframe        
'''
Author: CT
Date: 2023-05-10 09:49
LastEditors: CT
LastEditTime: 2023-05-18 20:58
'''

import json
import os
import argparse
from tqdm import tqdm

# load json file
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# analysis json file
def analysis_json(data):
    city_List = []
    title_List = []
    question_List = []
    answer_List = []

    if type(data) is list:
        data = {"": data}
        
    for city_info, city_data in data.items():
        for each_issue_data in city_data:
            for issue_title, issue_items in each_issue_data.items():
                city_List.append(city_info)
                title_List.append(issue_title)
                issue_question_List = []
                issue_answer_List = []
                
                if type(issue_items) is dict:
                    issue_items = [issue_items]
                
                for item_Dict in issue_items:
                    for question, answer in item_Dict.items():
                        issue_question_List.append(question)
                        issue_answer_List.append(answer)
                
                question_List.append(issue_question_List)
                answer_List.append(issue_answer_List)
        
    return city_List, title_List, question_List, answer_List

# prompt
def prompt(city_info, title, question, answer):
    if answer in ["无",""]:
        prompt_str = "对于{}的{}这个事项，{}这个问题暂时没有相关答案。".format(city_info, title, question)
    elif answer in ["下载","操作"]:
        prompt_str = ""
    else:
        prompt_str = "对于{}的{}这个事项，{}这个问题的答案是{}。".format(city_info, title, question, answer)
    return prompt_str

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_root_path', type=str, help='json root file path')
    args = parser.parse_args()
    args.json_root_path = "/home/ct/文档/Code/Prompt/SourceData"
    # walk through json root path
    for root, _, files in os.walk(args.json_root_path):
        # filter json file
        for file in tqdm(files):
            if not file.endswith(".json"):
                continue
            json_path = os.path.join(root, file)
            
            txt_root_path = os.path.dirname(json_path).replace("SourceData", "OutTxtData")
            if not os.path.exists(txt_root_path):
                os.makedirs(txt_root_path)
            txt_path = os.path.join(txt_root_path, os.path.basename(json_path).replace(".json", ".txt"))

            # load json file
            data = load_json(json_path)
            # analysis json file
            city_List, title_List, question_List, answer_List = analysis_json(data)
            # write to txt file
            with open(txt_path, 'w', encoding='utf-8') as f:
                for issue_index in range(len(title_List)):
                    title = title_List[issue_index]
                    city_info = city_List[issue_index]
                    for question_index in range(len(question_List[issue_index])):
                        question = question_List[issue_index][question_index]
                        answer = answer_List[issue_index][question_index]
                        prompt_str = prompt(city_info, title, question, answer)
                        if prompt_str != "":
                            f.write(prompt_str + "\n")
                        # print(prompt_str)
            
                f.close()
        print("Done!")


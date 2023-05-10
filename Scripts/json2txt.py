'''
Author: CT
Date: 2023-05-10 09:49
LastEditors: CT
LastEditTime: 2023-05-10 10:41
'''

import json
import os
import argparse

# load json file
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# analysis json file
def analysis_json(data):
    title_List = []
    question_List = []
    answer_List = []
    for each_issue_data in data:
        for issue_title, issue_items in each_issue_data.items():
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
        
    return title_List, question_List, answer_List

# prompt
def prompt(title, question, answer):
    if answer == "无" or answer == "":
        prompt_str = "对于{}这个事项，{}这个问题暂时没有相关答案。".format(title, question)
    else:
        prompt_str = "对于{}这个事项，{}这个问题的答案是{}。".format(title, question, answer)
    return prompt_str

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_path', type=str, help='json file path')
    args = parser.parse_args()
    json_path = args.json_path
    
    # json_path = os.path.abspath(r"SourceData/Json/1_reduce.json")
    txt_root_path = os.path.dirname(json_path).replace("SourceData", "OutTxtData")
    if not os.path.exists(os.path.dirname(txt_root_path)):
        os.makedirs(os.path.dirname(txt_root_path))
    txt_path = os.path.join(txt_root_path, os.path.basename(json_path).replace(".json", ".txt"))

    # load json file
    data = load_json(json_path)
    # analysis json file
    title_List, question_List, answer_List = analysis_json(data)
    # write to txt file
    with open(txt_path, 'w', encoding='utf-8') as f:
        for issue_index in range(len(title_List)):
            title = title_List[issue_index]
            for question_index in range(len(question_List[issue_index])):
                question = question_List[issue_index][question_index]
                answer = answer_List[issue_index][question_index]
                prompt_str = prompt(title, question, answer)
                f.write(prompt_str + "\n")
                print(prompt_str)
    
        f.close()
        print("Done!")


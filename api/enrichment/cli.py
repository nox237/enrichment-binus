import os, re
from termcolor import colored
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

def extract_filename(filename):
    return filename.split('.')[0]

def print_get_assignment(datas):
    print('[!] Printing all assignment in enrichment.binus.ac.id')
    x = PrettyTable()
    x.field_names = ["Assignment Title", "Month", "Assignment Due Date", "Assignment Status"]
    for data in datas['data']:
        x.add_row([data['assignmentTitle'], data['assignmentMonthDesc'], data['assignmentDueDate'].replace("T",", "), data['assignmentStatusName'] if data['assignmentStatusName'] != "" else "-"])
    print(x)
    print()

def print_get_monthly(datas, months):
    month_dictionary = {}
    for month in months['data']:
        month_dictionary[month['month']] = {"note":"-", "statusName":"-"}
    for data in datas:
        month_dictionary[data['monthString']]["note"] = data["note"]
        month_dictionary[data['monthString']]["statusName"] = data['statusName']
    
    print('[!] Printing all monthly report in enrichment.binus.ac.id')
    x = PrettyTable()
    x.field_names = ["Month", "Note", "Uploaded Date"]
    for month in month_dictionary:
        x.add_row([month, month_dictionary[month]['note'], month_dictionary[month]['statusName']])
    print(x)
    print()

def print_get_logbook(datas):
    print('[!] Printing all logbook in chosen month in enrichment.binus.ac.id')
    x = PrettyTable()
    x.field_names = ["Date", "ClockIn", "ClockOut", "Acceptance"]
    for data in datas['data']:
        soup = bs(data['acceptance'], "html.parser")
        span_list = [ span.getText() for span in soup.find_all("span")]
        if len(span_list) > 1:
            x.add_row([data['date'].split('T')[0], data['clockIn'], data['clockOut'], colored(span_list[0], "green") if "Approved" in span_list[0] else colored(span_list[0], "yellow")])
            x.add_row(["", "", "", colored(span_list[1], "green") if "Approved" in span_list[1] else colored(span_list[1], "yellow")])
        else:
            x.add_row([data['date'].split('T')[0], data['clockIn'], data['clockOut'], span_list[0] if len(span_list) == 1 else ""])
    print(x)
    print()

def get_all_local_logbook_data(path_file):
    files = os.listdir(path_file)
    contents = []
    for file in files:
        with open(path_file + '/' + file) as f:
            content = []
            temp_activity_name = ""
            for i in f.readlines():
                temp_content = i.strip()
                if temp_content != "":
                    if re.match(r"Activity:(.*)", temp_content):
                        temp_activity_name = temp_content.split(':')[1]
                    else:
                        content.append(temp_content)
            contents.append((extract_filename(file), content, temp_activity_name))
    return sorted(contents, key=lambda x: x[0])

def processed_list_data(list_data, clockIn, clockOut, flagActive, flagActiveName):
    new_dictionary_list = []
    for data in list_data:
        temp_dictionary = {
            "model[Date]": data[0]+"T00:00:00",
            "model[Activity]": data[2],
            "model[ClockIn]": clockIn,
            "model[ClockOut]": clockOut,
            "model[Description]": '\n'.join(data[1]), 
            f"model[{flagActiveName}]": flagActive
        }
        new_dictionary_list.append(temp_dictionary)
    return new_dictionary_list
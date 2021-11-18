from termcolor import colored
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

def print_get_assignment(datas):
    x = PrettyTable()
    x.field_names = ["Assignment Title", "Month", "Assignment Due Date", "Assignment Status"]
    for data in datas['data']:
        x.add_row([data['assignmentTitle'], data['assignmentMonthDesc'], data['assignmentDueDate'].replace("T",", "), data['assignmentStatusName'] if data['assignmentStatusName'] != "" else "-"])
    print(x)

def print_get_monthly(datas, months):
    month_dictionary = {}
    for month in months['data']:
        month_dictionary[month['month']] = {"note":"-", "statusName":"-"}
    for data in datas:
        month_dictionary[data['monthString']]["note"] = data["note"]
        month_dictionary[data['monthString']]["statusName"] = data['statusName']
    
    x = PrettyTable()
    x.field_names = ["Month", "Note", "Uploaded Date"]
    for month in month_dictionary:
        x.add_row([month, month_dictionary[month]['note'], month_dictionary[month]['statusName']])
    print(x)

def print_get_logbook(datas):
    x = PrettyTable()
    x.field_names = ["Date", "ClockIn", "ClockOut", "Acceptance"]
    for data in datas['data']:
        soup = bs(data['acceptance'], "html.parser")
        span_list = [ span.getText() for span in soup.find_all("span")]
        x.add_row([data['date'].split('T')[0], data['clockIn'], data['clockOut'], colored(span_list[0], "green") if "Approved" in span_list[0] else colored(span_list[0], "yellow")])
        x.add_row(["", "", "", colored(span_list[1], "green") if "Approved" in span_list[1] else colored(span_list[1], "yellow")])
    print(x)

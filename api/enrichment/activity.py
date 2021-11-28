import json
from bs4 import BeautifulSoup as bs

ACTIVITY_ENRICHMENT_URL = "https://enrichment.apps.binus.ac.id/Dashboard/Student/IndexStudentDashboard"
ACTIVITY_SSOTOACTIVITY_URL = "https://enrichment.apps.binus.ac.id/Login/Student/SSOToActivity"
ASSIGNMENT_URL = "https://activity-enrichment.apps.binus.ac.id/Assignment/GetAssignment"
LOGBOOK_URL = "https://activity-enrichment.apps.binus.ac.id/LogBook/GetLogBook"
MONTHLY_URL = "https://activity-enrichment.apps.binus.ac.id/LogBook/GetMonths"
MONTHLY_REPORT_URL = "https://activity-enrichment.apps.binus.ac.id/MonthlyReport/GetMonthlyReportList"
POST_LOGBOOK_URL = "https://activity-enrichment.apps.binus.ac.id/LogBook/StudentSave"

def extract_unempty_data(data):
    list_date = {}
    for d in data:
        if d['id'] != '00000000-0000-0000-0000-000000000000' and d['activity'] != "OFF":
            list_date[d['date']]=d['id']
    return list_date

MONTHLY_REPORT_UPLOAD_URL = "https://activity-enrichment.apps.binus.ac.id/MonthlyReport/SaveMonthly"
MONTHLY_REPORT_DELETE_URL = "https://activity-enrichment.apps.binus.ac.id/MonthlyReport/DeleteMonthlyReport"

def get_enrichment(session, response):
    semester = []
    soup = bs(response.text, "html.parser")
    for select in soup.find_all("select",{'id':'Semester'}):
        semester.append({'value':select.find('option').get('value'), 'name':select.find('option').getText()})
    
    idx = 0
    if len(semester) > 1:
        print('[!] Select Semester:')
        for idx,sem in enumerate(semester):
            print(f'[{idx}] {sem["name"]}')
        idx = int(input('[!] Choose idx = '))

    data = {'Strm':semester[idx]['value']}
    response = session.post(ACTIVITY_ENRICHMENT_URL, data=data)
    response = session.get(ACTIVITY_SSOTOACTIVITY_URL, allow_redirects=True)
    return response

def get_assignment(session):
    # 0 for all month
    data = {'month': 0}
    response = session.post(ASSIGNMENT_URL, data=data)
    return json.loads(response.text)

def get_logbook(session, monthly_data, input_idx):
    data = {'logBookHeaderID':monthly_data['data'][input_idx]['logBookHeaderID']}
    response = session.post(LOGBOOK_URL, data=data)
    return json.loads(response.text)

def get_monthly(session):
    response = session.get(MONTHLY_URL)
    return json.loads(response.text)

def get_month_report(session):
    response = session.get(MONTHLY_REPORT_URL)
    return json.loads(response.text)

# payload month, note, reportfile(binary)
def upload_monthly_report(session):
    pass
    
def post_logbook_report(session, list_data, logbook_data, logbookheaderid):
    response_list = []
    list_unempty_data = extract_unempty_data(logbook_data['data'])
    for lstdata in list_data:
        post_data = {
            "model[ID]": "00000000-0000-0000-0000-000000000000",
            "model[LogBookHeaderID]": logbookheaderid,
            "model[Date]": lstdata['model[Date]'],
            "model[Activity]": lstdata['model[Activity]'],
            "model[ClockIn]": lstdata['model[ClockIn]'],
            "model[ClockOut]": lstdata['model[ClockOut]'],
            "model[Description]": lstdata['model[Description]'], 
            "model[flagjulyactive]": lstdata['model[flagjulyactive]'],
        }
        if lstdata['model[Date]'] in list_unempty_data:
            post_data["model[ID]"] =list_unempty_data[lstdata['model[Date]']]
        response = session.post(POST_LOGBOOK_URL, data=post_data)
        response_list.append((response.status_code, response.text, lstdata['model[Date]']))
    return response_list

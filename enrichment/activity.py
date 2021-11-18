import json
from bs4 import BeautifulSoup as bs

ACTIVITY_ENRICHMENT_URL = "https://enrichment.apps.binus.ac.id/Dashboard/Student/IndexStudentDashboard"
ACTIVITY_SSOTOACTIVITY_URL = "https://enrichment.apps.binus.ac.id/Login/Student/SSOToActivity"
ASSIGNMENT_URL = "https://activity-enrichment.apps.binus.ac.id/Assignment/GetAssignment"
LOGBOOK_URL = "https://activity-enrichment.apps.binus.ac.id/LogBook/GetLogBook"
MONTHLY_URL = "https://activity-enrichment.apps.binus.ac.id/LogBook/GetMonths"
MONTHLY_REPORT_URL = "https://activity-enrichment.apps.binus.ac.id/MonthlyReport/GetMonthlyReportList"

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
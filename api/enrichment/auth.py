from bs4 import BeautifulSoup as bs

LOGIN_PAGE_URL="https://enrichment.apps.binus.ac.id/Login/Student/Login"
LOGIN_API_URL="https://enrichment.apps.binus.ac.id/Login/Student/DoLogin"

def login(session, username, password):
    """Login to enrichmetn page and return response output from requests"""
    response = session.get(LOGIN_PAGE_URL)
    soup = bs(response.text, "html.parser")
    input_list = soup.find_all("input")

    data = {}
    for tag in input_list:
        data[tag['name']] = tag.get('value')
    
    data['login.Username'] = username
    data['login.Password'] = password

    response = session.post(LOGIN_API_URL,data=data)
    soup2 = bs(response.text, "html.parser")
    if soup2.find("span",{"class":"alert is-error"}):
        print("Error authentication")
        return "Error"
    return response
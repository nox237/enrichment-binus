import requests
import stdiomask
from api.enrichment import auth
from api.enrichment import activity
from api.enrichment import cli

if __name__ == "__main__":
    session = requests.Session()
    username = input("[!] Username Binusmaya : ")
    password = stdiomask.getpass(mask="", prompt="[!] Password Binusmaya : ")
    response = auth.login(session, username, password)
    if response == "Error":
        exit(1)
    
    activity.get_enrichment(session, response)
    cli.print_get_assignment(activity.get_assignment(session))
    cli.print_get_monthly(activity.get_month_report(session), activity.get_monthly(session))
    cli.print_get_logbook(activity.get_logbook(session, activity.get_monthly(session), 0))
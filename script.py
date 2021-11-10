import requests
from enrichment import auth
from enrichment import activity
from enrichment import cli

if __name__ == "__main__":
    session = requests.Session()
    response = auth.login(session)
    if response == "Error":
        exit(1)
    
    activity.get_enrichment(session, response)
    cli.print_get_assignment(activity.get_assignment(session))
    cli.print_get_monthly(activity.get_month_report(session), activity.get_monthly(session))
    cli.print_get_logbook(activity.get_logbook(session, activity.get_monthly(session), 0))
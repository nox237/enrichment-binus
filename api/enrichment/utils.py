import requests

ENRICHMENT_ENDPOINT = "http://enrichment.apps.binus.ac.id/Login"

def check_status(session):
    print(f'[!] Checking {ENRICHMENT_ENDPOINT} connection')
    try:
        response = session.get(ENRICHMENT_ENDPOINT, timeout=15)
        return True
    except:
        return False
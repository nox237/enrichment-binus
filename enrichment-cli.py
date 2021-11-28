import requests
import stdiomask
import sys, getopt
from api.enrichment import auth
from api.enrichment import activity
from api.enrichment import cli
from api.enrichment import utils
from termcolor import colored

if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    pass
elif sys.platform == "darwin":
    # MAC OS X
    pass
elif sys.platform == "win32" or sys.platform == "win64":
    # Windows 32-bit or Windows 64-bit
    import colorama
    colorama.init()

def banner():
    print("  _____            _      _                          _        ____  _                 ")
    print(" | ____|_ __  _ __(_) ___| |__  _ __ ___   ___ _ __ | |_     | __ )(_)_ __  _   _ ___ ")
    print(" |  _| | '_ \| '__| |/ __| '_ \| '_ ` _ \ / _ \ '_ \| __|____|  _ \| | '_ \| | | / __|")
    print(" | |___| | | | |  | | (__| | | | | | | | |  __/ | | | ||_____| |_) | | | | | |_| \__ \\")
    print(" |_____|_| |_|_|  |_|\___|_| |_|_| |_| |_|\___|_| |_|\__|    |____/|_|_| |_|\__,_|___/\n\n")


def help():
    print("COMMAND:")
    print(" -h               : help command")
    print(" --username       : username for binus account")
    print(" --password       : password for binus account")
    print(" --path-logbook   : path for logbook data")
    print(" --current-month  : current month for listing")
    print(" --month          : month for listing")
    print(" --clockIn        : Clock In for Intern")
    print(" --clockOut        : Clock Out for Intern")
    print(" -p / --post      : type of post (Logbook)")
    print(" -t / --type      : type of listing (All, Logbook, Assignment, MonthlyReport)", end="\n\n")

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hp:t:", ["post=", "type=", "path-logbook=", "username=", "password=", "month=", "clockIn=", "clockOut="])
    POST_TYPE = ""
    TYPE_LIST = ""
    LOGBOOK_PATH = ""
    USERNAME = ""
    PASSWORD = ""
    FLAGACTIVE = "false"
    FLAGACTIVENAME = "flagjulyactive"
    CLOCKIN = ""
    CLOCKOUT = ""
    MONTH = -1

    banner()
    for opt, val in opts:
        if opt in ("-h"):
            help()
            exit(0)
        elif opt in ("-p", "--post"):
            POST_TYPE = val.lower()
        elif opt in ("-t", "--type"):
            TYPE_LIST = val.lower()
        elif opt in ("--path-logbook"):
            LOGBOOK_PATH = val
        elif opt in ("--username"):
            USERNAME = val
        elif opt in ("--password"):
            PASSWORD = val
        elif opt in ("--month"):
            MONTH = val
        elif opt in ("--clockIn"):
            CLOCKIN = val
        elif opt in ("--clockOut"):
            CLOCKOUT = val

    session = requests.Session()
    if utils.check_status(session) == True:
        print(colored('[!] Script can connect to enrichment.apps.binus.ac.id website', 'green'))
    else:
        print(colored('[!] Cannot connect to enrichment.apps.binus.ac.id - You might need to check the website from browser', "red"))
        exit(1)
    if USERNAME == "":
        USERNAME = input("[!] Username Binusmaya : ")
    else:
        print(f'[!] Using username {USERNAME} for login into enrichment.apps.binus.ac.id')
    if PASSWORD == "":
        PASSWORD = stdiomask.getpass(mask="", prompt="[!] Password Binusmaya : ")
    else :
        print('[!] Using password from parameter script')
    print('[!] Authenticating to enrichment.apps.binus.ac.id')
    
    response = auth.login(session, USERNAME, PASSWORD)
    if response == "Error":
        print(colored('[-] Unable login to enrichment.apps.binus.ac.id', 'red'))
        exit(1)
    print(colored('[+] Successful login to enrichment.apps.binus.ac.id', 'green'))

    print('\n[+] Getting enrichment session...')
    activity.get_enrichment(session, response)
    print('[+] Successful getting the enrichment session\n')

    months = activity.get_monthly(session)
    if MONTH == -1:
        while (int(MONTH) < 0 or int(MONTH) > len(months['data'])) and MONTH != "q":
            print('[!] Choose month for generating (enter q to quit):')
            for idx,month in enumerate(months['data']):
                if month['isCurrentMonth'] == True:
                    print(f'[{idx}] ' + colored(month['month'], "yellow"))
                else:
                    print(f'[{idx}] ' + month['month'])
            MONTH = input('>>> ')
        if MONTH == "q":
            print("[!] Exiting Program")
            exit(1)
        else:
            MONTH = int(MONTH)
    else:
        MONTH = int(MONTH)
        print(f"[!] Using month {months['data'][MONTH]['month']} for the enrichment month")

    if TYPE_LIST == "" and POST_TYPE == "":
        print()
        choice = -1
        while choice != 0 and choice != 1:
            choice = int(input("[!] Please input [0] listing or [1] post data?\n>>> "))
        if choice == 0:
            while TYPE_LIST not in ("all", "logbook", "assignment", "monthlyreport"):
                TYPE_LIST = input("[!] Please input type (all, logbook, assignment, monthlyreport)\n>>> ").lower()
        else:
            while POST_TYPE not in ("logbook"):
                POST_TYPE = input("[!] Please input post (logbook)\n>>> ").lower()
        print()

    if TYPE_LIST in ("all", "logbook", "assignment", "monthlyreport") and POST_TYPE == "":
        if TYPE_LIST == "all":
            cli.print_get_logbook(activity.get_logbook(session, months, int(MONTH)))
            cli.print_get_assignment(activity.get_assignment(session))
            cli.print_get_monthly(activity.get_month_report(session), months)
        if TYPE_LIST == "logbook":
            cli.print_get_logbook(activity.get_logbook(session, months, int(MONTH)))
        if TYPE_LIST == "assignment":
            cli.print_get_assignment(activity.get_assignment(session))
        if TYPE_LIST == "monthlyreport":
            cli.print_get_monthly(activity.get_month_report(session), months)
    elif POST_TYPE in ("logbook"):
        if POST_TYPE == "logbook":
            print('[!] Preparing to ')
            if LOGBOOK_PATH == "":
                print('[!] Please enter Logbook Path')
                LOGBOOK_PATH = input("> ")
            raw_list_data = cli.get_all_local_logbook_data(LOGBOOK_PATH)

            if CLOCKIN == "":
                print('[!] Please enter ClockIn number (example: 09:00 am)')
                CLOCKIN = input("> ")
            if CLOCKOUT == "":
                print('[!] Please enter ClockOut number (example: 09:00 pm)')
                CLOCKOUT = input("> ")
            
            print('[!] Sending all post data into enrichment.apps.binus.ac.id (This process might taking a minutes..)')
            list_data = cli.processed_list_data(raw_list_data, CLOCKIN, CLOCKOUT, FLAGACTIVE, FLAGACTIVENAME)
            print(activity.post_logbook_report(session, list_data, activity.get_logbook(session, months, MONTH), months['data'][MONTH]['logBookHeaderID']))
            print('[!] Succesfully post all logbook report')
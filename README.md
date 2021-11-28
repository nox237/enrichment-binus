# Enrichment Binus Scraper

## Description

This repository is for Binusian where they can use the python script for printing all the logbook, assignment, and monthly report inside the enrichment.apps.binus.ac.id website.

## To Do List

- [x] Create Authentication Function
- [x] Create View Function for request API Request
- [x] Create Insert Logbook Function for API Request
- [x] Create Django REST API serving the API Endpoint
- [ ] Create Insert Monthly Report and Assignment from API Request

## How to use

For the program, user can use **cli** version by executing the *enrichment-cli.py* or using the **django-rest-framework** version. Before executing it, the user can run to download the required library:

```bash
python3 -m pip install -r requirements.txt
```

Then the user can run the cli version or the django-rest-framework version

## API Description [ DJANGO REST FRAMEWORK ]

| endpoints | required data |
|-----------|---------------|
| api/list-monthly | username, password |
| api/list-logbook | username, password, month |
| api/list-assignment | username, password |
| api/list-monthly-report | username, password|
| api/post-logbook | username, password, month_idx, logbookheaderid, logbook |

Notes:

- logbookheaderid inside the api/post-logbook request data can be accessed from the return response of api/list-monthly which also depends on the chosen month_idx in the repsonse

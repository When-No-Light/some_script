# Project Title

Recruitment task - backend intership

## Description

The script allows you to get some information from the NBE API.

## Getting Started

### Dependencies

* Python 3.9

### Installing

* open project folder and create new env with command `virtualenv env`
* activate env `env\Scripts\activate`
* install dependencies `pip install -r requirements.txt`

### Example commands

* `python script.py grouped-teams` - get all teams and group them by division
* `python script.py players-stats --name Michael` - get players with a specific name (first_name or last_name) who is the tallest and another one who weight the most (print height and weight in metric system)
* python script.py teams-stats --season 2017 --output csv - get csv file with information about the game of different teams in a particular season
(options: csv, json, sqlite, stdout(default)).



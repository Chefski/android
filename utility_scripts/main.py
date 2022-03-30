from msilib.schema import DuplicateFile
from multiprocessing.spawn import prepare
from modules.delta_email_parser import main as parse_mails
from modules.merge_new_drawables import main as merge_drawables
from modules.create_updated_appfilters import main as create_updated_appfilters
from modules.svg_conversion import main as convertSVG
from modules.move_outdated_drawables import main as move_outdated_drawables
from sys import argv
import json

# make sure to run "pip install -r requirements.txt" before running this script

usage = """
Usage:
python (or python3) main.py (update_requests|prepare_release)

update_requests - parses the email folder and updates requests.txt
prepare_release - parses contributions.json, converts svgs to png, renames icons that get demoted to _alt, merges new drawables and updates xml files
"""

# CONSTANTS
CONTRIBUTIONS_PATH = '../contributions.json'
SVG_FOLDER = '../contributed-vectors'
DRAWABLE_PATH = '../app/src/main/res/xml/drawable.xml'
APPFILTER_PATH = '../app/src/main/res/xml/appfilter.xml'
DRAWABLE_CLONE_PATH = '../app/src/main/assets/drawable.xml'
APPFILTER_CLONE_PATH = '../app/src/main/assets/appfilter.xml'
PNG_OUTPUT_FOLDER = '../app/src/main/res/drawable-nodpi'
MAIL_FOLDER = './emails/'
REQUESTS_PATH = '../requests.txt'
UPDATABLE_PATH = '../updatable.txt'
REQUEST_PER_PERSON_LIMIT = 1
MONTHS_LIMIT = 6
KEEP_IF_REQUESTED_MORE_THAN_TIMES = 5


def duplicate_file(source, target):
    with open(source, 'r') as source_file:
        with open(target, 'w') as target_file:
            target_file.write(source_file.read())


def parse_contributions(cotributions_path):
    with open(cotributions_path, 'r') as f:
        data = json.load(f)
        return {
            "new": [x for x in data if x["drawable"] is not None],
            "to_update": [x for x in data if x["update_drawable"] is None],
        }


def update_requests():
    parse_mails(
        MAIL_FOLDER, REQUESTS_PATH, UPDATABLE_PATH, APPFILTER_PATH,
        REQUEST_PER_PERSON_LIMIT, MONTHS_LIMIT,
        KEEP_IF_REQUESTED_MORE_THAN_TIMES)


def prepare_release():
    contributions = parse_contributions(CONTRIBUTIONS_PATH)
    new_drawables = contributions["new"] + [x["new_drawable"]
                                            for x in contributions["to_update"]]
    renamed_drawables = move_outdated_drawables(contributions["to_update"])
    convertSVG(SVG_FOLDER, DRAWABLE_PATH, new_drawables)
    merge_drawables(DRAWABLE_PATH, new_drawables, renamed_drawables)
    duplicate_file(DRAWABLE_PATH, DRAWABLE_CLONE_PATH)
    create_updated_appfilters(APPFILTER_PATH, contributions)
    duplicate_file(APPFILTER_PATH, APPFILTER_CLONE_PATH)


if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == "update_requests":
            update_requests()
        elif argv[1] == "prepare_release":
            prepare_release()
        else:
            print(usage)
    else:
        print(usage)

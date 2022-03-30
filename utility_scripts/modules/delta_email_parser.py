import datetime
from email.parser import BytesParser
from email import policy
from email.utils import parsedate
from datetime import date
from time import mktime
import glob
import re

apps = {}  # Dictionary of requested apps and according info
addresses = {}  # E-Mail addresses with number of requests
appInfoQuery = re.compile(
    r'(?P<Name>[\w\d\@\?\/\(\)\!]+)\s?(?P<ComponentInfo>[\w\.\/\d]+)\shttps://play\.google\.com/store/apps/details\?id=(?P<PackageName>[\w\.]+)',
    re.M)
eMailQuery = re.compile(r'<(.+)>$')
updatable = []
newApps = []

# Filters to limit backlog
currentDate = date.today()

# Remove people sending more than X requests


def removeGreedy(address, element):
    if address in element['senders']:
        element['count'] = element['count'] - 1
        element['senders'] = [
            x for x in element['senders'] if x is not address]
    return element


def parseExisting(requests_file):
    requestBlockQuery = re.compile(
        r'(?P<Name>.+)\s(?P<ComponentInfo>.+)\shttps:\/\/play.google.com\/store\/apps\/details\?id=.+\sRequested (?P<count>\d+) times\s?(Last requested (?P<requestDate>\d+\.?\d+?))?')
    with open(requests_file, 'r', encoding="utf8") as existingFile:
        contents = existingFile.read()
        existingRequests = re.finditer(requestBlockQuery, contents)
        for req in existingRequests:
            elementInfo = req.groupdict()
            apps[elementInfo['ComponentInfo']] = elementInfo
            apps[elementInfo['ComponentInfo']]['requestDate'] = float(
                elementInfo['requestDate']) if elementInfo['requestDate'] is not None else mktime(currentDate.timetuple())
            apps[elementInfo['ComponentInfo']]['count'] = int(
                elementInfo['count'])
            apps[elementInfo['ComponentInfo']]['senders'] = []


def parseMails(e_mail_folder, request_limit):
    path = e_mail_folder
    if not path.endswith('/'):
        path += '/'

    for mail in glob.glob(path + '*.eml'):
        with open(mail, 'rb') as msg:
            # Convert Message to String
            msg = BytesParser(policy=policy.default).parse(msg)
            parsed = msg.get_body(preferencelist=('plain'))
            # Skip if body is empty
            if parsed is None:
                continue
            emailBody = parsed.get_content()

            # Check if sender exists
            sender = re.search(eMailQuery, msg['From'])
            if sender is None:
                continue

            # check if sender crossed limit
            if sender.groups()[0] not in addresses:
                addresses[sender.groups()[0]] = 1
            elif addresses[sender.groups()[0]] == request_limit:
                print('XXXXXX ---- We have a greedy one: ', sender.groups()[0])
                for key, value in apps.items():
                    value = removeGreedy(sender.groups()[0], value)
                continue
            else:
                addresses[sender.groups()[0]] += 1

            appInfo = re.search(appInfoQuery, emailBody)

            # AppInfo could not automatically be extracted
            if appInfo is None:
                # Search for String appearance of existing ComponentInfos in E-Mail body
                for key, value in apps.items():
                    if key in emailBody:
                        apps[key]['count'] += 1
                        apps[key]['senders'].append(sender.groups()[0])
                        continue
                print(
                    '\n/// The following message could not be handled:\n',
                    emailBody, '\n')
            else:
                tempDict = appInfo.groupdict()
                if tempDict['ComponentInfo'] in apps:
                    apps[tempDict['ComponentInfo']
                         ]['count'] = apps[tempDict['ComponentInfo']]['count'] + 1
                    apps[tempDict['ComponentInfo']]['senders'].append(
                        sender.groups()[0])
                else:
                    tempDict['count'] = 1
                    tempDict['senders'] = [sender.groups()[0]]
                    apps[tempDict['ComponentInfo']] = tempDict
                # Update date of last request
                if 'requestDate' not in apps[
                        tempDict['ComponentInfo']] or apps[
                        tempDict['ComponentInfo']]['requestDate'] < mktime(
                        parsedate(msg['date'])):
                    apps[tempDict['ComponentInfo']]['requestDate'] = mktime(
                        parsedate(msg['Date']))


def diffMonth(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def filterOld(months_limit, min_requests):
    global apps
    apps = {k: v for k, v in apps.items() if v['count'] > min_requests or diffMonth(
            currentDate, datetime.datetime.fromtimestamp(v['requestDate'])) < months_limit}


def separateupdatable(appfilter_file):
    objectBlock = """
{name}
{component}
https://play.google.com/store/apps/details?id={packageName}
Requested {count} times
Last requested {reqDate}
	"""
    with open(appfilter_file, 'r') as appfilter:
        appfilter = appfilter.read()
        for (componentInfo, values) in apps.items():
            componentInfo = componentInfo[:componentInfo.index('/')]
            if appfilter.find(componentInfo) == -1 and ''.join(newApps).find(
                    componentInfo) == -1:
                newApps.append(
                    objectBlock.format(
                        name=values["Name"],
                        component=values["ComponentInfo"],
                        packageName=values["ComponentInfo"][0: values["ComponentInfo"].index('/')],
                        count=values["count"],
                        reqDate=values["requestDate"],))
            elif appfilter.find(componentInfo) != -1 and ''.join(updatable).find(componentInfo) == -1:
                updatable.append(values['Name'] + '\n' +
                                 values['ComponentInfo'] + '\n\n')


def writeOutput(requests_file, updatable_file):
    newListHeader = """-------------------------------------------------------
{totalCount} Requested Apps Pending (Updated {date})
-------------------------------------------------------
"""
    # newList = newListHeader.format( totalCount = len(apps), date = date.today().strftime("%d %m %Y"))
    newList = newListHeader.format(
        totalCount=len(apps),
        date=date.today().strftime("X%d %B %Y").replace("X0", "X").replace(
            "X", ""))
    newList += ''.join(newApps)

    with open(requests_file, 'w', encoding='utf-8') as file:
        file.write(newList)
    if len(updatable):
        with open(updatable_file, 'w', encoding='utf-8') as fileTwo:
            fileTwo.write(''.join(updatable))


def main(e_mail_folder, requests_file, updatable_file, appfilter_file,
         request_limit, months_limit, min_requests):
    parseExisting(requests_file)
    filterOld(months_limit, min_requests)
    parseMails(e_mail_folder, request_limit)
    sorted(apps.values(), key=lambda item: item['count'], reverse=True)
    separateupdatable(appfilter_file)
    writeOutput(requests_file, updatable_file)


if __name__ == "__main__":
    main()

import csv
import sys
from urllib.parse import urlparse
from subprocess import Popen, PIPE

def escape(s):
    return s.replace(" ", "-")\
        .replace("&", "and")\
        .replace("[", "")\
        .replace("]", "")


def format_infos(row):
    username = escape(row[1])
    password = row[3]
    description = (row[0] + "\n" if len(row[0]) > 0 else "") + row[4]
    otp = row[6]

    if len(username) == 0:
        print(row[0] + " " + row[2] + " Empty username!")
        exit()

    return {"username": username, "password": password, "description": description, "otp": otp}


def pass_insert(path, data):
    proc = Popen(['pass', 'insert', '--multiline', path],
                 stdin=PIPE, stdout=PIPE)
    proc.communicate(data.encode('utf8'))
    proc.wait()


result = {}

with open(sys.argv[1], "r") as pbfile:
    next(pbfile)
    pbreader = csv.reader(pbfile, dialect='excel')
    for row in pbreader:
        row[2] = urlparse(row[2]).netloc

        if (len(row[2]) == 0):
            print(row[1] + " no valid URL!")
            exit()

        if row[2] in result:
            result[row[2]].append(format_infos(row))
        else:
            result[row[2]] = [format_infos(row)]

for netloc, entries in result.items():
    for credential in entries:
        path = netloc + "/" + credential["username"]
        if len(credential["password"]) > 0: pass_insert(path + "/password", credential["password"])
        if len(credential["description"]) > 0: pass_insert(path + "/description", credential["description"])
        if len(credential["otp"]) > 0: pass_insert(path + "/otp", credential["otp"])

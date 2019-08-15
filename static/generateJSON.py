
import os
import re
import json
import csv

DEBUG = False

applicants = {}
exclude = ["Harrison Papagianis", "Olivia Ferrel", "Prasad Adiga"]

this_dir, this_filename = os.path.split(__file__)
print(this_dir, this_filename)
directory = os.path.join(this_dir, "submissions")

for item in os.listdir(directory):
    file = re.search("(\\w+ *\\S*)(?=\\.).(png|jpg|pdf|PNG|JPG|PDF)", item)
    if file is not None:
        name = file.group(1)
        type = file.group(2)
        if name not in applicants:
            if name in exclude:
                if DEBUG:
                    print("Excluding applicant %s." % str(name))
                continue
            if DEBUG:
                print("Creating applicant %s." % str(name))
            applicants[name] = {}
        num = len(applicants[name])
        if "pdf" in type.lower():
            applicants[name]["PDF" + str(num)] = {'type': 'static', 'source': "submissions/" + item}
        elif type.lower() in ['jpg', 'png']:
            applicants[name]["Image" + str(num)] = {'type': 'static', 'source': "submissions/" + item}

types = ["youtu", "vimeo"]
with open("submissions/zips/ASU.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        for type in types:
            name = row[3]
            source = None
            if type in row[19]:
                source = row[19]
            elif type in row[20]:
                source = row[20]
            elif type in row[22]:
                source = row[22]
            elif type in row[23]:
                source = row[23]
            elif type in row[25]:
                source = row[25]
            elif type in row[26]:
                source = row[26]
            if source is not None:
                # Verify if the applicant is already in applicants; name is only firstname (last name in row[4] but sometimes row[3] has both first and last)
                for applicant in applicants:
                    if name in applicant:
                        name = applicant
                # Verify applicant exists in dict
                if name not in applicants:
                    if name in exclude:
                        continue
                    applicants[name] = {}

                # Attempt to convert to iframe compatible
                if "//vimeo.com" in source:
                    source = source.replace("//vimeo.com/", "//player.vimeo.com/video/")
                elif "//watch?v=" in source:
                    source = source.replace("//watch?v=", "/embed/")
                    source = re.sub("(&\\S*)", "", source)
                elif "youtu.be" in source:
                    source = source.replace("youtu.be/", "youtube.com/embed/")
                    source = re.sub("(&\\S*)", "", source)

                num = len(applicants[name])
                applicants[name]["Video" + str(num)] = {'type': 'URI', 'source': source}
                if DEBUG:
                    print("Applicant: %s\nSource: %s" % (name, source))

with open('data.json', 'w') as file:
    json.dump(applicants, file)

'''
for type in types:
    applicant = row[3]
    if type in row[19]:
        num = len(applicants[applicant])

        source = row[19]
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[19]}
    elif type in row[20]:
        num = len(applicants[applicant])
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[20]}
    elif type in row[22]:
        num = len(applicants[applicant])
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[22]}
    elif type in row[23]:
        num = len(applicants[applicant])
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[23]}
    elif type in row[25]:
        num = len(applicants[applicant])
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[25]}
    elif type in row[26]:
        if DEBUG:
            print("Applicant: %s\nSource row[26]: %s" % (applicant, row[26]))
        num = len(applicants[applicant])
        applicants[applicant]["Video" + str(num)] = {'type': 'URI', 'source': row[26]}
'''

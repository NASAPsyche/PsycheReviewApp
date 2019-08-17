from flask import Flask, render_template, jsonify, request, json
from jinja2 import Template
from collections import OrderedDict
import os
import re

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


app = Flask(__name__)

# data = json.load(open(os.path.join(app.root_path, "static", "jsonData.json")), object_pairs_hook=OrderedDict)

with open('static/jsonData.json') as file:
  data = json.load(file)

table = Template("""
    {% for row, items in data.items() %}
    <tr>
      <td class="center">
        <input type="checkbox" class="center set" value="{{ row }}">
      </td>
      {% for item in data[row] %}
      <td>
        {% if "Image" in item %}
          {% if data[row][item].type == "URI" %}
          <button class="btn btn-default modalImg" data-toggle="modal" data-target="#selectedImg">
            <img class="tblItems" src="{{ data[row][item].source }}" alt="Card image cap">
          </button>
          {% elif data[row][item].type == "static" %}
          <button class="btn btn-default modalImg" data-toggle="modal" data-target="#selectedImg">
            <img class="tblItems" src="/static/{{data[row][item].source}}" alt="Card image cap">
          </button>
          {% endif %}
        {% elif "Video" in item %}
          {% if data[row][item].type == "URI" %}
          <iframe class="tblItems video" src="{{ data[row][item].source }}" frameborder="0" allow="encrypted-media" allowfullscreen></iframe>
          {% endif %}
        {% elif "PDF" in item %}
          {% if data[row][item].type == "URI" %}
          <embed class="tblItems pdf" src="{{ data[row][item].source }}">
          {% elif data[row][item].type == "static" %}
          <embed class="tblItems pdf" src="/static/{{data[row][item].source}}">
          {% endif %}
          <a class="btn btn-primary pdfButton" type="button" href="{{ data[row][item].source }}" target="_blank">View in New Tab</a>
        {% endif %}
      </td>
      {% endfor %}
    </tr>
    {% endfor %}
""")

notif = Template("""
<div class="alert alert-{{ type }}" role="alert">
  <strong>{{ code }}</strong>{{ message }}
</div>
""")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', data=data)


@app.route('/selected')
def selected():
    selected = json.loads(request.args.get("value"))
    print ("selected artworks", selected)
    sets = OrderedDict()
    for item in selected:
        sets[item] = OrderedDict(data[item])
    return jsonify(result=table.render(data=sets))


@app.route('/all')
def all():
    return jsonify(result=table.render(data=data))


@app.route('/submit')
def submit():
    # choices = json.loads(request.args.get('choices'))
    favs = json.loads(request.args.get('favs'))
    token = request.args.get('token')
    tokens = json.load(open(os.path.join(app.root_path, "static", "tokens.json")))
    submission = {}
    if token in tokens:
      submission.update({str(token) : json.dumps(favs)})
        # submission = '{"%s":{"favourites":%s}}\n' % (str(token), json.dumps(favs))
      with open(os.path.join(app.root_path, "static", "submissions.json"), "a") as file:
          file.write(json.dumps(submission, sort_keys = True, indent = 4, separators = None))
      return jsonify(result=notif.render(type="success", code="Success: ", message="Submission was recieved."))
    elif token == "":
      return jsonify(result=notif.render(type="warning", code="Warning: ", message="Missing Token."))
    else:
      return jsonify(result=notif.render(type="danger", code="Error: ", message="Invalid token."))


@app.route('/sheets')
def sheets():
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

  SAMPLE_SPREADSHEET_ID = '1ARPAEK5IHN6o5PEy2KXQzMbDFRqEEYaViv_nTVswEkU'
  SAMPLE_RANGE_NAME = 'Form Responses 1'

  creds = None

  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)

  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  service = build('sheets', 'v4', credentials=creds)

  #construct urls of pdf and jpgs 
  this_dir, this_filename = os.path.split(__file__)
  directory_one = os.path.join(this_dir, "static/Sample_one")
  directory_two = os.path.join(this_dir, "static/Sample_two")
  directory_three = os.path.join(this_dir, "static/Sample_three")
  
  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME).execute()
  values = result.get('values', [])

  response = {}
  response["sheetdata"] = values
  array = []
  
  internNameList = []
  for element in response["sheetdata"]:
    if "//vimeo.com" in element[24] or "//vimeo.com" in element[27] or "//vimeo.com" in element[30]:
        element[24] = element[24].replace("//vimeo.com/", "//player.vimeo.com/video/")
        element[27] = element[27].replace("//vimeo.com/", "//player.vimeo.com/video/")
        element[30] = element[30].replace("//vimeo.com/", "//player.vimeo.com/video/")
    elif "/watch?v=" in element[24] or "/watch?v=" in element[27] or "/watch?v=" in element[30]:
        element[24] = element[24].replace("/watch?v=", "/embed/")
        element[27] = element[27].replace("/watch?v=", "/embed/")
        element[30] = element[30].replace("/watch?v=", "/embed/")
        element[24] = re.sub("(&\\S*)", "", element[24])
        element[27] = re.sub("(&\\S*)", "", element[27])
        element[30] = re.sub("(&\\S*)", "", element[30])
    elif "youtu.be" in element[24] or "youtu.be" in element[27] or "youtu.be" in element[30]:
        element[24] = element[24].replace("youtu.be/", "youtube.com/embed/")
        element[27] = element[27].replace("youtu.be/", "youtube.com/embed/")
        element[30] = element[30].replace("youtu.be/", "youtube.com/embed/")
        element[24] = re.sub("(&\\S*)", "", element[24])
        element[27] = re.sub("(&\\S*)", "", element[27])
        element[30] = re.sub("(&\\S*)", "", element[30])
    elif "spotify" in element[24] or "spotify" in element[27] or "spotify" in element[30]:
        element[24] = element[24].replace("open.spotify.com/", "open.spotify.com/embed/")
        element[27] = element[27].replace("open.spotify.com/", "open.spotify.com/embed/")
        element[30] = element[30].replace("open.spotify.com/", "open.spotify.com/embed/")
    elif "drive.google" in element[23] or "drive.google" in element[26] or "drive.google" in element[29]:
        element[23] = element[23].replace("drive.google.com/open?id=", "drive.google.com/file/d/")
        element[26] = element[26].replace("drive.google.com/open?id=", "drive.google.com/file/d/")
        element[29] = element[29].replace("drive.google.com/open?id=", "drive.google.com/file/d/")
        
    sheetDict = {'email': element[1], 
                  'first': element[3], 
                  'last': element[4],
                  'sample': [{"image": element[23], "video": element[24], "desc": element[25]},
                          {"image": element[26], "video": element[27], "desc": element[28]},
                          {"image": element[29], "video": element[30], "desc": element[31]}
                          ]
                  }

    internName = sheetDict['first'] + " " + sheetDict['last']
    internNameList.append(internName)
    dironenames = []

    for item in os.listdir(directory_one):
      file = re.search("(\w+ *\S*)(?=\.).(png|jpg|jpeg|pdf|tif|gif|PNG|JPG|PDF|TIF|GIF|JPEG)", item)
      if file is not None:
          name = file.group(1)
          type = file.group(2)
          dironenames.append(name)

          if "pdf" in type.lower() or "png" in type.lower() or "jpg" in type.lower() or "tif" in type.lower() or "gif" in type.lower() or "jpeg" in type.lower():
            if name.lower() == internName.lower():
              sheetDict['sample'][0]['image'] = "/static/Sample_one/" + item
            
    
    for item in os.listdir(directory_two):
      file = re.search("(\w+ *\S*)(?=\.).(png|jpg|jpeg|pdf|tif|gif|PNG|JPG|PDF|TIF|GIF|JPEG)", item)
      if file is not None:
          name = file.group(1)
          type = file.group(2)
          if "pdf" in type.lower() or "png" in type.lower() or "jpg" in type.lower() or "tif" in type.lower() or "gif" in type.lower() or "jpeg" in type.lower():
            if name.lower() == internName.lower():
              sheetDict['sample'][1]['image'] = "/static/Sample_two/" + item
            
              

              
    
    for item in os.listdir(directory_three):
      file = re.search("(\w+ *\S*)(?=\.).(png|jpg|jpeg|pdf|tif|gif|PNG|JPG|PDF|TIF|GIF|JPEG)", item)
      if file is not None:
          name = file.group(1)
          type = file.group(2)
          if "pdf" in type.lower() or "png" in type.lower() or "jpg" in type.lower() or "tif" in type.lower() or "gif" in type.lower() or "jpeg" in type.lower():
            if name.lower() == internName.lower():
              sheetDict['sample'][2]['image'] = "/static/Sample_three/" + item

    for sampleObj in sheetDict['sample']:
      if ".tif" in sampleObj['image']:
        print(sampleObj['image']  )  
        splittedobj = sampleObj['image'].split('.') 
        print("splaitted obj", splittedobj)
        splittedobj[1] = '.jpg'
        sampleObj['image'] = splittedobj[0] + splittedobj[1]
        print("sample obj" , sampleObj['image'])


    array.append(sheetDict)
    # print(" sheetdict", sheetDict)
    with open('static/jsonData.json', 'w') as file:
      file.write(json.dumps(array, sort_keys = True, indent = 4, separators = None))
  
  
  return response

if __name__ == "__main__":
    app.run(debug = True)


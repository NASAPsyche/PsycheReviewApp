import sys

#Expand Python classes path with your app’s path
sys.path.insert(0, “/data4/raj/src/anaconda3/envs/nasapsyche/lib/python3.7/site-packages”)
from PsycheReviewApp import app

#Initialize WSGI app object
application = app
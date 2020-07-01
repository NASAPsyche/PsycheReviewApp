# PsycheReviewApp
A system used to review the applications of NASA Psyche interns.

## Preview

<img width="1426" alt="Screenshot 2020-06-29 at 7 39 36 PM" src="https://user-images.githubusercontent.com/11274840/86078044-0c963580-ba42-11ea-9216-11d817853d6a.png">
<img width="1425" alt="Screenshot 2020-06-29 at 7 40 02 PM" src="https://user-images.githubusercontent.com/11274840/86078047-11f38000-ba42-11ea-86a7-dc9d163823c0.png">

[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)

## Minimal Application

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
      return 'Hello, World!'
      
## Running flask application?
    $ export FLASK_APP=app.py
    $ flask run

## Running app in debug mode
DEBUG=TRUE
so that you dont need to start the server over and over when there is a change

    $ export FLASK_DEBUG=1
    $ flask run


or add this 

    if __name__ == '__main__':
    app.run(debug=True)
    
    
## How to run app on different port  

    if __name__ == '__main__':
    app.run(host='127.0.0.1',port=4455, debug=True)
    
Output:

<img width="615" alt="Screenshot 2020-06-29 at 9 02 02 PM" src="https://user-images.githubusercontent.com/11274840/86082110-d8277700-ba4b-11ea-8627-0c0da46af850.png">

## How to resolve Server is already in use error?

    kill -9 `lsof -i:5000 -t`
    
5000 is the port number    

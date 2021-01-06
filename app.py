from flask import Flask
from flask import render_template
from flask import request
import json
import logic_newuser

app = Flask(__name__)
appConfig = logic_newuser.baseConfig()
app.config['SECRET_KEY'] = appConfig

@app.route('/newUser',  methods=['POST'])
def newUser():
    if request.method == 'POST':
      print(request.json)
      userJSON = request.json
      logic_newuser.createUser(userJSON)

    return 'JSON Posted'

@app.route('/test',  methods=['POST'])
def test():
    if request.method == 'POST':
      print(request.json)

    return 'JSON Posted'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, use_reloader=True, debug=True)

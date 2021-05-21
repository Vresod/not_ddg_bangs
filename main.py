import json
from flask import Flask, abort, request, redirect

app = Flask(__name__)
with open("bangs.json") as bangsfile: bangs = json.loads(bangsfile.read())

print(bangs)

@app.route('/', methods=['GET'])
def root():
	search = request.args.get('q')
	if search == None: # has no query
		return {'code':400,'message':'Invalid query'}, 400
	if not search.startswith('!'): # not a bang
		return redirect(f'https://duckduckgo.com/?q={search}')
	if search.lower().replace('!','').split(' ')[0] in bangs: # is a bang
		return 'you are a little piss boy'



# @app.route('/reload_bangs',methods=['PUT'])
# def reload_bangs():
# 	global bangs
# 	bangs = json.loads

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)

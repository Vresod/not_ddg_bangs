import json
from flask import Flask,  request, redirect, render_template
import extra

app = Flask(__name__)
with open("bangs.json") as bangsfile: bangs = json.loads(bangsfile.read())

@app.route('/search', methods=['GET'])
def search():
	search = request.args.get('q')
	if search == None: # has no query
		return {'code':400,'message':'Invalid query'}, 400
	extracted = extra.extract_bang(search,bangs)
	if not extracted:
		return redirect(f'https://duckduckgo.com/?q={search}'), 307
	return redirect(f'{bangs[extracted[0]] % extracted[1]}')

@app.route('/bangs',methods=['GET'])
def get_bangs():
	return bangs

@app.route('/',methods=['GET'])
def root():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)

import json
from flask import Flask,  request, redirect, render_template, url_for
import extra
import urllib.parse

app = Flask(__name__)
with open("bangs.json") as bangsfile: bangs = json.loads(bangsfile.read())

@app.route('/search', methods=['GET'])
def search():
	search = request.args.get('q')
	if not search: # has no query
		return redirect(url_for('root',e=5),code=307)
	extracted = extra.extract_bang(search,bangs)
	if not extracted:
		return redirect(f'https://duckduckgo.com/?q={urllib.parse.quote(search)}',code=307)
	if extracted[1] == search:
		return redirect(extra.get_root(bangs[extracted[0]]),code=307)
	return redirect(f'{bangs[extracted[0]] % extracted[1]}',code=307)

@app.route('/raw_bangs',methods=['GET'])
def get_bangs():
	return bangs

@app.route('/',methods=['GET'])
def root():
	return render_template('index.html',firefox=request.user_agent.browser == "firefox",linux=request.user_agent.platform == "linux",bad_search=bool(request.args.get("e")))

@app.route('/bangs',methods=['GET'])
def view_bangs():
	return render_template('bangs.html',bangs=bangs)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)

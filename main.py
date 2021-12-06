import json
from flask import Flask,  request, redirect, render_template, url_for
import requests
import extra
import urllib.parse

app = Flask(__name__)
bangs = json.load(open("bangs.json"))
engines = {"DuckDuckGo":"https://duckduckgo.com?q=%s","Google":"https://google.com/search?q=%s","Yahoo!":"https://search.yahoo.com/search?p=%s","Bing":"https://www.bing.com/search?q=%s"}

@app.route('/search', methods=['GET'])
def search():
	search = request.args.get('q')
	engine = request.args.get('engine') or 'DuckDuckGo'
	ddg_if_bang = bool(request.args.get('dib'))
	if not search: return redirect(url_for('root',e=5),code=307)
	extracted = extra.extracted_bang.from_str(search,bangs['bangs'],bangs['shortcuts'])
	print(extracted)
	# for DIB
	if ddg_if_bang and engine != 'DuckDuckGo' and search.startswith('!') and not extracted:
		if json.loads(requests.get(f"https://api.duckduckgo.com/?q={search}&format=json&no_redirect=1").content).get('Redirect'):
			return redirect(engines['DuckDuckGo'] % search)
	if extracted.term == f"!{extracted.bang}":
		return redirect(extra.get_root(f'{bangs["bangs"][extracted.bang] % extracted.term}'),code=307)
	if extracted.shortcut and extracted.term == '':
		return redirect(extra.get_root(f'{bangs["shortcuts"][extracted.bang] % (extracted.shortcut,extracted.term)}'),code=307)
	if extracted.shortcut:
		return redirect(f'{bangs["shortcuts"][extracted.bang] % (extracted.shortcut,extracted.term)}',code=307)
	if extracted.bang:
		return redirect(f'{bangs["bangs"][extracted.bang] % extracted.term}',code=307)
	return redirect(engines[engine] % urllib.parse.quote(search),code=307)

@app.route('/raw_bangs',methods=['GET'])
def get_bangs():
	return bangs

@app.route('/',methods=['GET'])
def root():
	return render_template('index.html',firefox=request.user_agent.browser == "firefox",linux=request.user_agent.platform == "linux",bad_search=bool(request.args.get("e")),engines=engines)

@app.route('/bangs',methods=['GET'])
def view_bangs():
	return render_template('bangs.html',bangs=bangs['bangs'])

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
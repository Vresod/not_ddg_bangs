from typing import Optional, Union
import re
from dataclasses import dataclass

@dataclass
class extracted_bang:
	term:str
	bang:Optional[str] = None
	shortcut:Optional[str] = None
	
	def __bool__(self):
		return bool(self.bang)

def extract_bang(bang_str:str,bangs:dict[str],shortcuts:dict[str]) -> extracted_bang:
	bang_str = bang_str.lower()
	for shortcut in shortcuts:
		if bang_str.startswith(f"!{shortcut}."):
			return extracted_bang(bang=shortcut, shortcut=(d := bang_str.replace(f'!{shortcut}.','',1).split(" ",maxsplit=1))[0], term=d[1])
	for bang in bangs:
		if bang_str.split()[0] == f'!{bang}':
			return extracted_bang(bang=bang, term=bang_str.replace(f'!{bang} ','',1))
	return extracted_bang(bang_str)

def get_root(url:str) -> Union[str,bool]:
	regex = re.compile(r"(^https?:\/\/(www\.)?[\da-zA-Z\.-]+)")
	match = regex.match(url)
	if not match:
		return False
	return match[0]


if __name__ == "__main__":
	def main():
		import json
		bangs = json.load(open("bangs.json"))
		assert extract_bang("!hits bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones","hits")
		assert extract_bang("!w.en bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones","w","en")
		assert extract_bang("bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones")
	main()
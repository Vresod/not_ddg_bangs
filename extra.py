from typing import Union
import re

def extract_bang(bang_str:str,bangs:dict) -> Union[tuple,bool]:
	bang_str = bang_str.lower()
	for bang in bangs:
		if bang_str.split()[0] == f'!{bang}':
			return bang, bang_str.replace(f'!{bang} ','',1)
	return False

def get_root(url:str) -> Union[str,bool]:
	regex = re.compile(r"(^https?:\/\/(www\.)?[\da-zA-Z\.-]+)")
	match = regex.match(url)
	if not match:
		return False
	return match[0]
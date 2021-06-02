from typing import Union

def extract_bang(bang_str:str,bangs:dict) -> Union[tuple,bool]:
	bang_str = bang_str.lower()
	for bang in bangs:
		if bang_str.startswith(f'!{bang}'):
			return bang, bang_str.replace(f'!{bang} ','',1)
	return False
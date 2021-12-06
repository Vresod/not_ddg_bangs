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
	@classmethod
	def from_str(cls,bang_str:str,bangs:dict[str],shortcuts:dict[str]):
		bang_str = bang_str.lower()
		for shortcut in shortcuts:
			if bang_str.startswith(f"!{shortcut}."):
				return cls(bang=shortcut, shortcut=(d := bang_str.replace(f'!{shortcut}.','',1).split(" ",maxsplit=1))[0], term=d[1] if len(d) > 1 else "")
		for bang in bangs:
			if bang_str.split()[0] == f'!{bang}':
				return cls(bang=bang, term=bang_str.replace(f'!{bang} ','',1))
		return cls(bang_str)


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
		assert extracted_bang.from_str("!hits bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones","hits")
		assert extracted_bang.from_str("!w.en bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones","w","en")
		assert extracted_bang.from_str("bones",bangs['bangs'],bangs['shortcuts']) == extracted_bang("bones")
	main()
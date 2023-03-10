from typing import (
	Final,
	List,
	Dict,
	Any
)
import obj


class Loader(obj.ObjStaticRW):
	objs:List[Dict[str, Any]]
	def __init__(self, HASH:int, FATHR_HASH:int, objs:List[Dict[str, Any]])->None: ...
	def save(self)->None: ...
	def close(self)->None: ...

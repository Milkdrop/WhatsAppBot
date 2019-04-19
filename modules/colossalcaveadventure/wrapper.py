import time, re
import importlib.util
from .moddata import main as mod

def init():
	return mod.init() #Return game object
	
def query(obj, q):
	q = re.findall(r'\w+', q)
	obj.do_command(q)

def getoutput(obj):
	return obj.output + "> █"
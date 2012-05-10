import random
from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

def randomize(request):
	dajax = Dajax()
	dajax.assign('#result','value',random.randint(1, 10))
	return dajax.json()
dajaxice_functions.register(randomize)

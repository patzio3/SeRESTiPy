import os

from src/client import JsonHelper

json = jh.input2json(os.path.join(os.getcwd(), "/WORK/p_esch01/progs/restApi/src/inp"))[0]

print(json)
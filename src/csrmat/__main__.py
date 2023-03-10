import sys
import json
from csrmat import CSRMat
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return super().default(obj)

def main(argc, argv):
	if argc < 3:
		print("Usage: csrmat NONE IN_FILE.json [OUT_FILE.json]")
		print("  NONE is a highly repeated json object in the matrix.")
		print("  IN_FILE.json is a file with a list of lists (a matrix).")
		print("  OUT_FILE.json is a file with an CSRMat object.")
		return

	with open(argv[2], "r") as fp:
		mat = json.load(fp)
	
	with open("csrmat.json" if argc == 3 else argv[3], "w") as fp:
		json.dump(CSRMat(mat, json.loads(argv[1])).asdict, fp, cls=NumpyArrayEncoder)

if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
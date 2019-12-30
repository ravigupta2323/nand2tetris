import os
import sys
from os import path
import subprocess

tar_file = sys.argv[1]
if not tar_file.endswith(".tar.gz"):
	print("Extension of file is not .tar.gz")
	sys.exit(0)

else:
	subprocess.run(["tar", "xzvf", tar_file])
	rollnum = tar_file[:tar_file.index(".tar.gz")]
	if(not path.exists(rollnum)):
		print("Folder name is not same as tar.gz file")
		sys.exit(0)
	else:
		os.chdir(rollnum)

		if (not path.exists("run_compiler.sh")):
			print("run_compiler.sh file not present")
			sys.exit(0)
		else:
			subprocess.run(["chmod", "+x", "./run_compiler.sh"])
			print("Done")
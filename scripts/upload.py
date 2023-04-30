import toml
import sys
import os
user = sys.argv[1]
password = sys.argv[2]

PACKAGE_NAME = "luau"

with open("pyproject.toml", "r") as file:
	data = toml.loads(file.read())
	version = data["project"]["version"]
	os.system(f"twine upload dist/{PACKAGE_NAME}-{version}.tar.gz -u {user} -p {password} --verbose")


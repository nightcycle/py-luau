import os
import dpath
import sys
import json
from .util import run_bundled_exe

DEFAULT_ROJO_PROJECT_PATH = "default.project.json"
ROJO_SOURCE = "rojo-rbx/rojo"
ROJO_VERSION = "7.1.0"

def get_rojo_project_path() -> str:
	if os.path.exists(DEFAULT_ROJO_PROJECT_PATH):
		return DEFAULT_ROJO_PROJECT_PATH
	for file_path in os.listdir(""):
		if os.path.isfile(file_path):
			base, ext = os.path.splitext(file_path)
			if ext == ".json":
				sec_base, sec_ext = os.path.splitext(base)
				if sec_ext== ".project":
					return file_path

def build_sourcemap(project_json_path: str = ""):
	if project_json_path == "":
		project_json_path = get_rojo_project_path()
	
	run_bundled_exe(exe_name="py_luau_rojo.exe", args=["sourcemap", project_json_path, "--output", "sourcemap.json"])


def get_roblox_path_from_env_path(env_path: str) -> str:
	project_path = get_rojo_project_path()
	rojo_file = open(project_path, "r")
	rojo_config = json.loads(rojo_file.read())
	rojo_file.close()
	tree_config = rojo_config["tree"]
	options = {}
	env_length = len(env_path.split("/"))
	best_env_path = ""
	best_env_length = 0
	for tree_path, tree_val in dpath.search(tree_config, '**', yielded=True):
		keys = tree_path.split("/")
		final_key = keys[len(keys)-1]
		if final_key == "$path" and len(keys) > 1:
			ro_path = "game/" + "/".join(keys[0:(len(keys)-1)])
			options[tree_val] = ro_path
			val_length = len(tree_val.split("/"))
			if val_length <= env_length and best_env_length < val_length:
				pattern = env_path[0:len(tree_val)]
				if pattern == tree_val:
					best_env_path = tree_val
					best_env_length = val_length

	conclusion = env_path[(len(best_env_path)):]
	final = options[best_env_path] + conclusion

	return final.split(".")[0]

import os
from .tool import get_tool_name

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

def get_rojo_name() -> str:
	return get_tool_name(ROJO_SOURCE, ROJO_VERSION)

def build_sourcemap(project_json_path: str = ""):
	if project_json_path == "":
		project_json_path = get_rojo_project_path()
	os.system(f"{get_rojo_name()} sourcemap {project_json_path} --output sourcemap.json")	
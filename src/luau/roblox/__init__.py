import os
from .tool import get_tool_name

def format(path: str):
	stylua_tool_name = get_tool_name("JohnnyMorganz/StyLua", "0.15.3")
	os.system(f"{stylua_tool_name} {path}")

def write_script(build_path: str, content: str, write_as_directory: bool=False):
	dir_name, file_name = os.path.split(build_path)
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	elif os.path.exists(build_path):
		os.remove(build_path)

	if write_as_directory:
		full_dir_path = build_path.split(".")[0]
		full_ext = ".".join(build_path.split(".")[1:])
		final_dir_path = (dir_name+"/"+file_name).replace(full_ext, "")
		os.makedirs(final_dir_path)
		init_file_path = final_dir_path+"/init."+full_ext
		out_file = open(init_file_path, "w")
		out_file.write(content)
		out_file.close()
		format(init_file_path)

	else:
		out_file = open(build_path, "w")
		out_file.write(content)
		out_file.close()
		format(build_path)


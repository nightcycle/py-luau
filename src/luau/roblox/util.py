import os
import sys
import subprocess
from pkg_resources import resource_filename

def get_instance_from_path(path: str) -> str:
	
	roblox_path_keys = path.split("/")

	roblox_path = ""

	for i, key in enumerate(roblox_path_keys):
		if i == 0:
			roblox_path += key
		else:
			roblox_path += f":WaitForChild(\"{key}\")"

	for service in ["ReplicatedStorage", "ServerStorage", "ServerScriptService", "ReplicatedFirst", "Lighting", "StarterGui", "StarterPlayer", "Workspace"]:
		roblox_path = roblox_path.replace(f"game:WaitForChild(\"{service}\")", f"game:GetService(\"{service}\")")

	return roblox_path

def run_bundled_exe(exe_name, args=None):
	# Get the path to the bundled executable file within the package
	exe_file_path = resource_filename('luau', f'data/{exe_name}')

	# Check if running as a PyInstaller single-file executable
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		# Construct the path to the executable file in a PyInstaller bundle
		exe_file_path = os.path.join(sys._MEIPASS, 'data', exe_name)

	# Ensure the file is executable
	os.chmod(exe_file_path, 0o755)

	# Build the command to run, including the executable path and any arguments
	cmd = [exe_file_path]
	if args:
		cmd.extend(args)

	# Run the bundled executable with the specified arguments
	subprocess.run(cmd, check=True)

def get_module_require(path: str):
	return f"require({get_instance_from_path(path)})"

def get_header_module(path: str, variable_name: str = ""):
	if variable_name == "":
		keys = path.split("/")
		variable_name = keys[len(keys)-1]

	value = get_module_require(path)

	return f"local {variable_name} = {value}"

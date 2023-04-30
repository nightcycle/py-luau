import os
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

def run_bundled_exe(exe_name: str, args: list[str]=[]):
	exe_name = os.path.splitext(exe_name)[0]

	abs_path = resource_filename('luau', f'data/{exe_name}.exe')
	arg_command = " ".join(args)
	sys_command = " ".join([abs_path, arg_command])
	os.system(sys_command)

def get_module_require(path: str):
	return f"require({get_instance_from_path(path)})"

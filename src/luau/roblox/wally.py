import os
import toml
from .tool import get_tool_name
from .rojo import get_rojo_project_path, get_rojo_name, build_sourcemap

WALLY_SOURCE = "UpliftGames/wally"
WALLY_VERSION = "0.3.1"
WPT_SOURCE = "JohnnyMorganz/wally-package-types"
WPT_VERSION = "1.2.0"

def get_wally_name():
	return get_tool_name(WALLY_SOURCE, WALLY_VERSION)

def get_wally_package_types_name():
	return get_tool_name(WPT_SOURCE, WPT_VERSION)

def update_wally():

	project_path = get_rojo_project_path()

	wally_tool_name = get_wally_name()
	rojo_tool_name = get_rojo_name()
	wpt_tool_name = get_wally_package_types_name()

	os.system(f"{wally_tool_name} install")
	build_sourcemap()
	os.system(f"{wpt_tool_name} --sourcemap sourcemap.json Packages")

def get_wally_package_nickname(package_wally_path: str, prefix: str="ToolGen") -> str:
	wally_config = toml.loads(open("wally.toml", "r").read())
	generated_nickname = (package_wally_path.split("/")[1].split("@")[0]).title()
	for nickname, package_path in wally_config["dependencies"].items():
		if nickname == generated_nickname:
			generated_nickname = prefix+"_"+generated_nickname.title()
		if package_wally_path == package_path:
			return nickname

	# no maid installed
	wally_config["dependencies"][generated_nickname] = package_wally_path

	open("wally.toml", "w").write(toml.dumps(wally_config))
	update_wally()

	return generated_nickname

def require_roblox_wally_package(
	package_wally_path: str, 
	is_private: bool = False, 
	is_header: bool = True,
	wally_directory_path: str ="game/ReplicatedStorage/Packages"
) -> str:

	package_nickname = get_wally_package_nickname(package_wally_path)

	package_path = ""
	roblox_path_keys = (wally_directory_path+"/"+package_nickname).split("/")
	for i, key in enumerate(roblox_path_keys):
		if i == 0:
			package_path += key
		else:
			package_path += f":WaitForChild(\"{key}\")"

	package_path = package_path.replace("game:WaitForChild(\"ReplicatedStorage\")", "game:GetService(\"ReplicatedStorage\")")
	package_path = package_path.replace("game:WaitForChild(\"ServerStorage\")", "game:GetService(\"ServerStorage\")")
	package_path = package_path.replace("game:WaitForChild(\"ReplicatedFirst\")", "game:GetService(\"ReplicatedFirst\")")

	if is_header:
		if is_private:
			return f"local _{package_nickname} = require({package_path})"
		else:
			return f"local {package_nickname} = require({package_path})"
	else:
		return f"require({package_path})"


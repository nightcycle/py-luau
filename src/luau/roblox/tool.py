
import os
import toml

FOREMAN_DEFAULT_PATH = "foreman.toml"
AFTMAN_DEFAULT_PATH = "aftman.toml"

def get_tool_name(source: str, version: str, prefix:str = "ToolGen") -> str:
	alt_nickname = source.split("/")[len(source.split("/"))-1]
	if os.path.exists(FOREMAN_DEFAULT_PATH):
		foreman_config = toml.loads(open(FOREMAN_DEFAULT_PATH, "r").read())
		foreman_tools = foreman_config["tools"]
		for nickname, entry in foreman_tools.items():
			if nickname == alt_nickname:
				alt_nickname = prefix+"_"+alt_nickname

			if "source" in entry and "version" in entry:
				if entry["source"] == source and entry["version"] == version:
					return nickname

		foreman_tools[alt_nickname] = {
			"source": source,
			"version": version
		}

		foreman_file = open(FOREMAN_DEFAULT_PATH, "w")
		foreman_file.write(toml.dumps(foreman_config))
		foreman_file.close()

		os.system("foreman install")

		return alt_nickname

	elif os.path.exists(AFTMAN_DEFAULT_PATH):
		aftman_config = toml.loads(open(AFTMAN_DEFAULT_PATH, "r").read())
		aftman_tools = aftman_config["tools"]
		aft_path = source+"@"+version
		for nickname, path in aftman_tools.items():
			if nickname == alt_nickname:
				alt_nickname = prefix+"_"+alt_nickname
			if path == aft_path:
				return path
		
		os.system(f"aftman add {aft_path} -{alt_nickname}")
		return alt_nickname
	else:
		raise IndexError("no foreman or aftman config files found")

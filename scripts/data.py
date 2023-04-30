import os

MODULE_NAME = "luau"
DATA_DIR = f"src/{MODULE_NAME}/data"

with open("MANIFEST.in", "w") as file:
	lines = []
	for data_file_name in os.listdir(DATA_DIR):
		lines.append(f"recursive-include {DATA_DIR} {data_file_name}")

	file.write("\n".join(lines))
import os
import shutil
from typing import Literal

def set_language_ext(path: str, desired_ext: Literal["luau", "lua"]) -> str:
	base, ext = os.path.splitext(path)
	return base + "." + desired_ext

def get_alt_ext_path(path: str) -> str:
	base, ext = os.path.splitext(path)
	if ext == ".luau":
		return set_language_ext(path, "lua")
	else:
		return set_language_ext(path, "luau")

def update_file_to_ext(path: str, desired_ext: Literal["luau", "lua"]):
	base, ext = os.path.splitext(path)
	src_file = open(path, "r")
	content = src_file.read()
	src_file.close()
	os.remove(path)

	out_file = open(base+"."+desired_ext, "w")
	out_file.write(content)
	out_file.close()


def get_domain_ext(path: str) -> str | None:
	base, lua_ext = os.path.splitext(path)
	second_base, domain_ext = os.path.splitext(base)
	if len(domain_ext) == 0:
		return None
	else:
		return domain_ext[1:]


def filter_domain(path: str) -> str:
	domain_ext = get_domain_ext(path)
	if domain_ext != None:
		return path.replace("."+domain_ext, "")
	return path

def get_if_using_lua_or_luau_ext(path: str) -> str:
	base, lua_ext = os.path.splitext(path)
	return lua_ext[1:]


def get_full_ext(path: str) -> str:
	ext = get_if_using_lua_or_luau_ext(path)
	domain = get_domain_ext(path)
	if domain == None:
		return ext
	else:
		return domain+"."+ext

def strip_full_ext(path: str) -> str:
	full_ext = get_full_ext(path)
	return path.replace(full_ext, "")

def get_if_module_script(path: str) -> bool:
	if get_domain_ext(path) == None:
		return True
	else:
		return False

def insert_domain(build_path: str, domain: str) -> str:
	no_domain_path = filter_domain(build_path)
	base, ext = os.path.splitext(no_domain_path)
	return base+"."+domain+ext

def remove_all_path_variants(path: str, domain: str=""):
	alt_ext_path = get_alt_ext_path(path)

	base_path = strip_full_ext(path)
	if os.path.exists(base_path):
		shutil.rmtree(base_path)

	if os.path.exists(path):
		os.remove(path)

	if os.path.exists(alt_ext_path):
		os.remove(alt_ext_path)

	if get_domain_ext(path) != None:
		no_domain_path = filter_domain(path)
		alt_no_domain_path = filter_domain(alt_ext_path)

		if os.path.exists(no_domain_path):
			os.remove(no_domain_path)

		if os.path.exists(alt_no_domain_path):
			os.remove(alt_no_domain_path)

	elif domain != "":
		domain_path = insert_domain(path, domain)
		alt_domain_path = insert_domain(alt_ext_path, domain)

		if os.path.exists(domain_path):
			os.remove(domain_path)

		if os.path.exists(alt_domain_path):
			os.remove(alt_domain_path)
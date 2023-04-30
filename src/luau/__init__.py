# creates a recursive luau table
def import_type(module_variable_name: str, type_name: str, type_local_name="") -> str:
	if type_local_name == "":
		type_local_name = type_name

	return f"type {type_local_name} = {module_variable_name}.{type_name}"	

def indent_block(content: list[str], indent_count: int = 1) -> list[str]:
	out = []
	for line in content:
		out.append(("\t"*indent_count)+line)

	return out

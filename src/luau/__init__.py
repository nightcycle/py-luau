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

def define_variable(
	variable_name: str, 
	value: str | None = None, 
	type_name: str | None = None, 
	is_private: bool = False, 
	include_semi_colon: bool = False
):
	final_variable_name = variable_name
	if is_private:
		final_variable_name = "_"+final_variable_name

	definition = f"local {final_variable_name}"
	if type_name != None:
		definition += f": {type_name}"

	statement = definition
	if value != None:
		statement = f"{definition} = {value}"

	if include_semi_colon:
		return statement + ";"
	else:
		return statement	

def get_function_header(name: str = "", parameters: list=[], return_type="", is_local: bool=False) -> str:
	assert name != "" or is_local==False, "you can't have a nameless local function"

	final_name_text = ""
	if name != "":
		final_name_text = " "+name

	local_text = ""
	if is_local:
		local_text = "local "

	param_text = ",".join(parameters)

	return_text = ""
	if return_type != "":
		return_text += f": {return_type}"

	return f"{local_text}function{final_name_text}({param_text}){return_text}"

def get_function_call(name: str="", object_name:str="", parameters: list=[]) -> str:
	object_text = ""
	if object_name != "":

		def get_first_letter(string):
			if not string:
				return None
			for char in string:
				if char.isalpha():
					return char
			
			return None

		first_letter = get_first_letter(name)
		if first_letter != None:
			if first_letter.isupper():
				object_text = object_text+":"
			else:
				object_text = object_text+"."
		else:
			object_text = object_name

	reference = object_text+name

	param_text = ",".join(parameters)

	return f"{reference}({param_text})"

import dpath

READ_STR_AS_LITERAL_PREFIX = "<LITERAL_STRING_START>_!_"
READ_STR_AS_LITERAL_SUFFIX = "_!_<LITERAL_STRING_END>"

def _insert_comma(enabled: bool) -> str:
	if enabled:
		return ","
	else:
		return ""

def _get_indent(indent_count: int) -> str:
	return "\t"*indent_count

def from_bool(value: bool, indent_count=0, add_comma_at_end=False) -> str:
	return _get_indent(indent_count) + str(value).lower() + _insert_comma(add_comma_at_end)

def get_if_literal(value: str):
	return (READ_STR_AS_LITERAL_PREFIX == value[0:len(READ_STR_AS_LITERAL_PREFIX)]) or value.find(READ_STR_AS_LITERAL_SUFFIX) != -1

def from_str(value: str, indent_count=0, add_comma_at_end=False) -> str:
	if get_if_literal(value):
		raw_val = value.replace(READ_STR_AS_LITERAL_PREFIX, "").replace(READ_STR_AS_LITERAL_SUFFIX, "")
		return _get_indent(indent_count) + raw_val + _insert_comma(add_comma_at_end)
	else:
		return _get_indent(indent_count) + f"\"{value}\"" + _insert_comma(add_comma_at_end)

def from_number(value: int | float, indent_count=0, add_comma_at_end=False) -> str:
	return _get_indent(indent_count) + str(value) + _insert_comma(add_comma_at_end)

def from_nil(indent_count=0, add_comma_at_end=False) -> str:
	return f"{_get_indent(indent_count)} nil" + _insert_comma(add_comma_at_end)

def from_list(value: list, indent_count=0, add_comma_at_end=False, multi_line=True, skip_initial_indent=False):
	
	# start list
	list_val = ""
	if skip_initial_indent:
		list_val += "{"
	else:
		list_val += _get_indent(indent_count) + "{"

	# iterate through values
	for v in value:
		
		# write entry
		if type(v) == dict or type(v) == list:
			entry = from_any(v, indent_count+1, False, multi_line, True) + _insert_comma(True)
		else:
			entry = from_any(v, indent_count, False, multi_line, True) + _insert_comma(True)

		# add it to existing string
		if multi_line:
			list_val += "\n" + _get_indent(indent_count+1) + entry
		else:
			list_val += entry

	# end the table on a new line if multi-line
	if multi_line:
		list_val += "\n" + _get_indent(indent_count)

	# close the table
	list_val += "}"

	# indent as needed and return value
	return _get_indent(indent_count) + list_val + _insert_comma(add_comma_at_end)

def from_dict(value: dict, indent_count=0, add_comma_at_end=False, multi_line=True, skip_initial_indent=False):
	
	# start dictionary
	list_val = ""
	if skip_initial_indent:
		list_val += "{"
	else:
		list_val += _get_indent(indent_count) + "{"

	# iterate through key-val pairs
	for k, v in value.items():

		is_literal = get_if_literal(k)

		# write entry
		if type(v) == dict or type(v) == list:
			if is_literal:
				entry = f"{from_any(k, 0, False)} = {from_any(v, indent_count+1, False, multi_line, True)}" + _insert_comma(True)
			else:
				entry = f"[{from_any(k, 0, False)}] = {from_any(v, indent_count+1, False, multi_line, True)}" + _insert_comma(True)
		else:
			if is_literal:
				entry = f"{from_any(k, 0, False)} = {from_any(v, 0, False, multi_line, True)}" + _insert_comma(True)
			else:
				entry = f"[{from_any(k, 0, False)}] = {from_any(v, 0, False, multi_line, True)}" + _insert_comma(True)

		# add it to existing string
		if multi_line:
			list_val += "\n" + _get_indent(indent_count+1) + entry
		else:
			list_val += entry

	# end the table on a new line if multi-line
	if multi_line:
		list_val += "\n" + _get_indent(indent_count)

	# close the table
	list_val += "}"

	# indent as needed and return value
	if skip_initial_indent:
		return _get_indent(0) + list_val + _insert_comma(add_comma_at_end)
	else:
		return _get_indent(indent_count) + list_val + _insert_comma(add_comma_at_end)

def from_dict_to_type(type_value: dict, indent_count=0, add_comma_at_end=False, multi_line=True, skip_initial_indent=False) -> str:
	out = {}
	for path, value in dpath.search(type_value, '**', yielded=True):
		literal_path_keys = []
		for key in path.split("/"):
			literal_path_keys.append(mark_as_literal(key))

		literal_path = "/".join(literal_path_keys)

		if value == bool or type(value) == bool:
			dpath.new(out, literal_path, mark_as_literal("boolean"))
		elif value == int or value == float or type(value) == int or type(value) == float:
			dpath.new(out, literal_path, mark_as_literal("number"))
		elif value == str:
			dpath.new(out, literal_path, mark_as_literal("string"))	
		elif type(value) == str:
			if get_if_literal(value):
				dpath.new(out, literal_path, value)
			else:
				dpath.new(out, literal_path, mark_as_literal("string"))	

	return from_dict(out, indent_count, add_comma_at_end, multi_line, skip_initial_indent).replace(" = ", ": ")

def from_any(
	value: int | str | None | float | dict | list = None, 
	indent_count = 0, 
	add_comma_at_end = False, 
	multi_line=True,
	skip_initial_indent=False
) -> str:

	if type(value) == list:

		return from_list(value, indent_count, add_comma_at_end, multi_line, skip_initial_indent)

	elif type(value) == dict:
		
		return from_dict(value, indent_count, add_comma_at_end, multi_line, skip_initial_indent)

	elif type(value) == float or type(value) == int:
		return from_number(value, indent_count, add_comma_at_end)
		
	elif type(value) == bool:
		return from_bool(value, indent_count, add_comma_at_end)
		
	elif type(value) == str:
		return from_str(value, indent_count, add_comma_at_end)
		
	return from_nil(indent_count, add_comma_at_end)


# allows for processing of text in the other methods as is without being wrapped in quotes as a string
def mark_as_literal(text: str) -> str:
	return READ_STR_AS_LITERAL_PREFIX+text+READ_STR_AS_LITERAL_SUFFIX
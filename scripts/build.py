import requests
import dpath
import os
import json
from copy import deepcopy
from typing import Literal, Any

def get_api_data():
	return requests.get(
		url = "https://raw.githubusercontent.com/CloneTrooper1019/Roblox-Client-Tracker/roblox/API-Dump.json",
		params = {}
	).json()

def get_if_path_is_list_descendant(path: str) -> bool:
	keys = path.split("/")
	exception = 0
	for v in keys:
		try:
			v = int(v)
			return True
		except:
			exception += 1
	return False

# Define a custom filter function to ignore branches that are descendants of lists
def iterate_tree(tree: dict) -> dict[str, list[Any]]:
	# Search for all keys and values in the tree using dpath's search function with the custom filter
	output = {}
	for path, value in dpath.search(tree, '**', yielded=True):
		if not isinstance(value, dict) and not isinstance(value, list) and type(value) == str:
			is_list_desc = get_if_path_is_list_descendant(path)

			if not is_list_desc:
				if not path in output:
					output[path] = []

				if not value in output[path]:
					output[path].append(value)

	return output

def build(build_path="src/luau/roblox/api.py"):
	data = get_api_data()

	value_registry = {}

	def append_out(tree_pairs: dict[str, any], prefix=""):
		for k, v in tree_pairs.items():
			k = prefix + k
			if not k in value_registry:
				value_registry[k] = []

			for option in v:
				if not option in value_registry[k]:
					value_registry[k].append(option)

	value_registry["Class/Tags"] = []
	value_registry["Member/Tags"] = []
	enum_data = {}
	enum_content = "\nENUM_TREE = {"
	enum_names = []
	enum_item_names = []
	for enum_entry in data["Enums"]:
		name = enum_entry["Name"]
		enum_data[name] = {}
		enum_names.append(name)
		enum_content += "\n\t\""+name+"\": {"
		for item in enum_entry["Items"]:
			item_name = item["Name"]
			enum_item_names.append(item_name)
			item_val = item["Value"]
			enum_data[name][item_name] = item_val
			enum_content += "\n\t\t\""+item_name+"\": " + str(item_val) + ","
		enum_content += "\n\t},"
	enum_content += "\n}"	

	for api_class in data["Classes"]:
		class_registry = iterate_tree(api_class)
		append_out(class_registry, "Class/")
		for api_member in api_class["Members"]:
			member_registry = iterate_tree(api_member)
			append_out(member_registry, "Member/")
			if "Tags" in api_member:
				for tag in api_member["Tags"]:
					if not tag in value_registry["Member/Tags"]:
						value_registry["Member/Tags"].append(tag)


		if "Tags" in api_class:
			for tag in api_class["Tags"]:
				if not tag in value_registry["Class/Tags"]:
					value_registry["Class/Tags"].append(tag)

	literal_lists = {
		"Class": {
			"Tags": deepcopy(value_registry["Class/Tags"]),
			"MemoryCategory": deepcopy(value_registry["Class/MemoryCategory"]),
			"Name": deepcopy(value_registry["Class/Name"]),
		},
		"Member": {
			"Tags": deepcopy(value_registry["Member/Tags"]),
			"MemberCategory": deepcopy(value_registry["Member/Category"]),
			"MemberType": deepcopy(value_registry["Member/MemberType"]),
			"MemberName": deepcopy(value_registry["Member/Name"]),
			"ThreadSafetyType": deepcopy(value_registry["Member/ThreadSafety"]),
			"SecurityReadType": deepcopy(value_registry["Member/Security/Read"]),
			"SecurityWriteType": deepcopy(value_registry["Member/Security/Write"]),
			"ValueTypeCategory": deepcopy(value_registry["Member/ValueType/Category"]),
			"ValueTypeName": deepcopy(value_registry["Member/ValueType/Name"]),
		},
	}
	literal_lists["Class"]["Name"].append("<<<ROOT>>>")

	api_version_list = []
	for i in range(1, data["Version"]+1):
		api_version_list.append(i)

	# with open("api.json", "w") as file:
	# 	file.write(json.dumps(data, indent=5))

	# with open("options.json", "w") as file:
	# 	file.write(json.dumps(value_registry, indent=5))	

	# with open("literals.json", "w") as file:
	# 	file.write(json.dumps(literal_lists, indent=5))	

	if os.path.exists(build_path):
		os.remove(build_path)
	with open(build_path, "w") as file:
		file.write(f"""import io
import requests
import json
import os
from tempfile import TemporaryDirectory
from typing import TypedDict, Literal, Any, Union
from copy import deepcopy

ApiMemoryCategory = Literal{json.dumps(literal_lists["Member"]["MemberCategory"])}
ApiPropertyTag = Literal{json.dumps(literal_lists["Member"]["Tags"])}
ApiClassTag = Literal{json.dumps(literal_lists["Class"]["Tags"])}
ApiPropertyCategory = Literal{json.dumps(literal_lists["Member"]["MemberCategory"])}
ApiMemberType = Literal{json.dumps(literal_lists["Member"]["MemberType"])}
ApiThreadSafety = Literal{json.dumps(literal_lists["Member"]["ThreadSafetyType"])}
ApiValueCategory = Literal{json.dumps(literal_lists["Member"]["ValueTypeCategory"])}
ApiValueTypeName = Literal{json.dumps(literal_lists["Member"]["ValueTypeName"])}
ApiClassTypeName = Literal{json.dumps(literal_lists["Class"]["Name"])}
ApiVersion = Literal{json.dumps(api_version_list)}
ApiSecurityReadData = Literal{json.dumps(literal_lists["Member"]["SecurityReadType"])}
ApiSecurityWriteData = Literal{json.dumps(literal_lists["Member"]["SecurityWriteType"])}
EnumName = Literal{json.dumps(enum_names)}
EnumItemName = Literal{json.dumps(enum_item_names)}

class ApiSecurityData(TypedDict):
	Read: ApiSecurityReadData
	Write: ApiSecurityWriteData

class ApiSerializationData(TypedDict):
	CanLoad: bool
	CanSave: bool

class ApiValueTypeData(TypedDict):
	Category: ApiValueCategory
	Name: ApiValueTypeName

class ApiMemberData(TypedDict):
	MemberType: ApiMemberType
	Name: str
	ThreadSafety: ApiThreadSafety

class ApiPropertyMemberData(ApiMemberData):
	Category: ApiPropertyCategory
	Serialization: ApiSerializationData
	Security: ApiSecurityData | Literal{json.dumps(literal_lists["Member"]["SecurityReadType"])}
	Tags: list[ApiPropertyTag] | None
	ValueType: ApiValueTypeData

class ApiVariableData(TypedDict):
	Name: str
	Type: ApiValueTypeData
	Default: str | None

class ApiEventMemberData(TypedDict):
	Parameters: list[ApiVariableData]

class ApiFunctionCallbackMemberData(ApiEventMemberData):
	ReturnType: ApiVariableData

class ApiClassData(TypedDict):
	Members: Union[list[ApiFunctionCallbackMemberData], list[ApiPropertyMemberData], list[ApiEventMemberData]]
	MemoryCategory: ApiMemoryCategory
	Superclass: str
	Tags: list[ApiClassTag] | None

class ApiEnumItemData(TypedDict):
	Value: int
	Name: str

class ApiEnumData(TypedDict):
	Items: list[ApiEnumItemData]
	Name: str

class ApiData(TypedDict):
	Classes: list[ApiClassData]
	Enums: list[ApiEnumData]
	Version: ApiVersion

class BaseMemberData(TypedDict):
	name: str
	is_replicated: bool
	is_hidden: bool
	is_deprecated: bool
	is_browsable: bool
	is_scriptable: bool

class ParameterData(TypedDict):
	name: str
	type: str

class PropertyData(BaseMemberData):
	Type: str

class FunctionData(BaseMemberData):
	is_yielding: bool
	is_custom_lua_state: bool
	can_yield: bool
	parameters: list[ParameterData]
	return_type: str

class EventData(TypedDict):
	parameters: list[ParameterData]

class InstanceData(TypedDict):
	name: ApiClassTypeName
	path: str
	is_creatable: bool
	is_browsable: bool
	is_deprecated: bool
	properties: dict[str, PropertyData]
	functions: dict[str, FunctionData]
	events: dict[str, EventData]

""" + enum_content + """

API_DATA: ApiData = requests.get(
	url = "https://raw.githubusercontent.com/CloneTrooper1019/Roblox-Client-Tracker/roblox/API-Dump.json",
	params = {}
).json()

def get_instance_data(
	apply_inheritance=True,
	include_services=False,
	include_deprecated_instances=False,
	include_non_creatable_instances=False,
	include_non_browsable_instances=False, 
	include_deprecated_properties=False,
	include_non_scriptable_properties=False,
) -> dict[ApiClassTypeName, InstanceData]:
	api_data = deepcopy(API_DATA)
	out_data = {}
	for class_data in api_data["Classes"]:
		class_name = class_data["Name"]
		property_data_registry = {}
		event_data_registry = {}
		function_data_registry = {}

		for member_data in class_data["Members"]:
			if "MemberType" in member_data:
				member_type = member_data["MemberType"]
				member_name = member_data["Name"]
				is_replicated = False
				is_hidden = False
				is_deprecated = False
				is_browsable = False
				is_scriptable = False
					
				if "Tags" in member_data:
					is_replicated = not "NotReplicated" in member_data["Tags"]
					is_hidden = "Hidden" in member_data["Tags"]
					is_deprecated = "Deprecated" in member_data["Tags"]
					is_browsable = not "NotBrowsable" in member_data["Tags"]
					is_scriptable = not "NotScriptable" in member_data["Tags"]

				if member_type == "Property":
					
					property_data: PropertyData = {
						"name": member_name,
						"is_replicated": is_replicated,
						"is_hidden": is_hidden,
						"is_deprecated": is_deprecated,
						"is_browsable": is_browsable,
						"is_scriptable": is_scriptable,
						"type": member_data["ValueType"]["Name"],
					}

					property_data_registry[property_data["name"]] = property_data

				elif member_type == "Event" or member_type == "Function" or member_type == "Callback":
		
					params: list[ParameterData] = []

					for param_data in member_data["Parameters"]:
						var_name = param_data["Name"]
						type_name = param_data["Type"]["Name"]
					
						if "Default" in param_data:
							type_name += "?"

						params.append({
							"name": var_name,
							"type": type_name
						})

					if member_type == "Function" or member_type == "Callback":
						
						is_yielding = False

						is_custom_lua_state = False
						can_yield = False
						if "Tags" in member_data:
							is_custom_lua_state = "CustomLuaState" in member_data["Tags"]
							can_yield = "CanYield" in member_data["Tags"]
							if "Yields" in member_data["Tags"]:
								is_yielding = True
								if "NoYield" in member_data["Tags"]:
									raise ValueError(f"somehow yields and no-yield co-exist in the same member: {class_name}.{member_name}")
					
						return_type_name = "nil"

						if "Type" in member_data["ReturnType"]:
							return_type_name = member_data["ReturnType"]["Type"]

						function_data: FunctionData = {
							"name": member_name,
							"is_replicated": is_replicated,
							"is_hidden": is_hidden,
							"is_deprecated": is_deprecated,
							"is_browsable": is_browsable,
							"is_scriptable": is_scriptable,
							"is_yielding": is_yielding,
							"is_custom_lua_state": is_custom_lua_state,
							"can_yield": can_yield,
							"parameters": params,
							"return_type": return_type_name,
						}

						function_data_registry[function_data["name"]] = function_data

					elif member_type == "Event":
						event_data: EventData = {
							"name": member_name,
							"is_replicated": is_replicated,
							"is_hidden": is_hidden,
							"is_deprecated": is_deprecated,
							"is_browsable": is_browsable,
							"is_scriptable": is_scriptable,
							"parameters": params,
						}
						event_data_registry[event_data["name"]] = event_data

		is_creatable = False
		is_browsable = False
		is_deprecated = False
		is_service = False
		is_replicated = False
		is_player_replicated = False
		is_settings = False
		is_user_settings = False

		if "Tags" in class_data:
			is_creatable = not "NotCreatable" in class_data["Tags"]
			is_browsable = not "NotBrowsable" in class_data["Tags"]
			is_deprecated = "Deprecated" in class_data["Tags"]
			is_service = "Service" in class_data["Tags"]
			is_replicated = not "NotReplicated" in class_data["Tags"]
			is_player_replicated = "PlayerReplicated" in class_data["Tags"]
			is_settings = "Settings" in class_data["Tags"]
			is_user_settings = "UserSettings" in class_data["Tags"]

		instance_data: InstanceData = {
			"name": class_name,
			"path": class_name,
			"super_class": class_data["Superclass"],
			"is_creatable": is_creatable,
			"is_browsable": is_browsable,
			"is_deprecated": is_deprecated,
			"is_service": is_service,
			"is_replicated": is_replicated,
			"is_player_replicated": is_player_replicated,
			"is_settings": is_settings,
			"is_user_settings": is_user_settings,
			"properties": property_data_registry,
			"functions": function_data_registry,
			"events": event_data_registry,
		}
		out_data[instance_data["name"]] = instance_data

	def write_inheritance(super_class_name="<<<ROOT>>>"):
		if super_class_name == "<<<ROOT>>>":
			for class_name, class_data in out_data.items():
				if class_data["super_class"] == super_class_name:
					write_inheritance(class_name)
		else:
			super_class = out_data[super_class_name]
			for class_name, class_data in out_data.items():
				if class_data["super_class"] == super_class_name:
					
					class_data["path"] = super_class["path"] + "/" + class_name
					if class_data["path"][0] == "/":
						class_data["path"] = class_data["path"][1:]

					if apply_inheritance:
						for prop_name, prop_val in super_class["properties"].items():
							if not prop_name in class_data["properties"]:
								class_data["properties"][prop_name] = deepcopy(prop_val)
					
						for event_name, event_val in super_class["events"].items():
							if not event_name in class_data["events"]:
								class_data["events"][event_name] = deepcopy(event_val)
					
						for func_name, func_val in super_class["functions"].items():
							if not func_name in class_data["functions"]:
								class_data["functions"][func_name] = deepcopy(func_val)

					write_inheritance(class_name)
	
	write_inheritance()

	final_out = {}
	for inst_name, inst_data in out_data.items():
		if inst_data["is_creatable"] or include_non_creatable_instances:
			if not inst_data["is_deprecated"] or include_deprecated_instances:
				if not inst_data["is_service"] or include_services:
					if not inst_data["is_browsable"] or include_non_browsable_instances:
						final_inst_data = deepcopy(inst_data)
						final_inst_data["properties"] = {}
						final_inst_data["events"] = {}
						final_inst_data["functions"] = {}

						for prop_name, prop_val in inst_data["properties"].items():
							if prop_val["is_scriptable"] or include_non_scriptable_properties:
								if not prop_val["is_deprecated"] or include_deprecated_properties:
									final_inst_data["properties"][prop_name] = prop_val

						for event_name, event_val in inst_data["events"].items():
							if event_val["is_scriptable"] or include_non_scriptable_properties:
								if not event_val["is_deprecated"] or include_deprecated_properties:
									final_inst_data["events"][event_name] = event_val
						
						for func_name, func_val in inst_data["functions"].items():
							if func_val["is_scriptable"] or include_non_scriptable_properties:
								if not func_val["is_deprecated"] or include_deprecated_properties:
									final_inst_data["functions"][func_name] = func_val
		
						final_out[inst_name] = final_inst_data
		
	return final_out

def get_enum_items(enum_name: EnumName) -> list[EnumItemName]:
	return deepcopy(ENUM_TREE[enum_name])

# with open("instance_text.json", "w") as file:
# 	file.write(json.dumps(get_instance_data(), indent=5))
""")

build()
from _typeshed import Incomplete
from tempfile import TemporaryDirectory as TemporaryDirectory
from typing import Literal, TypedDict, Union

ApiMemoryCategory: Incomplete
ApiPropertyTag: Incomplete
ApiClassTag: Incomplete
ApiPropertyCategory: Incomplete
ApiMemberType: Incomplete
ApiThreadSafety: Incomplete
ApiValueCategory: Incomplete
ApiValueTypeName: Incomplete
ApiClassTypeName: Incomplete
ApiVersion: Incomplete
ApiSecurityReadData: Incomplete
ApiSecurityWriteData: Incomplete
EnumName: Incomplete
EnumItemName: Incomplete

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
    Security: ApiSecurityData | Literal['None', 'LocalUserSecurity', 'PluginSecurity', 'RobloxScriptSecurity', 'RobloxSecurity']
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

ENUM_TREE: Incomplete
API_DATA: ApiData

def get_instance_data(apply_inheritance: bool = ..., include_services: bool = ..., include_deprecated_instances: bool = ..., include_non_creatable_instances: bool = ..., include_non_browsable_instances: bool = ..., include_deprecated_properties: bool = ..., include_non_scriptable_properties: bool = ...) -> dict[ApiClassTypeName, InstanceData]: ...
def get_enum_items(enum_name: EnumName) -> list[EnumItemName]: ...

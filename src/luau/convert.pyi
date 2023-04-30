READ_STR_AS_LITERAL_PREFIX: str
READ_STR_AS_LITERAL_SUFFIX: str

def get_if_literal(value: str): ...
def from_list(value: list, indent_count: int = ..., add_comma_at_end: bool = ..., multi_line: bool = ..., skip_initial_indent: bool = ...): ...
def from_dict(value: dict, indent_count: int = ..., add_comma_at_end: bool = ..., multi_line: bool = ..., skip_initial_indent: bool = ...): ...
def from_dict_to_type(type_value: dict, indent_count: int = ..., add_comma_at_end: bool = ..., multi_line: bool = ..., skip_initial_indent: bool = ...) -> str: ...
def from_any(value: int | str | None | float | dict | list = ..., indent_count: int = ..., add_comma_at_end: bool = ..., multi_line: bool = ..., skip_initial_indent: bool = ...) -> str: ...
def mark_as_literal(text: str) -> str: ...

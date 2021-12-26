from copy import copy
from collections import OrderedDict, namedtuple
import enum
import math
from types import ModuleType
from typing import Callable, Union, Generator, List, Dict, Iterable

import dict_tree.boxes as boxes
import dict_tree.exceptions as exceptions

NON_VALUE_TYPES = (
                    dict,
                    list,
                    tuple,
                    # Generator,
                    # type,
                    # ModuleType,
                )

DICTIONARY_TREELINE_TEMPLATE = OrderedDict(
    {
        "type": \
            lambda obj: type(obj).__name__,
        "value": \
            lambda obj: str(obj) if (
                not isinstance(
                    obj,
                    NON_VALUE_TYPES
                )
            ) else "",
    }
)

GUESS_NAME_BY_TYPE = OrderedDict(
    {
        ModuleType:lambda obj: f"Python Module [{obj.__name__}]",
        type:lambda obj: f"Object Class [{obj.__name__}]",
        "default":lambda obj: f"Instance of [{type(obj).__name__}] at address [0x{id(obj):x}]",
    }
)

IGNORE_STANDARD_TYPES = (
    type,
    ModuleType,
)

IGNORE_NO_TYPES = tuple()


class LineType(enum.Enum):
    INDENT_ONLY = enum.auto()
    SCALAR = enum.auto()
    TREE_BRANCH_BOTTOM = enum.auto()
    TREE_LIST_ITEM = enum.auto()

class DictionaryTree():
    line_buffer = None
    max_lengths = None

    TreeLine = namedtuple("TreeLine",(
        "box_lines",
        "name",
        "type",
        "value"
    ))

    def __init__(
        self,
        obj,
        name:str="",
        box:boxes.Box=boxes.ThinBox,
        indent:int=6,
        ignore_types:Iterable[type]=IGNORE_STANDARD_TYPES,
        echo:bool=True,
    ):
        self.reset_lines()
        self.build_lines(
            obj,
            name=name,
            box=box,
            indent=indent,
            ignore_types=ignore_types,
        )

        if (echo):
            self.render(
                box=box,
                echo=echo,
            )

    def reset_lines(
        self,
    ):
        # Reset variables
        self.line_buffer = []
        self.max_lengths = OrderedDict({
            # We don't need a max_length for box_lines - they are merged together with name.
            _key:0 for _key in self.TreeLine._fields
        })

    def guess_name(
        self,
        obj,
        converter = GUESS_NAME_BY_TYPE,
    ):
        _default = converter["default"]

        for _type in converter:
            if (isinstance(_type, type)):
                if (isinstance(obj, _type)):
                    return converter[_type](obj)
        
        return _default(obj)

    def build_lines(
        self,
        obj,
        name:str="",
        box:boxes.Box=boxes.ThinBox,
        is_last_item:bool=True,
        layers:tuple=(),
        indent:int=6,
        ignore_types:Iterable[type]=IGNORE_STANDARD_TYPES,
    )->None:

        # Work out a name if its the base object with no name
        if (not(name) and not(layers)):
            name = self.guess_name(obj)

        # Branch out into 3 cases:
        # - dict
        # - list
        # - scalar

        # ============================================================================================================
        # Treat as DICT
        if (
            (
                isinstance(obj, dict) or \
                (
                    hasattr(obj, "__dict__") and \
                    not isinstance(obj, (list, tuple)) # Weirdly if you subclass a tuple without adding anything, __dict__ will now exist in its instances. We have to make sure that any tuples that goes through are namedtuples only.
                ) or \
                (
                    isinstance(obj, tuple) and \
                    hasattr(obj, "_fields") and \
                    hasattr(obj, "_asdict")         # collections.namedtuple
                )
            ) and not (
                # Print as scalar if:
                #   either
                #       This is the root object or
                #       The object is in ignore_types
                isinstance(obj, ignore_types) and \
                layers
            )
        ):

            if (isinstance(obj, dict)) :
                _dict = obj
            # collections.namedtuple; see if statement above.
            elif (isinstance(obj, tuple)):
                _dict = obj._asdict()
            else:
                _dict = obj.__dict__

            self.add_line(
                self.build_line(
                    obj=obj,
                    name=str(name),
                    box=box,
                    line_type=LineType.TREE_BRANCH_BOTTOM if (len(_dict)>0) else LineType.SCALAR,
                    is_last_item=is_last_item,
                    layers=layers,
                    indent=indent,
                )
            )

            for _id, _key, _value in zip(range(len(_dict)), _dict, _dict.values()):
                _tail_of_dict = (_id+1 >= len(_dict))

                # Call itself to create any sub-lines
                self.build_lines(
                    obj=_value,
                    name=str(_key),
                    box=box,
                    is_last_item=_tail_of_dict,
                    layers=(*layers, not is_last_item),
                    indent=indent,
                )

        # ============================================================================================================
        # Treat as LIST
        elif (
            isinstance(obj, (
                list,
                tuple,
                Generator
                )
            ) and not (
                # Print as scalar if:
                #   either
                #       This is the root object or
                #       The object is in ignore_types
                isinstance(obj, ignore_types) and \
                layers
            )
        ):  

            # Make a copy of the object before listing - prevents Generator from being consumed
            _list = list(copy(obj))

            self.add_line(
                self.build_line(
                    obj=copy(obj),
                    name=str(name),
                    box=box,
                    line_type=LineType.TREE_BRANCH_BOTTOM if (len(_list)>0) else LineType.SCALAR,
                    is_last_item=is_last_item,
                    layers=layers,
                    indent=indent,
                )
            )

            _list_padding = math.ceil(math.log10(max(1,len(_list))))
            for _id, _value in enumerate(_list):
                _tail_of_list = (_id+1 >= len(_list))

                # Call itself to create any sub-lines
                self.build_lines(
                    obj=_value,
                    name=f"[{_id:{_list_padding}}]",
                    box=box,
                    is_last_item=_tail_of_list,
                    layers=(*layers, not is_last_item),
                    indent=indent,
                )
        
        # ============================================================================================================
        # Treat as SCALAR
        else:

            # Just a singular Scalar object
            _scalar = obj

            self.add_line(
                self.build_line(
                    obj=_scalar,
                    name=str(name),
                    box=box,
                    line_type=LineType.SCALAR,
                    is_last_item=is_last_item,
                    layers=layers,
                    indent=indent,
                )
            )

    def build_line(
        self,
        obj,
        name:str,
        template:"OrderedDict[str,Callable]"=DICTIONARY_TREELINE_TEMPLATE,
        box:boxes.Box=boxes.ThinBox,
        line_type:LineType=LineType.INDENT_ONLY,
        is_last_item:bool=False,
        layers:tuple=(),
        indent:int=6,
    )->TreeLine:
        BOX_SPACE               = box.BOX_SPACE.value
        BOX_HORIZONTAL          = box.BOX_HORIZONTAL.value
        BOX_VERTICAL            = box.BOX_VERTICAL.value
        BOX_ANGLE_TOP_RIGHT     = box.BOX_ANGLE_TOP_RIGHT.value
        BOX_VBRANCH_TO_RIGHT    = box.BOX_VBRANCH_TO_RIGHT.value
        BOX_HBRANCH_TO_BOTTOM   = box.BOX_HBRANCH_TO_BOTTOM.value
        BOX_LIST_ITEM           = box.BOX_LIST_ITEM.value
        BOX_BASE_ITEM           = box.BOX_BASE_ITEM.value
        LINE_BREAK              = box.LINE_BREAK.value

        # Generating box_lines
        _tree_indent = "".join([
            (BOX_VERTICAL if (_layer) else BOX_SPACE) + max(0, indent-1)*BOX_SPACE \
                for _layer in layers
        ])

        if (layers):
            # If this is a branch, select the branch depending on whether its the last item
            _branch_char = BOX_ANGLE_TOP_RIGHT if (is_last_item) else BOX_VBRANCH_TO_RIGHT
        else:
            # If this is the base object, don't show any branch
            _branch_char = BOX_BASE_ITEM

        _tree_indent_only = _tree_indent
        _tree_scalar = _tree_indent + _branch_char + max(1, indent)*BOX_HORIZONTAL + BOX_SPACE
        _tree_parent = _tree_indent + _branch_char + max(0, indent-1)*BOX_HORIZONTAL + BOX_HBRANCH_TO_BOTTOM + BOX_SPACE
        _tree_list_item = _tree_indent + BOX_SPACE*max(0, indent-2) + BOX_LIST_ITEM + BOX_SPACE

        if (line_type is LineType.INDENT_ONLY):
            _box_lines = _tree_indent_only
        elif (line_type is LineType.SCALAR):
            _box_lines = _tree_scalar
        elif (line_type is LineType.TREE_BRANCH_BOTTOM):
            _box_lines = _tree_parent
        elif (line_type is LineType.TREE_LIST_ITEM):
            _box_lines = _tree_list_item

        _name = name

        return self.TreeLine(
            box_lines=_box_lines,
            name=_name,
            **{
                _key:_func(obj) \
                    for _key, _func in zip(template, template.values())
            }
        )


    def add_line(
        self,
        line,
    )->None:
        if (isinstance(line, self.TreeLine)):
            self.line_buffer.append(line)
            self.max_lengths["name"] = max(
                self.max_lengths["name"],
                len(line.box_lines)+len(line.name),
            )

            for _key in (set(("box_lines","name")) ^ set(self.TreeLine._fields)):
                self.max_lengths[_key] = max(
                    self.max_lengths[_key],
                    len(getattr(line, _key, 0)),
                )

    def render(
        self,
        box:boxes.Box=boxes.ThinBox,
        echo:bool=False,
    )->str:
        _lines = []

        LINE_BREAK = box.LINE_BREAK.value

        for _line in self.line_buffer:

            # Dynamically adjust how long the box_lines+name field is for each line.
            max_lengths = self.max_lengths.copy()
            max_lengths["name"] -= len(_line.box_lines)

            # Generate template
            template_string = "".join(
                [
                    # What this is doing:
                    #       create a format string like {box_lines}{name:16s}{type:8s}{value}
                    # in which all the fields (box_lines, names, ...) are all fields of self.TreeLine.
                    # We can then use this string to template_string.format(**line._asdict())
                    #   to create the line we needed.
                    #
                    # Note:
                    # - box_lines is a special field which always has a max_lengths["box_lines"] of 0. self.add_line ignore that field.
                    # - The if statement takes care of:
                    #   - don't specify a {:{max_length}s} if max_length is 0. This can be removed; but retained in case of change in Python behaviour.
                    #   - the last field, whatever it is, does not need a length.
                    f"{{{_formatter}{(':'+str(max_lengths[_formatter]+4)+'s') if (max_lengths[_formatter] and _field_id+1<len(self.TreeLine._fields)) else ''}}}" \
                        for _field_id, _formatter in enumerate(self.TreeLine._fields)
                ]
            )
            
            _lines.append(
                template_string.format(
                    **_line._asdict(),
                )
            )
            
        _return = LINE_BREAK.join(
            _lines
        )

        if (echo):
            print (_return)

        return _return

    __str__ = render


if __name__=="__main__":
    _sample_dict = [
        {
            "name": "power_singlefield_with_unit",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "s_farbe_kombifeld",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "t_productfeature",
            "type": "RECORD",
            "mode": "REPEATED",
            "fields": [
                {
                    "name": "ID",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                {
                    "name": "Kurztext",
                    "type": "STRING",
                    "mode": "NULLABLE"
                },
                {
                    "name": "Text",
                    "type": "STRING",
                    "mode": "NULLABLE",
                    "fields": [
                        {
                            "name": "ID",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "Kurztext",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        },
                        {
                            "name": "Text",
                            "type": "STRING",
                            "mode": "NULLABLE"
                        }
                    ]
                }
            ]
        },
        {
            "name": "s_montageart",
            "type": "STRING",
            "mode": "NULLABLE"
        },

    ]
    _dict_tree = DictionaryTree(_sample_dict, echo=False, box=boxes.ThickBox,)

    print (_dict_tree)
    
    # DictionaryTree(math, echo=True, box=boxes.DoubleBox)


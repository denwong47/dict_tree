from enum import Enum

class Box(Enum):
    pass

#================================================================================================

class ThinBox(Box):
    BOX_SPACE = u" "
    BOX_HORIZONTAL = u"\u2500"
    BOX_VERTICAL = u"\u2502"
    BOX_ANGLE_TOP_RIGHT = u"\u2514"
    BOX_VBRANCH_TO_RIGHT = u"\u251C"
    BOX_HBRANCH_TO_BOTTOM = u"\u252C"
    BOX_LIST_ITEM = u"\u2576"
    BOX_BASE_ITEM = u"\u257E"
    LINE_BREAK = u"\n"

class ThickBox(Box):
    BOX_SPACE = u" "
    BOX_HORIZONTAL = u"\u2501"
    BOX_VERTICAL = u"\u2503"
    BOX_ANGLE_TOP_RIGHT = u"\u2517"
    BOX_VBRANCH_TO_RIGHT = u"\u2523"
    BOX_HBRANCH_TO_BOTTOM = u"\u2533"
    BOX_LIST_ITEM = u"\u257A"
    BOX_BASE_ITEM = BOX_HORIZONTAL
    LINE_BREAK = u"\n"

class DoubleBox(Box):
    BOX_SPACE = u" "
    BOX_HORIZONTAL = u"\u2550"
    BOX_VERTICAL = u"\u2551"
    BOX_ANGLE_TOP_RIGHT = u"\u255A"
    BOX_VBRANCH_TO_RIGHT = u"\u2560"
    BOX_HBRANCH_TO_BOTTOM = u"\u2566"
    BOX_LIST_ITEM = u"\u2576"
    BOX_BASE_ITEM = BOX_HORIZONTAL
    LINE_BREAK = u"\n"



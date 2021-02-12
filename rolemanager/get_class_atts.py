from typing import Class, Dict, List


def get_class_attributes(class_obj: Class, att_of_interest: List[str]) -> Dict:
    """
    Get attributes of a given class.
    """

    _class_dict = class_obj.__dict__
    return [(class_att, class_val) for (class_att, class_val) in _class_dict.items()
            if class_att in att_of_interest]

from typing import Dict, List, Union


def create_response(data: Dict, status_code: int, message: str = None) -> Dict:
    response_dict = {}
    response_dict["data"] = data
    if message:
        response_dict["message"] = message
    response_dict["code"] = status_code

    return response_dict, status_code

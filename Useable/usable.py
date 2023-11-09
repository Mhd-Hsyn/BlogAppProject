"""
Modeule : useable.py
"""
def check_pass_len(passwprd):
    """
    check password lenth
    """
    if len(passwprd) < 8:
        return False
    return True

def require_field_validation(requestdata, requirefield):
    """
    check if any field is missing or empty
    """
    requie_field = []
    unfilled_field = []

    for filed in requirefield:
        if filed not in requestdata:
            requie_field.append(filed)
        
        if filed in requestdata:
            if len(requestdata[filed]) == 0:
                unfilled_field.append(filed)

    message = {
        "status": not requie_field and not unfilled_field,
        "require_field": requie_field,
        "empty_fields": unfilled_field
    }

    return message


import visugraph.py3.runner as py3

def get_trace(json_data):
    '''
    Returns the trace as a json object from json_data
    json_data is the data (as a dictionary) passed from the front end.
    It should have the properties
        'code': the user's code as a string
        'lang': the user's language, which can be:
            'python3'
    '''
    print('getting trace {}'.format(json_data))
    if 'code' not in json_data:
        return ''
    code = json_data['code']
    # lang = json_data['lang']
    lang = 'python3'
    if lang == 'python3':
        return py3.get_trace(code)
    return ''
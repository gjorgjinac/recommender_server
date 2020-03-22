def call_protected(circuit_breaker,  default_data,protected_function, *protected_function_args):
    try:
        data = protected_function(*protected_function_args)
    except Exception:
        pass
    if circuit_breaker.current_state == 'open':
        print('defaulting')
        data = default_data
    print(data)
    return data
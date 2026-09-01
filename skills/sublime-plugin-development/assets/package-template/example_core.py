def greeting(name):
    normalized = name.strip()
    return "Hello, {}.".format(normalized or "workspace")

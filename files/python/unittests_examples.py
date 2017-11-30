def read_file_example(file_name):
    with open(file_name, "r") as f:
        file_contents = f.read()
    return(file_contents)

def write_file_example(file_name, file_data):
    with open(file_name, "w") as f:
        f.write(file_data)
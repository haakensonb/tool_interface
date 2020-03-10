def append_to_file(text, filename):
    with open(filename, "a") as f:
        f.write(text)

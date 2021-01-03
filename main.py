import json
import sys
import getopt


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def to_go_struct(obj):
    struct_string = ""
    for key, value in obj.items():
        camel_key = to_camel_case(key)
        value_type = ""
        if isinstance(value, list):
            value = value[0]
            value_type = "[]"
        if isinstance(value, bool):
            value_type += "bool"
        elif isinstance(value, str):
            value_type += "string"
        elif isinstance(value, float):
            value_type += "float64"
        elif isinstance(value, int):
            value_type += "int"
        elif isinstance(value, dict):
            value_type += "struct { \n"
            a = to_go_struct(value)
            value_type += "{}}}".format(a)
        else:
            value_type += "*map[string]interface{}"

        struct_string += '{} {} `json:"{}"`\n'.format(camel_key, value_type, key)
    return struct_string


if __name__ == "__main__":
    file_name = ""
    destination_file = ""
    name = ""
    package_name = ""

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv, "f:d:n:p:", ["filename=", "destination=", "name=", "package_name="]
        )
    except getopt.GetoptError:
        print(
            "main.py -f <filename> -d <destination_file> -n <struct_name> -p <package_name>"
        )
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-f", "--filename"]:
            filename = arg
        elif opt in ["-d", "--destination"]:
            destination_file = arg
        elif opt in ["-n", "--name"]:
            name = arg
        elif opt in ["-p", "--package_name"]:
            package_name = arg

    json_file = open(filename)
    obj = json.load(json_file)

    struct = """package {}
    
    type {} struct {{
    """.format(
        package_name, name
    )
    struct += to_go_struct(obj)
    struct += "}"
    f = open(destination_file, "w")
    f.write(struct)
    f.close()

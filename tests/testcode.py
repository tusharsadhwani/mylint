# type: ignore

s = {1, 2}  # Unused global
l = [1, 2, 3, 1, 2, 3]


def main():
    var = 5  # Unused local
    for item in l:
        methods = {
            "GET",
            "PUT",
            "POST",
            "DELETE",
            "PUT",  # Duplicate
        }
        if item in methods:
            print(item)


s2 = {1, 2, 3, 1}  # Unused, and has a duplicate
var = 7
print(var)

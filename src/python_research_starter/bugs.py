"""A script with many issues."""

def create_personalized_print_functions(list=["tom", "rishabh"]):
    """Create print functions for the given people listed."""
    # Capitalize the names first.
    new_list = []
    while list:
        name = list.pop(0)
        new_list.append(name.capitalize())
    # Create the functions.
    funcs = []
    for name in new_list:
        def print_fn(x):
            print(name + " says " + x)
        funcs.append(print_fn)
    return list(funcs)

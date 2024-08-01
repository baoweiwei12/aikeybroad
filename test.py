import os


def count_lines(directory):
    total_lines = 0
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(subdir, file), "r", encoding="utf-8") as f:
                    total_lines += len(f.readlines())
    return total_lines


project_directory = "./app"
print(f"Total lines of code: {count_lines(project_directory)}")

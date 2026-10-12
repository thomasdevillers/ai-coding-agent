from functions.get_file_content import get_file_content

file_content = get_file_content("calculator", "lorem.txt")
print(file_content[:50])
print(f"lorem.txt length: {len(file_content)}")
print(f"lorem.txt truncated: {'truncated' in file_content}")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
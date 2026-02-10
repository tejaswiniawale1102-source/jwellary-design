# Emergency fix for product_detail.html line 310
file_path = r"c:\Users\Tejaswini\OneDrive\Desktop\RentEasyIndia\templates\product_detail.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken Jinja2 syntax
broken_pattern = "const dailyPrice = {{ product[3] }\n                };"
fixed_pattern = "const dailyPrice = {{ product[3] }};"

if broken_pattern in content:
    content = content.replace(broken_pattern, fixed_pattern)
    print("Found and fixed the broken pattern!")
else:
    print("Pattern not found, checking alternative...")
    # Try alternative pattern with Windows line endings
    broken_pattern2 = "const dailyPrice = {{ product[3] }\r\n                };"
    if broken_pattern2 in content:
        content = content.replace(broken_pattern2, fixed_pattern)
        print("Found and fixed the alternative pattern!")
    else:
        print("Could not find the broken pattern")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully!")

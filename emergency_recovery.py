import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Look for the broken line
for i, line in enumerate(lines):
    if 'const dailyPrice = {{ product[3] }' in line and '}}' not in line:
        print(f"Found broken line at {i+1}: {line.strip()}")
        # Check the next line
        if i + 1 < len(lines) and '};' in lines[i+1]:
            print(f"Found stray closure at {i+2}: {lines[i+1].strip()}")
            # Fix it
            lines[i] = '                    const dailyPrice = {{ product[3] }};\n'
            lines[i+1] = '                    const total = dailyPrice * selectedDays;\n'
            # Also need to check if we accidentally deleted the next few lines
            # In Step 1724, 311 was 'const total = dailyPrice * selectedDays;'
            # and 312 was empty, 313 was rentalSubtotal.
            # Let's just normalize the whole block.
            break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fix applied.")

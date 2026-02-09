import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Clean up the script block (Fixing Step 1733 artifacts)
# Removing the duplicate line 312 and fixing indentation
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if 'const total = dailyPrice * selectedDays;' in line:
        # Check if previous line already had this
        if i > 0 and 'const total = dailyPrice * selectedDays;' in lines[i-1]:
            print(f"Skipping duplicate line at {i+1}")
            continue
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Cleanup complete.")

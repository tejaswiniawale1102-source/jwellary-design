import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the nesting: move the } after the total calculation
wrong_block = """                    const dailyPrice = {{ product[3] }};
                }
                const total = dailyPrice * selectedDays;

                document.getElementById('rentalSubtotal').innerText = `₹${total}`;
                document.getElementById('rentalTotal').innerText = `₹${total}`;"""

correct_block = """                    const dailyPrice = {{ product[3] }};
                    const total = dailyPrice * selectedDays;

                    document.getElementById('rentalSubtotal').innerText = `₹${total}`;
                    document.getElementById('rentalTotal').innerText = `₹${total}`;
                }"""

# Use a more flexible search if needed, but the previous python print showed this exact pattern (mostly)
# Let's just do a safer multi-line replace.

if wrong_block in content:
    content = content.replace(wrong_block, correct_block)
    print("Nesting fixed.")
else:
    # Fallback to a broader search
    print("Could not find exact block, trying a broader replace.")
    content = content.replace('const dailyPrice = {{ product[3] }};\n                }', 'const dailyPrice = {{ product[3] }};')
    # This is risky, let me just rewrite the whole function.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement attempted.")

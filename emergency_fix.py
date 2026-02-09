import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken Jinja tag
content = content.replace('{{ product[3] }', '{{ product[3] }}')

# Fix the stray bracket and calc logic for the flatpickr onClose if it's messed up
content = content.replace('{{ product[3] }}\n                };', '{{ product[3] }};\n                }')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement complete.")

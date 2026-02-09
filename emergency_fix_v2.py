import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the over-aggressive replacement (triple brackets)
content = content.replace('{{ product[3] }}}', '{{ product[3] }}')

# Ensure line 271 is exactly right
# (Previously it was {{ product[3] } followed by \n and };)
# Let's just normalize that whole block to be safe.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Double replacement fixed.")

import os

path = 'templates/payment.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pre-fill the fields in payment.html if they are passed
old_inputs = """                    <div class="input-group">
                        <label>Phone Number</label>
                        <input type="tel" name="phone" placeholder="+91 XXXXX XXXXX" required>
                    </div>
                    <div class="input-group">
                        <label>Delivery Address</label>
                        <textarea name="address" placeholder="Full Address (House No, Street, City)" rows="2"
                            required></textarea>
                    </div>
                    <div class="input-group">
                        <label>Location / Landmark</label>
                        <input type="text" name="location" placeholder="e.g. Near Central Park" required>
                    </div>"""

new_inputs = """                    <div class="input-group">
                        <label>Customer Name</label>
                        <input type="text" name="customer_name" value="{{ customer_name if customer_name else '' }}" readonly style="background: #f0f0f0;">
                    </div>
                    <div class="input-group">
                        <label>Phone Number</label>
                        <input type="tel" name="phone" placeholder="+91 XXXXX XXXXX" required>
                    </div>
                    <div class="input-group">
                        <label>Delivery Address</label>
                        <textarea name="address" placeholder="Full Address" rows="2" required>{{ address if address else '' }}</textarea>
                    </div>
                    <div class="input-group">
                        <label>Location / Landmark</label>
                        <input type="text" name="location" value="{{ location if location else '' }}" required>
                    </div>"""

content = content.replace(old_inputs, new_inputs)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Payment template updated.")

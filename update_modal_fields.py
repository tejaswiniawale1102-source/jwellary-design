import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update handleRentNow to allow single dates (removing the 'to' check)
old_handle_rent = """    function handleRentNow() {
        const dateInput = document.getElementById('datePicker').value;
        if (!dateInput || !dateInput.includes('to')) {
            showToast("Please select a date range first! 📅", "fa-calendar-circle-exclamation");
            return;
        }
        openPaymentModal('{{ product[1] }}', '{{ product[3] }}', '{{ product[4] }}', '{{ product[0] }}', selectedDays);
    }"""

new_handle_rent = """    function handleRentNow() {
        const dateInput = document.getElementById('datePicker').value;
        if (!dateInput) {
            showToast("Please select a date first! 📅", "fa-calendar-circle-exclamation");
            return;
        }
        openPaymentModal('{{ product[1] }}', '{{ product[3] }}', '{{ product[4] }}', '{{ product[0] }}', selectedDays);
    }"""

content = content.replace(old_handle_rent, new_handle_rent)

# 2. Update onClose to handle single date (selectedDates.length === 1 or 2)
old_on_close = """            onClose: function (selectedDates, dateStr, instance) {
                if (selectedDates.length === 2) {
                    const start = selectedDates[0];
                    const end = selectedDates[1];
                    const diffTime = Math.abs(end - start);
                    selectedDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

                    document.getElementById('priceBreakdown').style.display = 'block';
                    document.getElementById('rentalDaysLabel').innerText = `${selectedDays} days`;

                    const dailyPrice = {{ product[3] }};
                    const total = dailyPrice * selectedDays;

                    document.getElementById('rentalSubtotal').innerText = `₹${total}`;
                    document.getElementById('rentalTotal').innerText = `₹${total}`;
                }
            }"""

new_on_close = """            onClose: function (selectedDates, dateStr, instance) {
                if (selectedDates.length >= 1) {
                    if (selectedDates.length === 2) {
                        const start = selectedDates[0];
                        const end = selectedDates[1];
                        const diffTime = Math.abs(end - start);
                        selectedDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
                    } else {
                        selectedDays = 1;
                    }

                    document.getElementById('priceBreakdown').style.display = 'block';
                    document.getElementById('rentalDaysLabel').innerText = `${selectedDays} days`;

                    const dailyPrice = {{ product[3] }};
                    const total = dailyPrice * selectedDays;

                    document.getElementById('rentalSubtotal').innerText = `₹${total}`;
                    document.getElementById('rentalTotal').innerText = `₹${total}`;
                }
            }"""

content = content.replace(old_on_close, new_on_close)

# 3. Add fields to the Modal form
old_modal_form = """        <form action="{{ url_for('user.payment_page') }}" method="POST">
            <input type="hidden" id="modal_product_id" name="product_id">
            <input type="hidden" id="modal_image" name="image">
            <input type="hidden" id="modal_product_name" name="product_name">
            <input type="hidden" id="modal_price" name="price">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 id="display_name"></h3>
                <p style="color: #e91e63; font-size: 1.2rem;">₹<span id="display_price"></span> / day</p>
            </div>
            <label>Rental Duration (Days):</label>
            <input type="number" id="modal_days" name="days" value="1" min="1"
                style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
            <button type="submit"
                style="width: 100%; background-color: #e91e63; color: white; padding: 14px 20px; margin: 8px 0; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">Proceed
                to Payment</button>
        </form>"""

new_modal_form = """        <form action="{{ url_for('user.payment_page') }}" method="POST">
            <input type="hidden" id="modal_product_id" name="product_id">
            <input type="hidden" id="modal_image" name="image">
            <input type="hidden" id="modal_product_name" name="product_name">
            <input type="hidden" id="modal_price" name="price">
            
            <div style="text-align: center; margin-bottom: 15px;">
                <h3 id="display_name" style="color: #333; margin-bottom: 5px;"></h3>
                <p style="color: #ff1f6a; font-size: 1.2rem; font-weight: bold; margin: 0;">₹<span id="display_price"></span> / day</p>
            </div>

            <div style="margin-bottom: 12px;">
                <label style="display:block; font-size: 0.9rem; margin-bottom: 4px;">Customer Name:</label>
                <input type="text" name="customer_name" placeholder="Enter your full name" required 
                       style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: inherit;">
            </div>

            <div style="margin-bottom: 12px;">
                <label style="display:block; font-size: 0.9rem; margin-bottom: 4px;">Delivery Address:</label>
                <textarea name="address" placeholder="Full Address (House, Street, City)" required rows="2"
                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: inherit;"></textarea>
            </div>

            <div style="margin-bottom: 12px;">
                <label style="display:block; font-size: 0.9rem; margin-bottom: 4px;">Location / Landmark:</label>
                <input type="text" name="location" placeholder="e.g. Near Garden Area" required 
                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: inherit;">
            </div>

            <div style="margin-bottom: 20px;">
                <label style="display:block; font-size: 0.9rem; margin-bottom: 4px;">Rental Duration (Days):</label>
                <input type="number" id="modal_days" name="days" value="1" min="1" readonly
                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9; cursor: not-allowed;">
            </div>

            <button type="submit"
                style="width: 100%; background-color: #ff1f6a; color: white; padding: 14px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 10px rgba(255, 31, 106, 0.2);">
                Proceed to Payment
            </button>
        </form>"""

content = content.replace(old_modal_form, new_modal_form)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Product detail enhancements applied.")

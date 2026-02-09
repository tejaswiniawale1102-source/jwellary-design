import os

path = 'templates/product_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Re-construct the script block from line 253 to 311
# To be absolutely sure, I'll replace the entire block with known good code.
start_index = -1
end_index = -1

for i, line in enumerate(lines):
    if '<script>' in line and i > 250:
        start_index = i
    if '</script>' in line and i > start_index:
        end_index = i
        break

if start_index != -1 and end_index != -1:
    new_script = """<script>
    let selectedDays = 1;

    document.addEventListener("DOMContentLoaded", function () {
        flatpickr("#datePicker", {
            mode: "range",
            minDate: "today",
            dateFormat: "Y-m-d",
            onClose: function (selectedDates, dateStr, instance) {
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
            }
        });
    });

    function handleRentNow() {
        const dateInput = document.getElementById('datePicker').value;
        if (!dateInput || !dateInput.includes('to')) {
            showToast("Please select a date range first! 📅", "fa-calendar-circle-exclamation");
            return;
        }
        openPaymentModal('{{ product[1] }}', '{{ product[3] }}', '{{ product[4] }}', '{{ product[0] }}', selectedDays);
    }

    function openPaymentModal(name, price, image, id, days = 1) {
        document.getElementById('modal_product_name').value = name;
        document.getElementById('modal_price').value = price;
        document.getElementById('modal_image').value = image;
        document.getElementById('modal_product_id').value = id;
        document.getElementById('display_name').innerText = name;
        document.getElementById('display_price').innerText = price;
        document.getElementById('modal_days').value = days;
        document.getElementById('paymentModal').style.display = "block";
    }

    function closePaymentModal() {
        document.getElementById('paymentModal').style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == document.getElementById('paymentModal')) {
            closePaymentModal();
        }
    }
</script>
"""
    # Replace lines from start_index to end_index + 1
    lines[start_index:end_index+1] = [new_script]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Script restored successfully.")
else:
    print("Could not find script block.")

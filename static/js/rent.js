function openModal(name, price) {
  document.getElementById("modal").style.display = "flex";
  document.getElementById("productName").innerText = name;
  document.getElementById("productPrice").innerText = "₹" + price + " / day";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}

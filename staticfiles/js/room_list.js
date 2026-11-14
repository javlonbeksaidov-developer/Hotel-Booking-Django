const searchInput = document.getElementById("searchRoom");
const categoryFilter = document.getElementById("categoryFilter");
const priceFilter = document.getElementById("priceFilter");
const resetButton = document.getElementById("resetFilter");

const grid = document.getElementById("roomsGrid");
const emptyMessage = document.getElementById("filterEmpty");

const getCards = () => [...grid.querySelectorAll(".room-card")];

function filterRooms() {
  const search = searchInput.value.toLowerCase().trim();
  const category = categoryFilter.value.toLowerCase();

  getCards().forEach((card) => {
    const name = card.dataset.name;
    const roomCategory = card.dataset.category;

    const matchesSearch = name.includes(search);
    const matchesCategory = !category || roomCategory === category;

    card.style.display = matchesSearch && matchesCategory ? "" : "none";
  });

  const visibleCards = getCards().filter(
    (card) => card.style.display !== "none",
  );

  emptyMessage.style.display = visibleCards.length === 0 ? "block" : "none";
}

function sortRooms() {
  const cards = getCards();
  const sortValue = priceFilter.value;

  if (!sortValue) return;

  cards.sort((a, b) => {
    const priceA = Number(a.dataset.price);
    const priceB = Number(b.dataset.price);

    return sortValue === "low" ? priceA - priceB : priceB - priceA;
  });

  cards.forEach((card) => grid.insertBefore(card, emptyMessage));

  filterRooms();
}

searchInput.addEventListener("input", filterRooms);
categoryFilter.addEventListener("change", filterRooms);
priceFilter.addEventListener("change", sortRooms);

resetButton.addEventListener("click", () => {
  searchInput.value = "";
  categoryFilter.value = "";
  priceFilter.value = "";

  getCards().forEach((card) => {
    card.style.display = "";
  });

  emptyMessage.style.display = "none";
});

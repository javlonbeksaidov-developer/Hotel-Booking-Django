const filters = document.getElementById("filters");
const roomGrid = document.getElementById("roomGrid");

const category = document.getElementById("fCat");
const price = document.getElementById("fPrice");
const priceOutput = document.getElementById("fPriceOut");
const guests = document.getElementById("fGuests");
const sort = document.getElementById("fSort");
const available = document.getElementById("fAvail");
const noRooms = document.getElementById("noRooms");

function filterRooms() {
  const cards = [...roomGrid.querySelectorAll(".room-card")];

  const selectedCategory = category.value;
  const maxPrice = Number(price.value);
  const minGuests = Number(guests.value);

  priceOutput.value = maxPrice;

  cards.forEach((card) => {
    const cardCategory = card.dataset.category;
    const cardPrice = Number(card.dataset.price);
    const cardGuests = Number(card.dataset.guests);
    const cardAvailable = card.dataset.available === "1";

    const categoryMatch =
      selectedCategory === "all" || cardCategory === selectedCategory;

    const priceMatch = cardPrice <= maxPrice;
    const guestsMatch = cardGuests >= minGuests;
    const availabilityMatch = !available.checked || cardAvailable;

    card.hidden = !(
      categoryMatch &&
      priceMatch &&
      guestsMatch &&
      availabilityMatch
    );
  });

  noRooms.hidden = cards.some((card) => !card.hidden);
}

function sortRooms() {
  const cards = [...roomGrid.querySelectorAll(".room-card")];

  if (sort.value === "asc") {
    cards.sort((a, b) => Number(a.dataset.price) - Number(b.dataset.price));
  } else if (sort.value === "desc") {
    cards.sort((a, b) => Number(b.dataset.price) - Number(a.dataset.price));
  }

  cards.forEach((card) => roomGrid.appendChild(card));

  filterRooms();
}

category.addEventListener("change", filterRooms);
price.addEventListener("input", filterRooms);
guests.addEventListener("change", filterRooms);
available.addEventListener("change", filterRooms);
sort.addEventListener("change", sortRooms);

filters.addEventListener("submit", function (e) {
  e.preventDefault();
});

filterRooms();

const giftsContainer = document.getElementById("gifts");
const openedCountEl = document.getElementById("opened-count");
const resultEl = document.getElementById("result");
const dedBtn = document.getElementById("ded-moroz-btn");

const TOTAL_GIFTS = 10;

function makeGift(id) {
  const gift = document.createElement("div");
  gift.className = "gift";
  gift.innerText = "🎁";
  gift.dataset.id = String(id);
  gift.addEventListener("click", () => openGift(id, gift));
  return gift;
}

function markOpened(giftEl) {
  giftEl.classList.add("opened");
  giftEl.innerText = "✅";
}

function markAuthOnly(giftEl) {
  // визуальная подсказка, что подарок "закрыт"
  giftEl.style.opacity = "0.7";
  giftEl.title = "Только для авторизованных";
}

async function loadState() {
  const res = await fetch("/lab9/state");
  const data = await res.json();

  if (!data.ok) return;

  openedCountEl.textContent = String(data.opened_count);

  // отрисовка подарков
  giftsContainer.innerHTML = "";
  for (let i = 1; i <= TOTAL_GIFTS; i++) {
    const giftEl = makeGift(i);

    // если подарок уже пустой (общий) — показываем как открытый
    if (data.empty_gifts.includes(i)) {
      markOpened(giftEl);
    }

    // если подарок только для авторизованных и пользователь не авторизован
    if (!data.authed && data.auth_only_gifts.includes(i)) {
      markAuthOnly(giftEl);
    }

    giftsContainer.appendChild(giftEl);
  }
}

async function openGift(id, giftEl) {
  // если уже открыт на клиенте
  if (giftEl.classList.contains("opened")) return;

  const res = await fetch("/lab9/open", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });

  const data = await res.json();

  if (!res.ok || !data.ok) {
    resultEl.innerHTML = `⛔ ${data.error || "Ошибка"}`;
    return;
  }

  markOpened(giftEl);
  openedCountEl.textContent = String(data.opened_count);
  resultEl.innerHTML = `<strong>Подарок #${data.gift_id}</strong>: ${data.wish}`;
}

async function resetGifts() {
  const res = await fetch("/lab9/reset", { method: "POST" });
  const data = await res.json();

  if (!res.ok || !data.ok) {
    resultEl.innerHTML = `⛔ ${data.error || "Ошибка"}`;
    return;
  }

  resultEl.innerHTML = "🎅 Дед Мороз наполнил все коробки заново!";
  await loadState(); // перерисовать состояние
}

if (dedBtn) {
  dedBtn.addEventListener("click", resetGifts);
}

loadState();

let currentMode = 'add'; // 'add' | 'edit'
let currentId = null;

const tbody = document.getElementById('films-tbody');
const addBtn = document.getElementById('add-film-btn');

const modal = document.getElementById('film-modal');
const modalTitle = document.getElementById('modal-title');
const saveBtn = document.getElementById('save-btn');
const cancelBtn = document.getElementById('cancel-btn');

const errorBox = document.getElementById('error-message');

const inputTitleRu = document.getElementById('title_ru');
const inputTitle = document.getElementById('title');
const inputYear = document.getElementById('year');
const inputDescription = document.getElementById('description');


function showError(text) {
  if (!text) {
    errorBox.style.display = 'none';
    errorBox.innerHTML = '';
    return;
  }
  errorBox.innerHTML = text;
  errorBox.style.display = 'block';
}

function clearErrorOnShowModal() {
  showError('');
}

async function fetchFilms() {
  const res = await fetch('/lab7/rest-api/films/');
  return await res.json();
}

function escapeHtml(text) {
  return String(text ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderFilms(films) {
  tbody.innerHTML = '';

  films.forEach((film) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(film.id)}</td>
      <td>${escapeHtml(film.title_ru)}</td>
      <td>${escapeHtml(film.title)}</td>
      <td>${escapeHtml(film.year)}</td>
      <td>
        <button class="btn btn-edit" data-action="edit" data-id="${film.id}">Редактировать</button>
        <button class="btn btn-danger" data-action="delete" data-id="${film.id}">Удалить</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function refresh() {
  const films = await fetchFilms();
  renderFilms(films);
}

async function deleteFilm(id) {
  const res = await fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' });

  if (res.status === 204) {
    await refresh();
  } else if (res.status === 404) {
    showError('Фильм не найден (404)');
  } else {
    showError('Ошибка удаления: ' + res.status);
  }
}

async function fetchFilm(id) {
  const res = await fetch(`/lab7/rest-api/films/${id}`);
  if (!res.ok) return null;
  return await res.json();
}

function openModal(mode, film = null, id = null) {
  clearErrorOnShowModal();
  currentMode = mode;
  currentId = id;

  if (mode === 'add') {
    modalTitle.textContent = 'Добавить фильм';
    inputTitleRu.value = '';
    inputTitle.value = '';
    inputYear.value = '';
    inputDescription.value = '';
  } else {
    modalTitle.textContent = `Редактировать фильм #${id}`;
    inputTitleRu.value = film.title_ru ?? '';
    inputTitle.value = film.title ?? '';
    inputYear.value = film.year ?? '';
    inputDescription.value = film.description ?? '';
  }

  modal.showModal();
}

function closeModal() {
  modal.close();
}

function formatErrors(errors) {
  // errors — объект {field: message}
  const order = ['title_ru', 'title', 'year', 'description'];
  const labels = {
    title_ru: 'Русское название',
    title: 'Название (оригинал)',
    year: 'Год',
    description: 'Описание'
  };

  let items = [];
  for (const key of order) {
    if (errors[key]) {
      items.push(`<li><b>${labels[key]}:</b> ${escapeHtml(errors[key])}</li>`);
    }
  }

  // если прилетели какие-то другие ошибки
  for (const key in errors) {
    if (!order.includes(key)) {
      items.push(`<li><b>${escapeHtml(key)}:</b> ${escapeHtml(errors[key])}</li>`);
    }
  }

  if (items.length === 0) return '';
  return `<ul style="margin:0; padding-left:18px;">${items.join('')}</ul>`;
}

async function sendFilm() {
  const payload = {
    title_ru: inputTitleRu.value,
    title: inputTitle.value,
    year: Number(inputYear.value),
    description: inputDescription.value
  };

  let url = '/lab7/rest-api/films/';
  let method = 'POST';

  if (currentMode === 'edit') {
    url = `/lab7/rest-api/films/${currentId}`;
    method = 'PUT';
  }

  return fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).then(async (response) => {
    if (response.ok) {
      return {}; // успех
    }
    return await response.json(); // ошибки с бэка
  }).then((errors) => {
    const html = formatErrors(errors);
    if (html) {
      showError(html);
      return;
    }
    closeModal();
    refresh();
  });
}


tbody.addEventListener('click', async (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;

  const action = btn.dataset.action;
  const id = Number(btn.dataset.id);

  if (action === 'delete') {
    if (confirm(`Удалить фильм #${id}?`)) {
      await deleteFilm(id);
    }
  }

  if (action === 'edit') {
    const film = await fetchFilm(id);
    if (!film) {
      showError('Фильм не найден');
      return;
    }
    openModal('edit', film, id);
  }
});

addBtn.addEventListener('click', () => openModal('add'));
cancelBtn.addEventListener('click', closeModal);
saveBtn.addEventListener('click', sendFilm);

refresh();

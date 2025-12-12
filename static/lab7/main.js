async function fetchFilms() {
  const res = await fetch('/lab7/rest-api/films/');
  if (!res.ok) {
    alert('Ошибка загрузки фильмов: ' + res.status);
    return [];
  }
  return await res.json();
}

function renderFilms(films) {
  const tbody = document.getElementById('films-tbody');
  tbody.innerHTML = '';

  films.forEach((film, index) => {
    const tr = document.createElement('tr');

    tr.innerHTML = `
      <td>${index}</td>
      <td>${escapeHtml(film.title_ru ?? '')}</td>
      <td>${escapeHtml(film.title ?? '')}</td>
      <td>${escapeHtml(String(film.year ?? ''))}</td>
      <td>
        <button class="btn btn-edit" data-action="edit" data-id="${index}">Редактировать</button>
        <button class="btn btn-danger" data-action="delete" data-id="${index}">Удалить</button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

function escapeHtml(text) {
  return text
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

async function deleteFilm(id) {
  const res = await fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' });
  if (res.status === 204) {
    await refresh();
    return;
  }
  if (res.status === 404) {
    alert('Фильм не найден (404)');
    return;
  }
  alert('Ошибка удаления: ' + res.status);
}

async function addFilm() {
  const title_ru = prompt('Название (RU):', '');
  if (title_ru === null) return;

  const title = prompt('Название (EN):', '');
  if (title === null) return;

  const year = prompt('Год:', '2000');
  if (year === null) return;

  const description = prompt('Описание:', '');
  if (description === null) return;

  const payload = { title, title_ru, year: Number(year), description };

  const res = await fetch('/lab7/rest-api/films/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    await refresh();
  } else {
    alert('Ошибка добавления: ' + res.status);
  }
}

async function editFilm(id, currentFilm) {
  const title_ru = prompt('Название (RU):', currentFilm.title_ru ?? '');
  if (title_ru === null) return;

  const title = prompt('Название (EN):', currentFilm.title ?? '');
  if (title === null) return;

  const year = prompt('Год:', String(currentFilm.year ?? '0'));
  if (year === null) return;

  const description = prompt('Описание:', currentFilm.description ?? '');
  if (description === null) return;

  const payload = { title, title_ru, year: Number(year), description };

  const res = await fetch(`/lab7/rest-api/films/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    await refresh();
  } else if (res.status === 404) {
    alert('Фильм не найден (404)');
  } else {
    alert('Ошибка редактирования: ' + res.status);
  }
}

async function refresh() {
  const films = await fetchFilms();
  renderFilms(films);
}

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;

  const action = btn.dataset.action;
  const id = btn.dataset.id;

  if (!action || id === undefined) return;

  if (action === 'delete') {
    if (confirm(`Удалить фильм #${id}?`)) {
      await deleteFilm(id);
    }
  }

  if (action === 'edit') {
    const films = await fetchFilms();
    const film = films[Number(id)];
    if (!film) {
      alert('Фильм не найден');
      return;
    }
    await editFilm(id, film);
  }
});

document.getElementById('add-film-btn').addEventListener('click', addFilm);

refresh();

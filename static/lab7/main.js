function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;

            if (films[i].title && films[i].title !== films[i].title_ru) {
                let originalSpan = document.createElement('span');
                originalSpan.className = 'original-title';
                originalSpan.innerText = films[i].title;
                tdTitle.appendChild(originalSpan);
            } else {
                tdTitle.innerText = ''; 
            }

            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.className = 'edit-btn';
            editButton.onclick = function() {
                editFilm(films[i].id);
            }

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.className = 'delete-btn';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.appendChild(editButton);
            tdActions.appendChild(delButton);

            tr.appendChild(tdTitleRus);
            tr.appendChild(tdTitle);
            tr.appendChild(tdYear);
            tr.appendChild(tdActions);

            tbody.appendChild(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title_ru) {
    if(! confirm(`Вы точно хотите удалить фильм "${title_ru}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function (response) {
            if (response.ok) {
                fillFilmList();
            } else {
                console.error('Ошибка при удалении фильма');
            }
        })
        .catch(function(error) {
            console.error('Ошибка при удалении фильма:', error);
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    clearErrors();
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    clearErrors();
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    }

    // Проверка обязательных полей
    if (!film.title_ru) {
        document.getElementById('title-ru-error').innerText = 'Русское название обязательно';
        return;
    }
    
    if (!film.year) {
        document.getElementById('year-error').innerText = 'Год обязателен';
        return;
    }
    
    if (!film.description) {
        document.getElementById('description-error').innerText = 'Описание обязательно';
        return;
    }

    const url = id === '' ? `/lab7/rest-api/films` : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : "PUT";

    fetch(url, {
        method: method, 
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function (resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        clearErrors();

        if(errors && typeof errors === 'object') {
            if(errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
            if(errors.title_ru) {
                document.getElementById('title-ru-error').innerText = errors.title_ru;
            }
            if(errors.title) {
                document.getElementById('title-error').innerText = errors.title;
            }
            if(errors.year) {
                document.getElementById('year-error').innerText = errors.year;
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при сохранении фильма:', error);
    });
}

function clearErrors() {
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = film.id;
        document.getElementById('title').value = film.title || '';
        document.getElementById('title-ru').value = film.title_ru || '';
        document.getElementById('year').value = film.year || '';
        document.getElementById('description').value = film.description || '';
        clearErrors();
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильма для редактирования:', error);
    });
}
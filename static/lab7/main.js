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

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';

            tdActions.appendChild(editButton);
            tdActions.appendChild(delButton);

            tr.appendChild(tdTitle);
            tr.appendChild(tdTitleRus);
            tr.appendChild(tdYear);
            tr.appendChild(tdActions);

            tbody.appendChild(tr);
        }
    });
}
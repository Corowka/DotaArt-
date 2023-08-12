
function isBestVisible() {
    return document.getElementById('best').display === 'none';
}

function createImagesAndFill(num, images) {
    const more = document.querySelector('#more .container');
    const container = document.createElement("div");
    container.setAttribute('id', `image-page-${num}`);
    container.classList.add("content");
    imagesArray = images.map(item => item[0]);
    imagesArray.forEach((num) => {
        const imgWrap = document.createElement("div");
        imgWrap.classList.add("img-wrap");
        const img = document.createElement("img");
        img.src = `../dotart server/data/pics/${num}.jpg`;
        img.alt = "";
        imgWrap.appendChild(img);
        container.appendChild(imgWrap);
    });
    more.appendChild(container);
}

function createNamesAndFill(num, names) {
    const more = document.querySelector('#more .container');
    const name = document.createElement("div");
    name.setAttribute('id', `name-page-${num}`);
    name.classList.add("name");
    wrap = document.createElement("div");
    wrap.classList.add("name-wrap");
    container = document.createElement("div");
    container.classList.add("name-container");
    namesArray = names.map(item => item[0]);
    namesArray.forEach((name) => {
        const nameItem = document.createElement("div");
        nameItem.classList.add("name-item");
        nameItem.textContent = name;
        container.appendChild(nameItem);
    });
    wrap.appendChild(container);
    name.appendChild(wrap);
    more.appendChild(name);
}

async function pagination(imagePage, imageOffset, imageSkip, namePage, nameOffset, nameSkip) {
    [imageSkip, nameSkip] = (isBestVisible()) ? [imageSkip, imageSkip] : [0, 0];
    url = `http://127.0.0.1:8000/pagination/?image_page=${imagePage}&image_offset=${imageOffset}&image_skip=${imageSkip}&name_page=${namePage}&name_offset=${nameOffset}&name_skip=${nameSkip}`;
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.image_part.length !== 0) {
                createImagesAndFill(imagePage, data.image_part);
            }
            if (data.name_part.length !== 0) {
                createNamesAndFill(namePage, data.name_part);
            }
        })
        .catch(error => console.error('Pagination error:', error));
}

var imagePage = 1;
var imageOffset = 24;
var imageSkip = 3;

var namePage = 1;
var nameOffset = 30;
var nameSkip = 15;

window.addEventListener('scroll', function () {
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight - 200) {
        pagination(imagePage, imageOffset, imageSkip, namePage, nameOffset, nameSkip);
        imagePage++;
        namePage++;
    }
});
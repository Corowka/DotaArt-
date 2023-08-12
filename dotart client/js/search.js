function setBestNames(namesArray) {
    const names = namesArray.map(item => item[0]);
    const scores = namesArray.map(item => item[1]);
    const nameContainer = document.querySelector('.best-names-container');
    names.forEach((name) => {
        const nameBlock = document.createElement('p');
        nameBlock.textContent = name;
        nameBlock.classList.add('best-name-item');
        nameContainer.appendChild(nameBlock);
    });
}

function setBestImages(bestImages) {
    const setBestImage = (num, img) => {
        const bestImage = document.querySelector(`#best-img-${num} img`);
        const imageElement = new Image();
        imageElement.onload = () => {
            bestImage.src = imageElement.src;
        };
        imageElement.src = `../dotart server/data/pics/${img[0]}.jpg`;
        const bestImageScore = document.querySelector(`#best-img-${num} .best-score`);
        bestImageScore.textContent = Math.round(img[1] * 10000) / 100 + '%';
    };
    setBestImage(1, bestImages[0]);
    setBestImage(2, bestImages[1]);
    setBestImage(3, bestImages[2]);
}

function deleteAllBestNames() {
    const nameContainer = document.querySelector('.best-names-container');
    while (nameContainer.firstChild)
        nameContainer.removeChild(nameContainer.firstChild);
}

function deleteAllPaginationImages() {
    const container = document.querySelector('#more .container');
    while (container.firstChild)
        container.removeChild(container.firstChild);
}

function displayBest() {
    const best = document.getElementById('best');
    best.style.display = 'block';
}

function displayBestNavLink() {
    const bestLink = document.getElementById('best-nav-link');
    bestLink.style.display = 'block';
}

function scrollToBest() {
    const bestBlock = document.getElementById('best');
    if (bestBlock) {
        window.scroll({
            top: bestBlock.offsetTop + 30,
            behavior: 'smooth'
        });
    }
}

async function getSearshResponse(imageUrl, name) {
    const url = `http://127.0.0.1:8000/search/?url=${imageUrl}&name=${name}`;
    const response = await fetch(url, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            setBestImages(data.best_images);
            deleteAllBestNames();
            setBestNames(data.best_names);
            displayBest();
            displayBestNavLink();
            deleteAllPaginationImages();
            scrollToBest();
        })
        .catch(error => console.error('Search error:', error));
}

function pushSearch() {
    const imageUrlInput = document.querySelector('.image-url');
    const imageUrl = imageUrlInput.value;
    const nameInput = document.querySelector('.name');
    const name = nameInput.value;
    if (imageUrl !== '' || name !== '') {
        const response = getSearshResponse(imageUrl, name)
    }
}

const searchBtn = document.querySelector('.search-btn');
searchBtn.addEventListener('click', pushSearch);
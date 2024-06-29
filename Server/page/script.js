const casesContainer = document.getElementById('casesContainer');
const prevPageBtn = document.getElementById('prevPageBtn');
const nextPageBtn = document.getElementById('nextPageBtn');

const casesPerPage = 50;
let currentPage = 1;

function displayCases(data) {
    casesContainer.innerHTML = '';
    const startIndex = (currentPage - 1) * casesPerPage;
    const endIndex = startIndex + casesPerPage;
    const casesToShow = data.slice(startIndex, endIndex);

    casesToShow.forEach(caseData => {
        const caseElement = document.createElement('div');
        caseElement.classList.add('case');
        caseElement.innerHTML = `
            <h3>Case ID: ${caseData.caseid}</h3>
            <p>Depth: ${caseData.depth}</p>
            <p>Location: ${caseData.location}</p>
            <p>Date: ${caseData.date}</p>
            <img src="${caseData.files.split(';')[0]}" alt="Image 1">
            <img src="${caseData.files.split(';')[1]}" alt="Image 2">
        `;
        casesContainer.appendChild(caseElement);
    });

    updatePagination(data.length);
}

function updatePagination(totalCases) {
    if (currentPage === 1) {
        prevPageBtn.disabled = true;
    } else {
        prevPageBtn.disabled = false;
    }

    const totalPages = Math.ceil(totalCases / casesPerPage);
    if (currentPage === totalPages) {
        nextPageBtn.disabled = true;
    } else {
        nextPageBtn.disabled = false;
    }
}

function nextPage() {
    currentPage++;
    fetchCases();
}

function prevPage() {
    currentPage--;
    fetchCases();
}

function fetchCases() {
    fetch('server.php')
        .then(response => response.json())
        .then(data => {
            displayCases(data);
            console.log(data);
        })
        .catch(error => {
            console.error('Error fetching cases:', error);
        });
}

// Initial fetch
fetchCases();

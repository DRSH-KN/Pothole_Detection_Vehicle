document.addEventListener('DOMContentLoaded', function () {
    // Fetch data from the server
    fetch('get_data.php')
        .then(response => response.json())
        .then(data => {
            // Process the retrieved data
            renderPotholeData(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

    // Function to render pothole data on the webpage
    // Function to render pothole data on the webpage
function renderPotholeData(data) {
    const potholeDataContainer = document.getElementById('potholeData');

    data.forEach(entry => {
        const entryDiv = document.createElement('div');
        entryDiv.classList.add('potholeEntry');

        const imageContainer = document.createElement('div');
        imageContainer.classList.add('potholeImage');
        imageContainer.style.display = 'flex'; // Set display to flex
        imageContainer.style.flexDirection = 'row'; // Set flex direction to row

        // Splitting image file paths
        const imagePaths = entry.files.split(';');
        imagePaths.forEach(path => {
            const image = document.createElement('img');
            image.src = path;
            image.alt = 'Pothole Image';
            image.width = 250; // Set the width of the image (adjust as needed)
            image.height = 250; // Set the height of the image (adjust as needed)
            image.style.marginRight = '10px'; // Add margin between images (adjust as needed)
            imageContainer.appendChild(image);
        });

        const detailContainer = document.createElement('div');
        detailContainer.classList.add('potholeDetail');

        // Extracting latitude and longitude
        const [lat, long] = entry.location.split(',');
        
        // Adding other details
        const locationLink = `<a href="https://www.google.com/maps?q=${lat},${long}" target="_blank">View on Google Maps</a>`;
        detailContainer.innerHTML = `
            <p><strong>Case ID:</strong> ${entry.caseid}</p>
            <p><strong>Depth:</strong> ${entry.depth} cm</p>
            <p><strong>Location:</strong> (${lat}, ${long}) (${locationLink})</p>
            <p><strong>Date:</strong> ${entry.date}</p>
        `;

        entryDiv.appendChild(imageContainer);
        entryDiv.appendChild(detailContainer);
        potholeDataContainer.appendChild(entryDiv);
    });
}

});

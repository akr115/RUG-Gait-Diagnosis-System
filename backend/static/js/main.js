document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('data-container').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('data-container').innerHTML = `<p>${data.message}</p><ul>${data.items.map(item => `<li>${item}</li>`).join('')}</ul>`;
            }
        })
        .catch(error => console.error('Error fetching data:', error));
});


document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([28.5, 77.1], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let bounds;
    map.on('draw:created', function (e) {
        const layer = e.layer;
        bounds = layer.getBounds();
    });

    const segmentBtn = document.getElementById('segment-btn');
    segmentBtn.addEventListener('click', () => {
        if (bounds) {
            const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
            fetch('/segment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ bbox })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('original-img').src = data.original_image;
                document.getElementById('segmented-img').src = data.segmented_image;
            });
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const map = L.map('map').setView([28.5, 77.1], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems
        },
        draw: {
            polygon: true,
            polyline: false,
            rectangle: true,
            circle: false,
            marker: false
        }
    });
    map.addControl(drawControl);

    let bounds;
    map.on('draw:created', function (e) {
        const layer = e.layer;
        drawnItems.addLayer(layer);
        bounds = layer.getBounds();
    });

    const segmentBtn = document.getElementById('segment-btn');
    segmentBtn.addEventListener('click', () => {
        if (bounds) {
            document.getElementById('loader').style.display = 'block';
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
                document.getElementById('loader').style.display = 'none';
                document.getElementById('original-img').src = data.original_image;
                document.getElementById('segmented-img').src = data.segmented_image;
            });
        }
    });
});

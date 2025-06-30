
from flask import Flask, render_template, request, jsonify
import requests
import os
from model_handler import ModelHandler

app = Flask(__name__)

# Initialize the model handler
model = ModelHandler('1.tflite')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/segment', methods=['POST'])
def segment_image():
    data = request.json
    bbox = data.get('bbox')

    # Fetch the WMS image
    wms_url = f"https://ows.terrestris.de/osm/service?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&LAYERS=OSM-WMS&SRS=EPSG:4326&BBOX={bbox}&WIDTH=512&HEIGHT=512&STYLES=default&FORMAT=image/png&TRANSPARENT=TRUE"
    response = requests.get(wms_url)

    # Save the original image
    original_image_path = os.path.join('static', 'output', 'original.png')
    with open(original_image_path, 'wb') as f:
        f.write(response.content)

    # Preprocess the image
    input_data = model.preprocess(original_image_path)

    # Run inference
    inference_output = model.run_inference(input_data)

    # Postprocess the output
    segmented_image = model.postprocess(inference_output)

    # Save the segmented image
    segmented_image_path = os.path.join('static', 'output', 'segmented.png')
    segmented_image.save(segmented_image_path)

    return jsonify({
        'original_image': original_image_path,
        'segmented_image': segmented_image_path
    })

if __name__ == '__main__':
    app.run(debug=True)

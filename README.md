# EDGE-BASED SEMANTIC SEGMENTATION OF GEOSPATIAL WMS DATA
 
 This project implements a web-based application for fetching geospatial data from a Web Map Service (WMS) and performing image processing using a TensorFlow Lite model. The goal is to demonstrate a pipeline for semantic segmentation of geospatial imagery, although with a current limitation in the provided model.
 
 ## Features
 
 *   **Interactive Map:** Utilizes Leaflet.js to display an OpenStreetMap base layer, allowing users to select a specific geographic area of interest.
 *   **WMS Integration:** Fetches high-resolution map images for the selected bounding box from a public WMS server (`https://ows.terrestris.de/osm/service` ).
 *   **TensorFlow Lite Model Integration:** Processes the fetched geospatial images using a pre-trained TensorFlow Lite (`.tflite`) model.
 *   **Image Preprocessing:** Handles image resizing, color channel conversion (RGBA to RGB), and normalization to prepare images for model inference.
 *   **Result Visualization:** Displays both the original WMS image and the processed (segmented) image side-by-side in the web interface.
 *   **Loading Indicator:** Provides visual feedback during the segmentation process.
 
 ## Current Limitation
 
 The `1.tflite` model currently included in this repository appears to be an **image classification model** rather than a true pixel-wise semantic segmentation model. This means it predicts a single class for the entire input image, rather than assigning a class to each individual pixel. As a result, the "segmented" output will be a solid color corresponding to the predicted class (currently, it consistently predicts class 0, which is mapped to black).
 
 To achieve actual edge-based semantic segmentation, you would need to replace `1.tflite` with a TensorFlow Lite model specifically trained for pixel-wise semantic segmentation.
 
 ## Setup
 
 Follow these steps to set up and run the project locally:
 
 1.  **Clone the repository:**

      git clone https://github.com/your-username/EDGE-BASED-SEMANTIC-SEGMENTATION-OF-GEOSPATIAL-WMS-DATA.git
      cd EDGE-BASED-SEMANTIC-SEGMENTATION-OF-GEOSPATIAL-WMS-DATA


      *(Note: Replace `https://github.com/your-username/EDGE-BASED-SEMANTIC-SEGMENTATION-OF-GEOSPATIAL-WMS-DATA.git` with the actual URL of your repository 
  once it's on GitHub.)*
  
  2.  **Create and activate a Python Virtual Environment:**
      It's highly recommended to use a virtual environment to manage project dependencies 
   python3 -m venv venv_segmentation
   source venv_segmentation/bin/activat 
  
  3.  **Install Dependencies:**
      Install all required Python packages using pip 
   pip install -r requirements.tx 
  
  ## Usage
  
  1.  **Run the Flask Application:**
      Ensure your virtual environment is activated, then run the `app.py` file 
   python app.p 
      The application will start a local development server, typically accessible at `http://127.0.0.1:5000/`.
  
  2.  **Access the Web Interface:**
      Open your web browser and navigate to the address provided in the terminal (e.g., `http://127.0.0.1:5000/`).
  
  3.  **Select an Area and Run Segmentation:**
      *   On the map, use the drawing tools (rectangle icon) to draw a bounding box around the area you want to segment.
   *   Click the "Run Segmentation" button.
   *   A loading spinner will appear, indicating that the process is underway.
   *   Once complete, the original WMS image and the segmented image will be displayed.
 ## Project Structure

  .
  ├── app.py                  # Main Flask application
  ├── model_handler.py        # Handles model loading, preprocessing, inference, and post-processing
  ├── requirements.txt        # Python dependencies
  ├── 1.tflite                # TensorFlow Lite model (image classification)
  ├── static/
  │   ├── css/
  │   │   └── style.css       # CSS for styling the web interface
  │   ├── js/
  │   │   └── script.js       # JavaScript for map interaction and API calls
  │   └── output/             # Directory to save original and segmented images
  └── templates/
      └── index.html          # HTML template for the web interface


 
 ## Future Improvements
 
 *   **Model Training:** Provide instructions or scripts for training a custom semantic segmentation model.
 *   **User Interface Enhancements:** Add more drawing tools, clear map functionality, and better error reporting to the UI.
 *   **Multiple WMS Layers:** Allow users to select different WMS layers or services.
 *   **Performance Optimization:** Optimize image processing and model inference for larger areas or faster results.


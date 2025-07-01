
import tflite_runtime.interpreter as tflite_interpreter
import numpy as np
from PIL import Image

class ModelHandler:
    def __init__(self, model_path):
        self.interpreter = tflite_interpreter.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def preprocess(self, image_path):
        img = Image.open(image_path).convert('RGB').resize((257, 257))
        img_array = np.array(img) / 255.0
        if img_array.shape[-1] == 4: # If it's still RGBA, take only RGB
            img_array = img_array[:, :, :3]
        return np.expand_dims(img_array, axis=0).astype(self.input_details[0]['dtype'])

    def run_inference(self, input_data):
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output_data

    def postprocess(self, inference_output):
        # Assuming inference_output is (batch_size, height, width, num_classes)
        # or (batch_size, num_classes) if it's a single prediction for the whole image
        segmentation_map = inference_output[0]

        # If the output is logits/probabilities, take argmax to get class IDs
        if segmentation_map.ndim == 3 and segmentation_map.shape[-1] > 1:
            segmentation_map = np.argmax(segmentation_map, axis=-1)
        elif segmentation_map.ndim == 1 and segmentation_map.shape[0] > 1: # Case for (num_classes,)
            # This might be a single prediction for the whole image
            # Take the argmax to get the predicted class ID
            predicted_class_id = np.argmax(segmentation_map)
            # Create a 2D array of the predicted class ID, sized to 257x257
            segmentation_map = np.full((257, 257), predicted_class_id, dtype=np.uint8)
        elif segmentation_map.ndim == 2 and segmentation_map.shape == (1, 21): # Case for (1, num_classes)
            predicted_class_id = np.argmax(segmentation_map[0])
            segmentation_map = np.full((257, 257), predicted_class_id, dtype=np.uint8)
        elif segmentation_map.ndim == 3 and segmentation_map.shape == (1, 1, 21): # Case for (1, 1, num_classes)
            predicted_class_id = np.argmax(segmentation_map[0, 0])
            segmentation_map = np.full((257, 257), predicted_class_id, dtype=np.uint8)


        # Ensure the segmentation_map is 2D (height, width)
        if segmentation_map.ndim != 2:
            raise ValueError(f"Unexpected segmentation map shape after argmax: {segmentation_map.shape}. Expected 2D (height, width).")

        # Resize the segmentation map to 257x257 if it's not already
        if segmentation_map.shape != (257, 257):
            # This should ideally not be needed if the above logic correctly creates 257x257
            # But as a fallback, if it's a small map, resize it.
            segmentation_map = Image.fromarray(segmentation_map.astype(np.uint8)).resize((257, 257), Image.NEAREST)
            segmentation_map = np.array(segmentation_map)

        # Log unique values in the segmentation map
        # Create a simple color palette for up to 21 classes (or more if needed)
        num_classes = 21 # Based on the previous error message (1, 1, 21)
        colors = [
            (0, 0, 0),       # Class 0: Black
            (255, 0, 0),     # Class 1: Red
            (0, 255, 0),     # Class 2: Green
            (0, 0, 255),     # Class 3: Blue
            (255, 255, 0),   # Class 4: Yellow
            (255, 0, 255),   # Class 5: Magenta
            (0, 255, 255),   # Class 6: Cyan
            (128, 0, 0),     # Class 7: Dark Red
            (0, 128, 0),     # Class 8: Dark Green
            (0, 0, 128),     # Class 9: Dark Blue
            (128, 128, 0),   # Class 10: Olive
            (128, 0, 128),   # Class 11: Purple
            (0, 128, 128),   # Class 12: Teal
            (192, 192, 192), # Class 13: Silver
            (128, 128, 128), # Class 14: Gray
            (255, 165, 0),   # Class 15: Orange
            (255, 192, 203), # Class 16: Pink
            (165, 42, 42),   # Class 17: Brown
            (240, 230, 140), # Class 18: Khaki
            (230, 230, 250), # Class 19: Lavender
            (255, 228, 196)  # Class 20: Bisque
        ]

        # Create an empty RGB image array
        colored_segmentation = np.zeros((segmentation_map.shape[0], segmentation_map.shape[1], 3), dtype=np.uint8)

        # Apply colors based on class IDs
        for class_id in range(num_classes):
            if class_id < len(colors): # Ensure we don't go out of bounds for colors
                colored_segmentation[segmentation_map == class_id] = colors[class_id]

        output_image = Image.fromarray(colored_segmentation)
        return output_image

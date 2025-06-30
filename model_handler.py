
import tensorflow as tf
import numpy as np
from PIL import Image

class ModelHandler:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def preprocess(self, image_path):
        img = Image.open(image_path).resize((256, 256))
        img_array = np.array(img) / 255.0
        return np.expand_dims(img_array, axis=0).astype(self.input_details[0]['dtype'])

    def run_inference(self, input_data):
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output_data

    def postprocess(self, inference_output):
        # This is a placeholder. The actual post-processing will depend on the model's output format.
        # For now, we'll just convert the output to a color image.
        output_image = Image.fromarray((inference_output[0] * 255).astype(np.uint8))
        return output_image

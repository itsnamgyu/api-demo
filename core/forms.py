from django import forms

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dropout, Flatten, Dense

mobilenet = keras.applications.MobileNetV3Small(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

model = keras.models.Sequential()
model.add(mobilenet)
model.add(Flatten())
model.add(Dense(256, activation= 'relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation= 'sigmoid'))

model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

model.load_weights("weights.h5")

class BasicForm(forms.Form):
    student_number = forms.IntegerField()


class ClassificationForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data["image"]
        # save image to image.jpg
        with image.open(mode="rb") as f:
            data = f.read()
        with open("image.jpg", "wb") as f:
            f.write(data)

        img = keras.preprocessing.image.load_img(
            "image.jpg", target_size=(224, 224)
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        predictions = model.predict(img_array)
        score = predictions[0]
        print(
            "This image is %.2f percent cat and %.2f percent dog."
            % (100 * (1 - score), 100 * score)
        )
        self.p = 1 - float(score)

        return image
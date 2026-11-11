# Python script exported from Vandana_Handwritten_Digit_Recognition_ANN_CNN.ipynb

# # Handwritten Digit Recognition Using ANN and CNN
#
# **Beginner-level Machine Learning practice**
#
# In this notebook, I will build two simple models to recognize handwritten digits from **0 to 9**.
#
# - **ANN (Artificial Neural Network):** uses the image pixel values after flattening them.
# - **CNN (Convolutional Neural Network):** learns patterns such as edges and shapes from the image.
#
# I will use the MNIST dataset available in TensorFlow/Keras.
#
# **Before running:** Open this notebook in Google Colab and run the cells from top to bottom. The dataset downloads automatically the first time, so an internet connection is needed.

# ## 1. Import the libraries
# We use TensorFlow/Keras to build the models, NumPy to work with arrays, and Matplotlib to display images.

# %%
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras import layers, models

# Set random seeds to make results more repeatable
tf.keras.utils.set_random_seed(42)

print("TensorFlow version:", tf.__version__)

# ## 2. Load the MNIST dataset
# The dataset already contains training images and test images. Each image is a handwritten digit.

# %%
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

print("Training images:", x_train.shape)
print("Training labels:", y_train.shape)
print("Test images:", x_test.shape)
print("Test labels:", y_test.shape)

# ## 3. Look at some sample images
# The number shown below each image is the correct digit label.

# %%
plt.figure(figsize=(10, 4))

for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(x_train[i], cmap="gray")
    plt.title(f"Label: {y_train[i]}")
    plt.axis("off")

plt.tight_layout()
plt.show()

# ## 4. Prepare the images
# Pixel values range from 0 to 255. Dividing by 255 changes them to a range between 0 and 1, which helps the model learn more easily.

# %%
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

print("Minimum pixel value:", x_train.min())
print("Maximum pixel value:", x_train.max())

# ## 5. Build an ANN model
#
# An ANN needs a one-dimensional list of values, so `Flatten` converts each 28 × 28 image into 784 values. The final layer has 10 outputs because the possible digits are 0 to 9.

# %%
ann_model = models.Sequential([
    layers.Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(10, activation="softmax")
])

ann_model.summary()

# ## 6. Compile and train the ANN
# The model adjusts its weights during training. We use a small number of epochs to keep this beginner exercise manageable.

# %%
ann_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

ann_history = ann_model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1
)

# ## 7. Test the ANN
# Test data is kept separate from training so we can check how the model performs on images it did not train on.

# %%
ann_loss, ann_accuracy = ann_model.evaluate(x_test, y_test, verbose=0)

print(f"ANN test loss: {ann_loss:.4f}")
print(f"ANN test accuracy: {ann_accuracy * 100:.2f}%")

# ## 8. Build a CNN model
#
# A CNN works directly with the image shape. `Conv2D` learns image patterns, `MaxPooling2D` reduces the feature-map size, and `Flatten` prepares the learned features for the final classification layers.

# %%
cnn_model = models.Sequential([
    layers.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(10, activation="softmax")
])

cnn_model.summary()

# ## 9. Add the channel dimension and train the CNN
# CNN layers expect grayscale images to include a channel dimension. We add it here, changing each image from 28 × 28 to 28 × 28 × 1.

# %%
x_train_cnn = np.expand_dims(x_train, axis=-1)
x_test_cnn = np.expand_dims(x_test, axis=-1)

cnn_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

cnn_history = cnn_model.fit(
    x_train_cnn,
    y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1
)

# ## 10. Test the CNN

# %%
cnn_loss, cnn_accuracy = cnn_model.evaluate(x_test_cnn, y_test, verbose=0)

print(f"CNN test loss: {cnn_loss:.4f}")
print(f"CNN test accuracy: {cnn_accuracy * 100:.2f}%")

# ## 11. Compare ANN and CNN
# The values below come from your own run. Results may vary slightly depending on the environment and training.

# %%
model_names = ["ANN", "CNN"]
accuracies = [ann_accuracy * 100, cnn_accuracy * 100]

plt.figure(figsize=(6, 4))
plt.bar(model_names, accuracies)
plt.ylabel("Test accuracy (%)")
plt.title("ANN vs CNN on MNIST")
plt.ylim(0, 100)
plt.show()

for name, score in zip(model_names, accuracies):
    print(f"{name}: {score:.2f}%")

# ## 12. Try a prediction
# Change `image_index` to view another test image. The model will predict which digit it sees.

# %%
image_index = 12  # Change this number to try another test image

image_to_predict = x_test_cnn[image_index:image_index + 1]
probabilities = cnn_model.predict(image_to_predict, verbose=0)
predicted_digit = int(np.argmax(probabilities[0]))

plt.imshow(x_test[image_index], cmap="gray")
plt.title(f"Actual: {y_test[image_index]} | Predicted: {predicted_digit}")
plt.axis("off")
plt.show()

print("Actual digit:", int(y_test[image_index]))
print("Predicted digit:", predicted_digit)

# ## Conclusion
#
# - ANN uses flattened pixel values to classify each digit.
# - CNN uses convolution and pooling layers to learn image patterns.
# - I checked both models using test accuracy.
# - The CNN prediction cell lets me compare a predicted digit with the actual digit.
#
# The accuracy values can change slightly between runs. This notebook is a basic practice example for handwritten digit classification.

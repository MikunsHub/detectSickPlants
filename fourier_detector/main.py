import os
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt

file_path = "/Users/mac/Documents/detectSickPlants/fourier_detector/temp/"

# Get the list of images in the directory.
image_files = os.listdir(file_path)

image_list = os.listdir(file_path)
healthy_cocoa = []
sick_cocoa = []
test_image = None

# separate images based on the anotation on the
# filenames
for filename in image_list:
    if filename.startswith("healthy"):
        healthy_cocoa.append(filename)
    elif filename.startswith("test_healthy2"):
        test_image = filename
    elif filename.startswith("sick"):
        sick_cocoa.append(filename)

healthy_resized = []
sick_resized = []

for image in healthy_cocoa:
    loaded_image = cv2.imread(os.path.join(file_path, image))
    resized_image = cv2.resize(loaded_image, (400, 400))
    healthy_resized.append(resized_image)

for image in sick_cocoa:
    loaded_image = cv2.imread(os.path.join(file_path, image))
    resized_image = cv2.resize(loaded_image, (400, 400))
    sick_resized.append(resized_image)


# convert healthy cocoa to grayscale
healthy_gray = []
sick_gray = []

for image in healthy_resized:
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    healthy_gray.append(grayscale_image)

for image in sick_resized:
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sick_gray.append(grayscale_image)

# # convert images to frequency domain
healthy_freq = []
sick_freq = []

for image in healthy_gray:
    # perform 2D Fourier Transform
    freq = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    # shift zero frequency component to center of spectrum
    freq_shifted = np.fft.fftshift(freq)
    healthy_freq.append(freq_shifted)

for image in sick_gray:
    # perform 2D Fourier Transform
    freq = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    # shift zero frequency component to center of spectrum
    freq_shifted = np.fft.fftshift(freq)
    sick_freq.append(freq_shifted)

# compute the average frequency of healthy cocoa images
avg_healthy_freq = np.mean(healthy_freq, axis=0)

# compute the average frequency of sick cocoa images
avg_sick_freq = np.mean(sick_freq, axis=0)

# preprocessing test image
test_image = cv2.imread(os.path.join(file_path, test_image))
resized_test_image = cv2.resize(test_image, (400, 400))
gray_test = cv2.cvtColor(resized_test_image, cv2.COLOR_BGR2GRAY)
freq_test = cv2.dft(np.float32(gray_test), flags=cv2.DFT_COMPLEX_OUTPUT)

freq_shifted_test = np.fft.fftshift(freq_test)

# Calculate the SSIM between healthy reference spectral and test image
ssim_score_healthy = ssim(
    avg_healthy_freq,
    freq_shifted_test,
    win_size=3,
    channel_axis=2,
    data_range=np.max(avg_healthy_freq) - np.min(avg_healthy_freq),
)

# Calculate the SSIM between sick reference spectral and test image
ssim_score_sick = ssim(
    avg_sick_freq,
    freq_shifted_test,
    win_size=3,
    channel_axis=2,
    data_range=np.max(avg_sick_freq) - np.min(avg_sick_freq),
)

# Calculate the mean squared error (MSE) between the average frequency of healthy cocoa images and the test image frequency.
mse_healthy = np.mean(np.square(np.abs(avg_healthy_freq) - np.abs(freq_shifted_test)))

# Calculate the mean squared error (MSE) between the average frequency of sick cocoa images and the test image frequency.
mse_sick = np.mean(np.square(np.abs(avg_sick_freq) - np.abs(freq_shifted_test)))

# Print the SSIM score.
print("The SSIM score between healthy and test", ssim_score_healthy)

# Print the SSIM score.
print("The SSIM score between sick and test", ssim_score_sick)

print("MSE_healthy: ", mse_healthy)

print("MSE_sick: ", mse_sick)


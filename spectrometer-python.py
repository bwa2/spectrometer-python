import cv2
import numpy as np
import matplotlib.pyplot as plt

# === CONFIGURATION ===
roi_coords = (140, 100, 200, 100)  # Fixed ROI (x, y, width, height)             MUST BE ADJUSTABLE!!
OUTPUT_IMAGE = "captured_image.png"
OUTPUT_TEXT = "spectrum_distribution.txt"
OUTPUT_GRAPH = "spectrum_plot.png"

# === CALIBRATION FORMULA: Convert Pixels to Wavelength ===
def pixel_to_wavelength(x_pixel):
    return 1.4671 * x_pixel + 394.7305 # Formula from calibration                 MUST BE ADJUSTABLE!!

# === FUNCTION: Compute Spectrum from ROI ===
def compute_spectrum(frame):
    """ Extract spectrum intensity from a fixed ROI. """
    x, y, w, h = roi_coords
    cropped = frame[y:y+h, x:x+w]
    cropped_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Grayscale ROI", cropped_gray)

    # Sum intensity along Y-axis to get 1D profile
    intensity_profile = np.sum(cropped_gray, axis=0)

    # Cleaning Data
    lenght_profile = len(intensity_profile)
    intensity_profile[0] = intensity_profile[2]
    intensity_profile[1] = intensity_profile[2]
    intensity_profile[lenght_profile-1] = intensity_profile[lenght_profile-2]
    print("intensity before: ", intensity_profile)

    # Normalize intensity (0 to 1)
    intensity_profile = (intensity_profile - np.min(intensity_profile)) / (np.max(intensity_profile) - np.min(intensity_profile))
    print("intensity after: ", intensity_profile)

    # Convert pixels to wavelength
    pixel_positions = np.arange(lenght_profile)
    print(pixel_positions)
    wavelengths = pixel_to_wavelength(pixel_positions)

    return wavelengths, intensity_profile, cropped

# === FUNCTION: Display Live Spectrum ===
# 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
def show_spectrum(frame):
    """ Show the spectrum analyzer in real-time when 's' is pressed. """
    wavelengths, intensity, _ = compute_spectrum(frame)

    plt.figure(figsize=(8, 6))
    plt.plot(wavelengths, intensity, color="black", label="Normalized Spectrum")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity (0-1)")
    plt.title("Live Spectrum Analyzer")
    plt.legend()
    plt.grid(True)
    plt.show()

# === FUNCTION: Save Spectrum Data & Image ===
def save_spectrum_data(frame):
    """ Save spectral intensity data to a TXT file and save the spectrum graph. """
    wavelengths, intensity, cropped = compute_spectrum(frame)

    # Save to TXT file
    np.savetxt(OUTPUT_TEXT, np.column_stack((wavelengths, intensity)), fmt="%.2f\t%.6f",
               header="Wavelength (nm)\tNormalized Intensity", comments="")
    print(f"✅ Spectrum data saved to: {OUTPUT_TEXT}")

    # Save captured image
    cv2.imwrite(OUTPUT_IMAGE, frame)
    print(f"✅ Image saved as: {OUTPUT_IMAGE}")

    # Save spectrum graph
    plt.figure(figsize=(8, 6))
    plt.plot(wavelengths, intensity, color="black", label="Normalized Spectrum")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity (0-1)")
    plt.title("Estimated Spectrum Distribution")
    plt.legend()
    plt.grid(True)
    plt.savefig(OUTPUT_GRAPH, dpi=300)
    plt.close()
    print(f"✅ Spectrum graph saved as: {OUTPUT_GRAPH}")

# === MAIN FUNCTION: Capture Webcam & Process Spectrum ===
def main():
    cap = cv2.VideoCapture(0)
    last_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Failed to capture frame.")
            break

        # Draw a rectangle to show ROI
        x, y, w, h = roi_coords
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Live Camera", frame)
        last_frame = frame  # Store the latest frame

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and last_frame is not None:  # Press 's' to show the spectrum
            show_spectrum(last_frame)
        elif key == ord('q') and last_frame is not None:  # Press 'q' to save & exit
            save_spectrum_data(last_frame)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

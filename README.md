# 🎯 Rifle Shot Grouping Analysis using Computer Vision

Proof-of-Concept (PoC) system that automatically analyzes rifle shot grouping accuracy from target images using computer vision techniques.

The system detects shot impact points, clusters them spatially, and quantifies grouping precision through geometric measurements.

Developed as an industry assignment for **Bangladesh Army** through a private software company, with focus on objective precision evaluation and visual measurement.

## Problem Statement

Manual evaluation of rifle shot grouping during shooting practice is:

- Time-consuming  
- Subjective  
- Prone to human error and inconsistency

**Goal**: Build an automated, image-based solution to objectively evaluate shot grouping accuracy and spatial dispersion.

## Features

- Automatic detection of bullet impact points  
- Centroid extraction of each shot hole  
- Spatial clustering of shot groups  
- Calculation of grouping precision metrics  
- Visual overlays showing detected points and analysis  
- Objective, repeatable measurement results

## Methodology

1. **Image Preprocessing**  
   - Grayscale conversion  
   - Noise reduction (Gaussian blur / median filter)  
   - Contrast enhancement if needed  

2. **Shot Detection**  
   - Adaptive thresholding / binary segmentation  
   - Contour detection  
   - Shape & size filtering to isolate bullet holes  

3. **Feature Extraction**  
   - Compute centroid (x,y) of each valid contour  
   - Optional: diameter / area validation  

4. **Grouping & Spatial Analysis**  
   - Spatial clustering (DBSCAN / hierarchical / k-means with silhouette)  
   - Calculate group center, radius, extreme spread, mean radial deviation  
   - Compute standard metrics (group size in MOA, inches, cm, etc.)

5. **Visualization & Reporting**  
   - Overlay detected points and clusters on original image  
   - Display key statistics (group count, size, center, dispersion)  
   - Save annotated result images

## Technologies Used

- **Python**  
- **OpenCV** – core computer vision library  
- **NumPy** – numerical operations & array handling  
- **SciPy** – spatial algorithms & clustering  
- **Matplotlib** – visualization & result plotting

## Results

- Reliable detection of shot impact points across various lighting conditions and target types  
- Objective grouping precision scores  
- Clear visual feedback suitable for instructors and shooters  
- Significant time saving compared to manual measurement

## Applications

- Military & defense shooting practice analysis  
- Precision rifle training evaluation  
- Law enforcement firearms qualification scoring  
- Competitive shooting performance tracking  
- General image-based geometric measurement systems  
- Computer vision PoC / research projects

## Future Improvements

- Machine learning / deep learning based shot detection (more robust to lighting, dirt, torn paper)  
- Synthetic bullet hole data generation for training & evaluation  
- Real-time analysis from live camera feed  
- Multi-session statistical comparison & progress tracking  
- Mobile/web interface for field usage  
- Automatic target type recognition (bullseye, silhouette, etc.)

## Important Notes

- This project contains **no classified or sensitive information**

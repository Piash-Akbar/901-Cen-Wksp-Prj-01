🎯 Rifle Shot Grouping Analysis using Computer Vision
Overview

This project presents a computer vision–based Proof-of-Concept (PoC) system designed to automatically analyze rifle shot grouping accuracy from target images. The system detects shot impact points, clusters them spatially, and quantifies grouping precision using geometric analysis.

The project was developed as part of an industry assignment for Bangladesh Army through a private software company, focusing on precision evaluation and visual measurement.

Problem Statement

Manual evaluation of rifle shot grouping during shooting practice is time-consuming and subjective. The goal of this project was to build an automated, image-based solution to objectively evaluate grouping accuracy and spatial dispersion.

Methodology

Image preprocessing (grayscale conversion, noise reduction)

Thresholding and contour detection

Extraction of shot impact centroids

Spatial clustering and grouping analysis

Visualization of detected points and grouping metrics

Technologies Used

Python

OpenCV

NumPy

SciPy

Matplotlib

Results

Accurate detection of shot impact points from target images

Computation of grouping precision based on spatial distribution

Visual overlays for interpretation and reporting

Applications

Military and defense shooting practice analysis

Precision training evaluation

Image-based measurement systems

Computer vision research and PoC development

Future Improvements

ML-based clustering for improved robustness

Synthetic data generation for training and evaluation

Real-time camera integration

Statistical analysis across multiple sessions

Disclaimer

This project does not contain any classified or sensitive information. All data used are anonymized and intended solely for research and demonstration purposes.

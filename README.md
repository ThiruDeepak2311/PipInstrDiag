# P&ID Symbol Detection System

A computer vision-based system for detecting and extracting P&ID (Piping and Instrumentation Diagram) components from schematic diagrams. The system uses deep learning to identify components and generates a master list of detected elements.

## Overview

This project provides an automated solution for processing P&ID diagrams, leveraging computer vision and deep learning techniques to detect and classify various industrial components. The system supports multiple input formats (.pdf/.jpeg/.png) and generates both visual and data outputs.

## Features

- Automated P&ID component detection
- Support for multiple input formats (PDF, JPEG, PNG)
- Region of Interest (ROI) based component detection
- Annotated output images with component labels
- CSV export of detected components
- Standalone application deployment
- Deep learning-based symbol recognition

## Technical Architecture

### Input Processing
- Support for multiple file formats:
  - PDF documents
  - JPEG images
  - PNG images
- Automatic image preprocessing and enhancement
- ROI (Region of Interest) detection

### Deep Learning Model
- Based on YOLOv5/YOLOv8 architecture
- Pre-trained on P&ID symbol datasets
- Custom training support for specific symbol sets
- ISO Standard compliance

### Output Generation
1. Annotated Images:
   - Visual component identification
   - Component labeling
   - Bounding box visualization

2. Master Component List:
   - CSV format output
   - Component categorization
   - Location information
   - Reference identifiers


## Model Training

### Dataset Preparation
1. Collect P&ID diagrams from:
   - ISO standards
   - Open-source datasets
   - Industry standard diagrams

2. Data Preprocessing:
   - Image standardization
   - Annotation formatting
   - Augmentation pipeline
   - 

## Deployment

### Docker Container
```bash
docker build -t pid-detector .
docker run -p 8501:8501 pid-detector
```

### Cloud Deployment
- AWS/Azure/GCP compatible
- Containerized deployment support
- API endpoint configuration

## References

1. [Academic Paper on P&ID Recognition](https://academic.oup.com/jcde/article/9/4/1298/6611631)
2. [YOLOv5 for Symbol Extraction](https://www.researchgate.net/publication/366123842_YOLOv5_for_symbol_extraction_in_PID_diagrams)
3. [P&ID Standards Documentation](https://instrumentationandcontrol.net/pid-diagram-basics-part-2-standards.html)

## Dataset Sources

- [Roboflow P&ID Dataset](https://universe.roboflow.com/new-workspace-ojauf/pidnfu5r/)
- ISO Standard P&ID Symbols
- Custom annotated datasets

---

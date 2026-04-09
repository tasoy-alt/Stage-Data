# Master’s Year 1 Internship Project

## Project Overview
This project aims to automate and refine the annotation of medical prescriptions using **medkit**. The goal is to extract entities and identify relationships within clinical texts to create a high-quality dataset for healthcare data science.

## Methodology
To ensure the highest accuracy (**Gold Standard**), the workflow follows these steps:

1. **Automatic Annotation**: Using `medkit` to pre-annotate prescriptions.
2. **Manual Refinement**: If the automatic output is suboptimal, data is exported to `doccano`.
3. **Gold Standard Creation**: Manual correction of labels and relationships in doccano to generate a "perfect" CSV dataset.
4. **Model Optimization**: Using the Gold Standard to evaluate and fine-tune the annotation algorithms.

## Tech Stack
* **Language**: Python
* **Libraries**: medkit, pandas
* **Annotation Tool**: doccano
* **Format**: CSV / JSONL

## Data Structure
The final output is a structured CSV file containing:
* **Entities**: Medication names, dosage, duration, frequency.
* **Relations**: Linking dosages to their respective medications.

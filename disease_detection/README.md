# AgriAI Deep Learning: Plant Foliage Disease Detection Model Card

## 1. Model Overview & Scientific Literature Alignment
- **Model Names**: `MobileNetV2-AgriFoliage` and `EfficientNetB0-AgriFoliage`
- **Application**: Automated diagnosis of crop foliar pathologies from smartphone photographs with Grad-CAM visual attention overlays.
- **Scientific Literature Reference**:
  Guided by the comparative transfer learning evaluation in:
  > **Demilie, Wubetu Barud (2024)**. *Plant disease detection and classification techniques: a comparative study of the performances*. **Journal of Big Data (SpringerOpen)**, 11:71. [https://doi.org/10.1186/s40537-024-00927-1](https://doi.org/10.1186/s40537-024-00927-1)
  The paper evaluated CNN backbones across standardized plant disease benchmarks, highlighting that MobileNetV2 achieves optimal parameter efficiency for mobile devices, while EfficientNetB0 balances high accuracy with low compute overhead.

---

## 2. Supported Crops & Pathological Classes

| Crop | Class Name | Biological Pathogen / Condition |
| :--- | :--- | :--- |
| **Tomato** | `Tomato___Early_blight` | *Alternaria solani* (Fungal concentric ring lesions) |
| **Tomato** | `Tomato___Late_blight` | *Phytophthora infestans* (Water-soaked dark lesions) |
| **Tomato** | `Tomato___Bacterial_spot` | *Xanthomonas* spp. (Small dark angular spots) |
| **Tomato** | `Tomato___healthy` | Healthy vigorous foliage |
| **Potato** | `Potato___Early_blight` | *Alternaria solani* |
| **Potato** | `Potato___Late_blight` | *Phytophthora infestans* (Severe foliar blight) |
| **Potato** | `Potato___healthy` | Healthy foliage |
| **Pepper Bell** | `Pepper__bell___Bacterial_spot` | *Xanthomonas campestris* |
| **Pepper Bell** | `Pepper__bell___healthy` | Healthy foliage |
| **Corn (Maize)** | `Corn_(maize)___Common_rust_` | *Puccinia sorghi* (Golden-brown pustules) |
| **Corn (Maize)** | `Corn_(maize)___Northern_Leaf_Blight` | *Exserohilum turcicum* (Elongated grayish lesions) |
| **Corn (Maize)** | `Corn_(maize)___healthy` | Healthy foliage |

---

## 3. Preprocessing, Normalization & Data Augmentation
1. **Resolution**: All input images are standardized to $224 \times 224 \times 3$ via bilinear interpolation.
2. **Normalization**: Pixel values are scaled to $[0.0, 1.0]$ and z-score normalized using ImageNet parameters:
   $$\text{Mean} = [0.485, 0.456, 0.406], \quad \text{Std} = [0.229, 0.224, 0.225]$$
3. **Data Augmentation**: Applied **strictly to the training set** to prevent data leakage:
   - Random horizontal flip ($p = 0.5$)
   - Random vertical flip ($p = 0.3$)
   - Random rotation ($\pm 15^\circ$)
   - Color and contrast jitter ($\pm 10\%$)
   - Validation and test partitions undergo **zero augmentation** (resize and normalization only).

---

## 4. Architectural Comparison Benchmark

| Metric / Attribute | MobileNetV2 | EfficientNetB0 |
| :--- | :--- | :--- |
| **Core Convolution Type** | Inverted Residuals & Depthwise Separable | Compound Scaled MBConv Blocks |
| **Parameters** | 3.5 Million | 5.3 Million |
| **Input Shape** | $224 \times 224 \times 3$ | $224 \times 224 \times 3$ |
| **Macro Accuracy** | 96.8% | 97.4% |
| **Macro Precision** | 96.7% | 97.2% |
| **Macro Recall** | 96.8% | 97.4% |
| **Macro F1-Score** | 96.7% | 97.3% |
| **Inference Latency (CPU)** | 48 ms | 76 ms |
| **Model Checkpoint Size** | 14.2 MB | 21.5 MB |
| **Primary Deployment Target** | Smartphone App / Kiosk / Edge | Cloud API Server / Batch Screening |

---

## 5. Explainability: Grad-CAM Saliency Maps
Gradient-weighted Class Activation Mapping (Grad-CAM) computes gradients of the predicted class score with respect to feature activation maps of the final convolutional layer:
- **MobileNetV2**: Gradients hooked to `features.18` (final $1 \times 1$ expansion layer).
- **EfficientNetB0**: Gradients hooked to `conv_head`.
The resulting 2D activation matrix is passed through a ReLU nonlinearity, normalized to $[0, 1]$, color-mapped to Jet/Thermal spectrum, and blended as a semi-transparent overlay over the original leaf image. This allows farmers and extension officers to confirm whether the model attended to actual foliar lesions rather than background soil clutter.

---

## 6. Field Generalization & Critical Disclaimers
1. **Laboratory to Open-Field Gap**: The model is evaluated on benchmark foliage datasets. Real-world farm images in Andhra Pradesh with intense solar glare, dust accumulation, chemical residue stains, or complex weeds may exhibit reduced confidence.
2. **Out-of-Distribution (OOD) Protection**: Images yielding a top class probability below 60% are flagged as "Uncertain / Unsupported" to avoid forced false diagnoses.
3. **Safety & Regulatory Warning**:
   > **CRITICAL NOTICE**: This automated deep learning system is intended for educational screening and decision-support. Do **not** apply synthetic chemical fungicides or pesticides without confirmation from an ANGRAU / ICAR certified plant pathologist or your local Rythu Bharosa Kendra (RBK) agricultural officer.

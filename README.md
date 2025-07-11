# Visitor Detection Algorithm

## Objective

Identify unique visitors from entry/exit events using computer vision. The system analyzes colored rectangles in surveillance images to assign unique visitor IDs.

## Algorithm

Color-based appearance descriptor with incremental clustering:

1. **Extract Features**: HSV histogram (5×5×5 bins) + mean RGB values → 128-dimensional descriptor
2. **Incremental Clustering**: Compare each detection to existing visitor centroids
3. **Threshold Assignment**: Assign to existing visitor if distance < 0.25, otherwise create new visitor
4. **Centroid Update**: Moving average to update visitor representations

## Results

| Metric             | Value |
| ------------------ | ----- |
| Total Events       | 558   |
| Unique Visitors    | 92    |
| Events per Visitor | 6.07  |

## Usage

### Installation

```bash
pip install -r requirements.txt
```

### Run Detection

```bash
python visitor_detection.py
```

### Options

```bash
python visitor_detection.py --threshold 0.25 --output results.csv
```

- `--threshold`: Clustering threshold (0.20-0.30, default: 0.25)
- `--output`: Output CSV file name

## Dependencies

- `numpy>=1.21.0`
- `opencv-python>=4.5.0`
- `pandas>=1.3.0`

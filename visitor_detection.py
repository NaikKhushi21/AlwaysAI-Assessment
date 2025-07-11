"""
Visitor Detection Algorithm - Simple color-based approach
"""

import cv2
import numpy as np
import pandas as pd
import pathlib
import datetime as dt
import argparse

def ts_to_path(ts_str):
    """Convert timestamp to image path"""
    t = dt.datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
    return pathlib.Path(f'event_images/location1_{t:%Y-%m-%d_%H-%M-%S}.png')

def get_descriptor(img_path, bbox):
    """Extract color descriptor from image ROI"""
    img = cv2.imread(str(img_path))
    x, y, w, h = map(int, bbox.split(','))
    roi = img[y:y+h, x:x+w]
    
    # HSV histogram + mean RGB
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [5, 5, 5], [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    mean_rgb = roi.mean(axis=(0, 1)) / 255.0
    return np.hstack([hist, mean_rgb])

def detect_visitors(csv_path='location1.csv', threshold=0.25):
    """Main detection function"""
    df = pd.read_csv(csv_path).sort_values('timestamp')
    
    centroids = []
    visitor_ids = []
    
    for _, row in df.iterrows():
        img_path = ts_to_path(row['timestamp'])
        feat = get_descriptor(img_path, row['bbox'])
        
        if not centroids:
            centroids.append(feat)
            visitor_ids.append(0)
        else:
            distances = [np.linalg.norm(feat - c) for c in centroids]
            min_dist = min(distances)
            
            if min_dist > threshold:
                centroids.append(feat)
                visitor_ids.append(len(centroids) - 1)
            else:
                idx = np.argmin(distances)
                centroids[idx] = 0.5 * centroids[idx] + 0.5 * feat
                visitor_ids.append(idx)
    
    df['visitor_id'] = visitor_ids
    unique_count = len(set(visitor_ids))
    
    print(f"Total events: {len(df)}")
    print(f"Unique visitors: {unique_count}")
    print(f"Events per visitor: {len(df) / unique_count:.2f}")
    
    return df, unique_count

def main():
    parser = argparse.ArgumentParser(description='Visitor Detection')
    parser.add_argument('--threshold', type=float, default=0.25, help='Clustering threshold')
    parser.add_argument('--output', default='location1_with_ids.csv', help='Output file')
    args = parser.parse_args()
    
    df, unique_count = detect_visitors(threshold=args.threshold)
    df.to_csv(args.output, index=False)
    
    print(f"Result: {unique_count} unique visitors detected")
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main() 
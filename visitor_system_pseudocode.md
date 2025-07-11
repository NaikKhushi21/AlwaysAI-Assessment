# Visitor Identification System - Simple Logic Flow

## Main System Loop

```
WHILE store is open:
  
    1. GET image from camera
  
    2. DETECT people in image
       IF no people found → go back to step 1
  
    3. FOR each detected person:
     
       a) EXTRACT face features (if face visible)
       b) EXTRACT appearance features (clothing colors, body shape)
       c) COMBINE face + appearance → create feature vector
     
       d) COMPARE feature vector to all stored visitor profiles
     
       e) IF closest match distance < threshold:
            → ASSIGN existing visitor ID
            → UPDATE that visitor's profile (moving average)
          ELSE:
            → CREATE new visitor ID
            → STORE new profile in database
     
       f) LOG event: timestamp, visitor_ID, location, entry/exit
  
    4. UPDATE analytics dashboard
  
    5. REPEAT

END WHILE
```

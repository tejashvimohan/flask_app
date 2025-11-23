import cv2
import pickle
import numpy as np
from deepface import DeepFace


# --- CONFIGURATION ---
DETECTOR_BACKEND = "opencv" 
MODEL_NAME = "VGG-Face"     
THRESHOLD = 0.50            



def capture_embedding():
        
    print("[INFO] Registering Student Face. Press 'c' to capture and 'q' to quit.")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: 
            break

        cv2.putText(frame, "Press 'c' to Capture face", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Face Registration", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        
        elif key == ord('c'):
            try:
                # Generate Embedding
                results = DeepFace.represent(
                    img_path=frame, 
                    model_name=MODEL_NAME, 
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=True
                )
                
                if results:
                    
                    embedding_list = results[0]["embedding"]
                    embedding_array = np.array(embedding_list, dtype=np.float32)
                    
                    embedding_blob = pickle.dumps(embedding_array)
                    
                   
                    
                    print("[Success] Student face embedding captured successfully.")
                    break
                
            except ValueError:
                print("[ERROR] No face detected. Try again!")
            except Exception as e:
                print(f"[ERROR] {e}")

    cap.release()
    cv2.destroyAllWindows()      
    
    return embedding_blob
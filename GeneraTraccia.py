import json
import cv2

def draw_bbox_from_json(video_path, json_path, output_path):

    with open(json_path, 'r') as f:
        bbox_data = json.load(f)

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_idx = 0

    trace = []

    while True:
        ret, frame = cap.read()
        if not ret:  # Se non ci sono più frame, esci
            break

        frame_key = f"{frame_idx:05d}"

        if frame_key in bbox_data:
            bbox = bbox_data[frame_key]
            center_x, center_y = int(bbox["x"]), int(bbox["y"])
            w, h = 30, 30  # Dimensione del bounding box

            trace.append((center_x, center_y)) # Memorizzo centro del pallone
            if len(trace) > 10:
                trace.pop(0)

            c1 = (center_x - w // 2, center_y - h // 2)  # Vertice superiore sinistro
            c2 = (center_x + w // 2, center_y + h // 2)  # Vertice inferiore destro

            color = (255, 255, 255)

            # Disegna la traccia
            for i in range(1, len(trace)):
                thickness = (len(trace)+i) - len(trace)  # Spessore decrescente: massimo vicino al pallone
                cv2.circle(frame, trace[i], 5, color, thickness)
            cv2.rectangle(frame, c1, c2, color, 2)


        out.write(frame)

        cv2.imshow("Frame with BBox", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_idx += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

video_path = "testset/ID-6.avi"
json_path = "annotazione1.json"
output_path = "output_with_bbox_6.avi"

draw_bbox_from_json(video_path, json_path, output_path)
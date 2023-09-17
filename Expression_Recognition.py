import numpy as np
import cv2
from keras.models import model_from_json, load_model
import keras.utils as image
from utils.utils_fr.utils_fr import rescale_frame


def main():
    face_cascade = cv2.CascadeClassifier(
        "./utils/utils_fr/haarcascades/haarcascade_frontalface_default.xml"
    )
    model = model_from_json(
        open("./utils/utils_fr/facial_expression_model_structure.json", "r").read()
    )
    model.load_weights("./utils/utils_fr/facial_expression_model_weights.h5")

    emotions = ("angry", "disgust", "fear", "happy", "sad", "surprise", "neutral")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # print(faces) #locations of detected faces

        for x, y, w, h in faces:
            cv2.rectangle(
                img, (x, y), (x + w, y + h), (255, 0, 0), 2
            )  # draw rectangle to main image

            detected_face = img[
                int(y) : int(y + h), int(x) : int(x + w)
            ]  # crop detected face
            detected_face = cv2.cvtColor(
                detected_face, cv2.COLOR_BGR2GRAY
            )  # transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48

            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis=0)

            img_pixels /= 255

            predictions = model.predict(img_pixels)

            # find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[max_index]

            cv2.putText(
                img,
                emotion,
                (int(x), int(y)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

        cv2.imshow("Res", rescale_frame(img, percent=130))
        if cv2.waitKey(5) & 0xFF == 32:
            break

    # kill open cv things
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

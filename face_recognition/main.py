import argparse
import face_recognition
import cv2
import os
import numpy as np


def collect(name):
    if name == None:
        raise("what's your name? ")

    cap = cv2.VideoCapture(0)
    ok = False
    while True:
        ret, frame = cap.read()
        if ret == False:
            raise('Cemera error!')

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_location = face_recognition.face_locations(small_frame)

        if len(face_location) > 1:
            cv2.putText(frame, 'please ensure there is only one person in the picture!', (0, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        elif len(face_location) == 1:
            ok = True
            cv2.putText(frame, 'please type "c" to take the picture!', (0, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        else:
            cv2.putText(frame, 'no face detected!', (0, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        cv2.imshow('', frame)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            print('quit!')
            break
        elif k & 0xFF == ord('c'):
            print('collect ' + name + "'s data successfully!")
            cv2.imwrite('./known/' + name + '.jpg', frame)
            break

        ok = False

    cap.release()
    cv2.destroyAllWindows()


def main():
    print('Initializing...')
    image_names = os.listdir('./known')
    known_encodings = []
    names = []
    for image_name in image_names:
        image = face_recognition.load_image_file(os.path.join("./known", image_name))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(face_encoding)
        names.append(os.path.splitext(image_name)[0])
        print(image_name)
    print('Done!')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if ret == False:
            raise('Cemera error!')

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_location = face_recognition.face_locations(small_frame)

        if len(face_location) > 1:
            cv2.putText(frame, 'please ensure there is only one persion in the picture!', (0, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
        elif len(face_location) == 1:
            face_encoding = face_recognition.face_encodings(small_frame, face_location)[0]

            # match = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.4)
            # prediction = 'unknown'
            # for i, known in enumerate(match):
            #     if known == True:
            #         predection = names[i]

            distance = face_recognition.face_distance(known_encodings, face_encoding)
            idx = np.argmin(distance)
            if distance[idx] < 0.6:
                prediction = 'Door is opened! Wellcome' + names[idx]
            else:
                prediction = 'Unknown locked'

            for (top, right, bottom, left) in face_location:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, prediction, (0, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                # cv2.putText(frame, prediction, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('quit!')
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='face recognition demo')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--collect', help='add a new person into dataset', action="store_true")
    group.add_argument('-r', '--recognition', help='predict the ID of a persion', action="store_true")
    parser.add_argument('-n', '--name', help='person name', type=str)
    args = parser.parse_args()
    if args.recognition:
        main()
    elif args.collect:
        collect(args.name)

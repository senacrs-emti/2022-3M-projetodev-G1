# https://medium.com/@sumantrajoshi/face-recognizer-application-using-a-deep-learning-model-python-and-keras-2873e9aa6ab3
# https://medium.com/data-science-lab-amsterdam/face-recognition-with-python-in-an-hour-or-two-d271324cbeb3

import face_recognition
import cv2
import numpy as np
import glob
import os
import logging
import pymysql, pymysql.cursors


IMAGES_PATH = './faces' 
CAMERA_DEVICE_ID = 0
MAX_DISTANCE = 0.6

"""
Take a raw image and run both the face detection and face embedding model on it
"""
def get_face_embeddings_from_image(image, convert_to_rgb=False):
    #converte de BGR to RBG se precisar
    if convert_to_rgb:
        image = image[:, :, ::-1]

    # roda o rosto detecta o modelopara encontrar os locais do rosto
    face_locations = face_recognition.face_locations(image)

  # execute o modelo de incorporação para obter incorporações de face para os locais fornecidos
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings

"""
Load reference images and create a database of their face encodings
"""
def setup_database(faceid):
    database = {}

    for filename in glob.glob(os.path.join(IMAGES_PATH, '*.jpg')):
        # carregar
        image_rgb = face_recognition.load_image_file(filename)

        # use o nome no nome do arquivo como a chave de identidade
        identity = os.path.splitext(os.path.basename('faceid'))[0]

        # obter a codificação facial e vinculá-la à identidade
        locations, encodings = get_face_embeddings_from_image(image_rgb)
        database[identity] = encodings[0]

    return database



# abrir uma conexão com a câmera
video_capture = cv2.VideoCapture(CAMERA_DEVICE_ID)

# ler da câmera em um loop, quadro a quadro
while video_capture.isOpened():
    
# Pegue um único quadro de vídeo
    ok, frame = video_capture.read()
    
    #Exibir a imagem
    cv2.imshow('Nome da tela', frame)

    # Pressione 'q' no teclado para parar o loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    # liberar identificador para a webcam
    video_capture.release()

    # feche a janela (com erros em um Mac btw)
    cv2.destroyAllWindows()

    # executar modelos de detecção e incorporação
    face_locations, face_encodings = get_face_embeddings_from_image(frame, convert_to_rgb=True)

# a biblioteca face_recognition usa chaves e valores de seu banco de dados separadamente
    known_face_encodings = list(database.values())
    known_face_names = list(database.keys())

# Percorra cada rosto neste quadro de vídeo e veja se há uma correspondência
    for location, face_encoding in zip(face_locations, face_encodings):

        # obtenha as distâncias desta codificação para as de todas as imagens de referência
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        # selecione a correspondência mais próxima (menor distância) se estiver abaixo do valor limite
        if np.any(distances <= MAX_DISTANCE):
            best_match_idx = np.argmin(distances)
            name = known_face_names[best_match_idx]
        else:
            name = None

        # mostrar informações de reconhecimento na imagem
        paint_detected_face_on_image(frame, location, name)

    """
    Paint a rectangle around the face and write the name
    """
    def paint_detected_face_on_image(frame, location, name=None):
        
        # descompacte as coordenadas da tupla de localização
        top, right, bottom, left = location

        if name is None:
            name = 'Unknown'
            color = (0, 0, 255)  # red for unrecognized face
        else:
            color = (0, 128, 0)  # dark green for recognized face

        # Desenhe uma caixa ao redor do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Desenhe uma etiqueta com um nome abaixo do rosto
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)


    """
    Start the face recognition via the webcam
    """
    def run_face_recognition(database):
        # Abra um manipulador para a câmera
        video_capture = cv2.VideoCapture(CAMERA_DEVICE_ID)

        # a biblioteca face_recognitino usa chaves e valores do seu banco de dados separadamente
        known_face_encodings = list(database.values())
        known_face_names = list(database.keys())
        
        while video_capture.isOpened():
            #Pegue um único quadro de vídeo (e verifique se deu tudo certo)
            ok, frame = video_capture.read()
            if not ok:
                logging.error("Could not read frame from camera. Stopping video capture.")
                break

            # executar modelos de detecção e incorporação
            face_locations, face_encodings = get_face_embeddings_from_image(frame, convert_to_rgb=True)

            # Percorra cada rosto neste quadro de vídeo e veja se há uma correspondência
            for location, face_encoding in zip(face_locations, face_encodings):

                #obtenha as distâncias desta codificação para as de todas as imagens de referência
                distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                # selecione a correspondência mais próxima (menor distância) se estiver abaixo do valor limite
                if np.any(distances <= MAX_DISTANCE):
                    best_match_idx = np.argmin(distances)
                    name = known_face_names[best_match_idx]
                else:
                    name = None

                # colocar informações de reconhecimento na imagem
                paint_detected_face_on_image(frame, location, name)

                print(name)

            # Exibir a imagem resultante
            cv2.imshow('Video', frame)

            # Pressione 'q' no teclado para sair!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #Solte o identificador para a webcam
        video_capture.release()
        cv2.destroyAllWindows()









## Executar code
database = setup_database()
run_face_recognition(database)
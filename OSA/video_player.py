from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, QTimer, QObject, pyqtSignal

import cv2
import os
import mediapipe as mp
import numpy as np
import math
import time
from move_detec import *
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
class VideoPlayer(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def __init__(self, exercise_type, videostream_path, scores_updater):
        super().__init__()
        self.exercise_type = exercise_type
        self.videostream_path = videostream_path
        self.scores_update = scores_updater

    def run(self):
        self.ThreadActive = True


        self.cap = cv2.VideoCapture(self.videostream_path)
        local_best_score = 0
        while self.ThreadActive:
            with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5,
                              min_tracking_confidence=0.5) as pose:

            ###
                ret, frame = self.cap.read()
                if ret:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Обработка позы человека
                    results = pose.process(image)

                    # Проверка наличия обнаруженных поз
                    if results.pose_landmarks is not None:
                        # Проверка правильно положения тела
                        corr_pos = self.exercise_type.is_correct_pose(results.pose_landmarks)

                        # ДОБАВИТЬ УВЕДОМЛЕНИЕ ОБ отсутстивв чатси тела в кадре
                        score = 0
                        if corr_pos:
                            score = self.exercise_type.do()

                        # Вывод положения на изображение
                        if score > local_best_score:
                            local_best_score = score
                        #score_str_repr = str(corr_pos) + '; current score: ' + self.exercise_type.get_beauty_score(score)
                        #best_score_str_repr = 'Local best: ' + self.exercise_type.get_beauty_score(local_best_score)

                        # print()
                        #pos_color = (0, 0, 255)
                        if corr_pos:
                            pos_color = (0, 255, 0)
                        self.scores_update(self.exercise_type, score, local_best_score)
                        #cv2.putText(frame, score_str_repr, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, pos_color, 2, cv2.LINE_AA)
                        #cv2.putText(frame, best_score_str_repr, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, pos_color, 2,
                        #            cv2.LINE_AA)
                        ###

                        #mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        #                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                        #                                                 circle_radius=2),
                        #                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                        #                          )
                    else:
                        pass
                        #position = "No person in Frame"
                        #cv2.putText(frame, position, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    # Отображение кадра

                    Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    #FlippedImage = cv2.flip(Image, 1)
                    ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(Pic)
    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        self.ThreadActive = False
        self.quit()
    def __del__(self):
        self.cap.release()

def get_available_cameras_dict():
    # Получение списка доступных камер
    camera_dict = {}
    num_cameras = 0
    template = 'Cam '
    while True:
            cap = cv2.VideoCapture(num_cameras, cv2.CAP_DSHOW)
            if not cap.read()[0]:
                break
            camera_dict[template+str(num_cameras)] = num_cameras
            cap.release()
            num_cameras += 1
    return camera_dict
#!pip install mediapipe opencv-python

import cv2
import mediapipe as mp
import numpy as np
import math
import time
from notifier import Notifier
#mport chime

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def placeholder():
    pass
def distance_between_points(point1, point2):
    squared_distance = (point2.x - point1.x)**2 + (point2.y - point1.y)**2
    return math.sqrt(squared_distance)
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def calculate_distance(p1, p2):
    d2d = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    #distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    d1d = abs(p1.y - p2.y)
    return d2d*0.9 < d1d

def is_in_frame(point):
    if (point.x > 0 and point.x < 1) and (point.y > 0 and point.y < 1):
        return True
    return False

def push_up_corr(p1, p2):
    dy = abs(p1.y - p2.y)
    dx = abs(p1.x - p2.x)
    return dx > dy

class PushUp:
    def __init__(self, notifier = placeholder):
        self.notify = notifier
        self.stage = None
        self.counter = 0

    def pose_requirements(self):
        return '''встаньте в положение отжимений сбоку от камеры так что бы было видно: плечи, локти, колени и кисти'''

    def beauty_name(self):
        return 'Push Ups'
    def path_to_example_img(self):
        return r"\exercise_examples\push_up.png"

    def score_scaler(self):
        return 3

    def path_to_video_example(self):
        # r"vidoe_examples\push_up_h.mp4" - horizontal camera setup
        # r"vidoe_examples\push_up_v.mp4" - vertical camera setup
        return r"vidoe_examples\push_up.mp4"

    def is_correct_pose(self, pase_land):
        left_shoulder = pase_land.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        left_elbow = pase_land.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

        left_wirst = pase_land.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wirst = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

        left_knee = pase_land.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

        is_corr = False

        if (is_in_frame(left_shoulder) and is_in_frame(left_knee) and
            is_in_frame(left_elbow) and is_in_frame(left_wirst) ):
            self.shoulder = left_shoulder
            self.elbow = left_elbow
            self.wirst = left_wirst
            #self.side = 'left'
            is_corr = (push_up_corr(left_shoulder, left_knee))

        elif (is_in_frame(right_shoulder) and is_in_frame(right_knee) and
            is_in_frame(right_elbow) and is_in_frame(right_wirst) ):
            self.shoulder = right_shoulder
            self.elbow = right_elbow
            self.wirst = right_wirst
            #self.side = 'right'
            is_corr = (push_up_corr(right_shoulder, right_knee))
        #врядли кому то нужны бубдут атрибуты, если нет правильной позиции
        if is_corr:
            return True
        else:
            self.shoulder = None
            self.elbow = None
            self.wirst = None
            self.stage = None
            self.counter = 0
            return False

    def do(self):
        assert (self.shoulder is not None or
            self.elbow is not None or
            self.wirst is not None), 'shoulder, elbow or wirst is None'

        angle = calculate_angle([self.shoulder.x, self.shoulder.y],
                                [self.elbow.x, self.elbow.y],
                                [self.wirst.x, self.wirst.y])
        if angle > 150 and self.stage == 'down':
            self.counter += 1
            self.stage = 'up'
            self.notify()
        elif angle > 150:
            self.stage = 'up'
        elif angle < 110 and self.stage == 'up':
            self.stage = 'down'
        #if self.stage
        return self.counter# + ' ' + self.stage

    def get_beauty_score(self, score):
        return str(score)



def squats_corr(hip, knee, ankle):
    #print(hip.y, knee.y, ankle.y)
    #return hip.y < knee.y # < ankle.y
    return True

class Squats:
    def __init__(self, notifier = placeholder):
        self.notify = notifier
        self.stage = None
        self.counter = 0

    def pose_requirements(self):
        return '''встаньте сбоку от камеры так что бы было видно: ступни, колени и таз'''

    def beauty_name(self):
        return 'Squats'

    def path_to_example_img(self):
        return r"\exercise_examples\squats.png"

    def path_to_video_example(self):
        # r"vidoe_examples\squats_h.mp4" - horizontal camera setup
        # r"vidoe_examples\squats_v.mp4" - vertical camera setup
        return r"vidoe_examples\squats.mp4"

    def score_scaler(self):
        return 2

    def is_correct_pose(self, pase_land):
        left_hip = pase_land.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        left_knee = pase_land.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

        left_ankle = pase_land.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        is_corr = False

        if is_in_frame(left_hip) and is_in_frame(left_knee) and is_in_frame(left_ankle) :
            self.hip = left_hip
            self.knee = left_knee
            self.ankle = left_ankle
            #self.side = 'left'
            is_corr = squats_corr(hip= self.hip, knee= self.knee, ankle=self.ankle)

        elif is_in_frame(right_hip) and is_in_frame(right_knee) and is_in_frame(right_ankle) :
            self.hip = right_hip
            self.knee = right_knee
            self.ankle = right_ankle
            #self.side = 'right'
            is_corr = squats_corr(hip= self.hip, knee= self.knee, ankle=self.ankle)

        #врядли кому то нужны бубдут атрибуты, если нет правильной позиции
        if is_corr:
            return True
        else:
            self.hip = None
            self.knee = None
            self.ankle = None
            self.stage = None
            self.counter = 0
            return False

    def do(self):
        assert (self.hip is not None or
            self.knee is not None or
            self.ankle is not None), 'hip, knee or ankle is None'

        angle = calculate_angle([self.hip.x, self.hip.y],
                                [self.knee.x, self.knee.y],
                                [self.ankle.x, self.ankle.y])
        if angle > 120 and self.stage == 'down':
            self.counter += 1
            self.stage = 'up'
            self.notify()
        elif angle > 120:
            self.stage = 'up'
        elif angle < 110 and self.stage == 'up':
            self.stage = 'down'
        #if self.stage
        #print(angle)
        return self.counter# + ' ' + self.stage

    def get_beauty_score(self, score):
        return str(score)


class Posture:
    def __init__(self, notifier = placeholder):
        self.notify = notifier
        self.first_iter = True
        self.stage = 'OK'
        self.time = 0
        self.last_incorret_pose_time = 0
        self.last_notify_time = 0

    def beauty_name(self):
        return 'Posture'

    def pose_requirements(self):
        return '''сядьте сбоку от камеры так что бы угол в колене был 90 градусов и держите шею прямо нос, плечи, таз, колени и ступни должны быть в кадре'''

    def path_to_example_img(self):
        return r"\exercise_examples\posture.jpg"

    def path_to_video_example(self):
        # only vertical recording format
        return r"vidoe_examples\posture.mp4"

    def score_scaler(self):
        return 0.01
    def change_time(self):
        time_now = time.time()

        if self.time == 0:
            self.time = time_now
        if self.last_incorret_pose_time == 0:
            self.last_incorret_pose_time = time_now
        #else:
        #
        #print(self.time, self.last_incorret_pose_time)
        if self.stage == 'OK':
            self.last_incorret_pose_time = time_now
            self.stage = 'WR'
        elif self.stage == 'WR':
            elapsed_time = time_now - self.last_incorret_pose_time
            if elapsed_time >= 2:
                self.time = time_now
                self.last_incorret_pose_time = time_now
                if time_now - self.last_notify_time > 10:
                    self.last_notify_time = time_now
                    self.notify()
        return
        #
        '''time_now = time.time()
        elapsed_time = time_now - self.last_incorret_pose_time
        if elapsed_time <= 3:
            self.time = time_now
            self.last_incorret_pose_time = time_now
            #if time_now - self.last_sound_time > 10:
            #    self.last_sound_time = time_now
            #    chime.success(sync=True)
        else:
            pass'''
        #self.last_incorret_pose_time = time.time()
    def sec_to_hms(self, sec):
        hours = sec // 3600  # Получение количества часов
        minutes = (sec % 3600) // 60  # Получение количества минут
        seconds = sec % 60  # Получение количества секунд

        return 'H: {}; M: {}; S: {}'.format(hours, minutes, seconds)
    def is_correct_pose(self, pase_land):
        self.nose = pase_land.landmark[mp_pose.PoseLandmark.NOSE]

        left_hip = pase_land.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        left_knee = pase_land.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

        left_ankle = pase_land.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        left_shoulder = pase_land.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        left_wrist = pase_land.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pase_land.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

        is_corr = False
        self.wrist = None

        if (is_in_frame(self.nose) and is_in_frame(left_hip) and is_in_frame(left_knee) and
            is_in_frame(left_ankle) and is_in_frame(left_shoulder)) :
            self.hip = left_hip
            self.knee = left_knee
            self.ankle = left_ankle
            self.shoulder = left_shoulder
            #self.side = 'left'
            is_corr = True
            if is_in_frame(left_wrist):
                self.wrist = left_wrist

        elif (is_in_frame(self.nose) and is_in_frame(right_hip) and is_in_frame(right_knee) and
            is_in_frame(right_ankle) and is_in_frame(right_shoulder)) :
            self.hip = right_hip
            self.knee = right_knee
            self.ankle = right_ankle
            self.shoulder = right_shoulder
            #self.side = 'left'
            is_corr = True
            if is_in_frame(right_wrist):
                self.wrist = right_wrist


        #врядли кому то нужны бубдут атрибуты, если нет правильной позиции
        if is_corr:
            return True
        else:
            self.hip = None
            self.knee = None
            self.ankle = None
            self.stage = 'OK'
            self.wrist = None
            self.change_time()
            return False

    def do(self):
        assert (self.hip is not None or
            self.knee is not None or
            self.ankle is not None), 'hip, knee or ankle is None'

        head_tilt = calculate_angle([self.nose.x, self.nose.y],
                                [self.shoulder.x, self.shoulder.y],
                                [self.hip.x, self.hip.y])

        knee_angle = calculate_angle([self.hip.x, self.hip.y],
                                [self.knee.x, self.knee.y],
                                [self.ankle.x, self.ankle.y])
        if self.first_iter:
            self.first_iter = False
            self.change_time()

        if not (head_tilt > 110 and head_tilt < 150):
            self.change_time()
        elif not(knee_angle > 80 and knee_angle < 110):
            self.change_time()
        elif (self.wrist is not None) and distance_between_points(self.wrist, self.shoulder) < 0.1:
            # print(distance_between_points(self.wrist, self.shoulder), distance_between_points(self.hip, self.shoulder))
            #if distance_between_points(self.wrist, self.shoulder) < 0.1:
            self.change_time()
        else:
            self.stage = 'OK'
            '''elif self.wrist is not None:
                        #print(distance_between_points(self.wrist, self.shoulder), distance_between_points(self.hip, self.shoulder))
                        if distance_between_points(self.wrist, self.shoulder)  < 0.1:
                            self.change_time()'''
        if self.wrist is not None:
            # print(distance_between_points(self.wrist, self.shoulder), distance_between_points(self.hip, self.shoulder))
            if distance_between_points(self.wrist, self.shoulder) < 0.1:
                self.change_time()
        #if self.stage
        #print('head',head_tilt,'knee', knee_angle)
        returning_value = time.time() - self.time
        #print(returning_value)
        if returning_value > 10_000_000:
            returning_value = 0
        return round(returning_value) #self.to_beautifull_time(self.counter)# + ' ' + self.stage

    def get_beauty_score(self, score):
        return self.sec_to_hms(score)


if __name__ == "__main__":

    pass
    #ex_type = PushUp()
    #ex_type = Squats()
    #ex.start(exercise_type=ex_type, cam_path = ex_type.path_to_video_example())









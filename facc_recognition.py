import face_recognition
from wx.lib import statbmp
import os
import traceback
import cv2
import wx
import numpy as np
import time

# #open camera
# video_capture = cv2.VideoCapture(0)
#
# #load image which is alreading known and encoding
# load_image1 = face_recognition.load_image_file("./known_people/yn.jpg")
# image_encoding1 = face_recognition.face_encodings(load_image1)[0]
# load_image2 = face_recognition.load_image_file("./known_people/qy.jpg")
# image_encoding2 = face_recognition.face_encodings(load_image2)[1]
#
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
#
# while True:
# #get frame
#     ret, frame = video_capture.read()

class ShowCapture(wx.Frame):
    def __init__(self, capture, fps=15):
        wx.Frame.__init__(self, None)
        panel = wx.Panel(self, -1)

        # create a grid sizer with 5 pix between each cell
        sizer = wx.GridBagSizer(5, 5)
        self.flag = 0

        self.capture = capture
        ret, frame = self.capture.read()

        height, width = frame.shape[:2]
        self.orig_height = height
        self.orig_width = width

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("initiating...")

        image_names = os.listdir('./known')
        self.known_encodings = []
        self.names = []
        for image_name in image_names:
            image = face_recognition.load_image_file(os.path.join("./known", image_name))
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_encodings.append(face_encoding)
            self.names.append(os.path.splitext(image_name)[0])
            print(image_name)
        print('Done!')

        # create image display widgets
        self.ImgControl = statbmp.GenStaticBitmap(panel, wx.ID_ANY, self.bmp)

        collectButton = wx.Button(panel, label='collect', pos=(20, 20), size=(125,40))
        recognitionButton = wx.Button(panel, label='recognite', pos=(100, 80), size=(125,40))
        deleteButton = wx.Button(panel, label='delete', pos=(100, 140), size=(125,40))

        self.nameTest = wx.TextCtrl(panel, value='',pos=(100,200), size=(200,40))#, validator=wx.TE_CENTER)

        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer.Add(collectButton, 0)
        box_sizer.Add(recognitionButton, 0)
        box_sizer.Add(deleteButton, 0)
        box_sizer.Add(self.nameTest,0)
        sizer.Add(box_sizer, (0, 0), wx.DefaultSpan, wx.ALIGN_RIGHT)

        sizer.Add(self.ImgControl, (1, 0), (0, 0), wx.EXPAND | wx.CENTER | wx.LEFT | wx.BOTTOM, 5)

        # set the sizer and tell the Frame about the best size
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        # start a timer that's handler grabs a new frame and updates the image widgets
        self.timer = wx.Timer(self)
        self.fps = fps
        self.timer.Start(1000. / self.fps)

        #bind timer events to the handler
        self.Bind(wx.EVT_TIMER, self.NextFrame)

        collectButton.Bind(wx.EVT_BUTTON, self.onClickCollect)
        recognitionButton.Bind(wx.EVT_BUTTON, self.onClickRecognite)
        deleteButton.Bind(wx.EVT_BUTTON, self.onClickDelete)

    def onClickCollect(self, event):
        self.str = self.nameTest.GetValue()
        self.flag = 1
        print("collect", self.str)

    def onClickRecognite(self, event):
        self.flag = 0
        print("recognite")

    def onClickDelete(self, event):
        print("delete")

    def NextFrame(self, event):
        try:
            time.sleep(0.03)
            ret, self.orig_frame = self.capture.read()
            if ret:
                small_frame = cv2.resize(self.orig_frame, (0, 0), fx=0.25, fy=0.25)
                face_location = face_recognition.face_locations(small_frame)

                if len(face_location) > 1:
                    self.statusbar.SetStatusText('please ensure there is only one person in the picture!')
                elif len(face_location) == 1:
                    if self.flag == 0:
                        face_encoding = face_recognition.face_encodings(small_frame, face_location)[0]
                        distance = face_recognition.face_distance(self.known_encodings, face_encoding)
                        idx = np.argmin(distance)
                        if distance[idx] < 0.6:
                            prediction = self.names[idx]+ ' opened'
                        else:
                            prediction = 'Unknown locked'

                        for (top, right, bottom, left) in face_location:
                            top *= 4
                            right *= 4
                            bottom *= 4
                            left *= 4

                            cv2.rectangle(self.orig_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                            self.statusbar.SetStatusText(prediction)
                    else:
                        cv2.imwrite('./known/' + self.str + '.jpg', self.orig_frame)
                        self.flag = 0
                else:
                    self.statusbar.SetStatusText('no face detected!')

                frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)
                self.bmp.CopyFromBuffer(frame)
                self.ImgControl.SetBitmap(self.bmp)

            else:
                print("camera error")
        except:
            traceback.print_exc()
            print("error")


capture = cv2.VideoCapture(0)

app = wx.App()
frame = ShowCapture(capture)
frame.Show()
app.MainLoop()
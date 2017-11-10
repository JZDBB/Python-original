import argparse
import face_recognition
import cv2
import os
import numpy as np
import wx
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (' ' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        print(plain_text)
        strip_text = plain_text.rstrip()
        str_text = strip_text.decode()
        return str_text


class SubclassDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Dialog Subclass', size=(300, 100))

        static = wx.StaticText(self, -1, label='haha', pos=(10, 10))
        okButton = wx.Button(self,wx.ID_OK, "OK", pos=(10, 30))
        okButton.SetDefault()
        cancelButton = wx.Button(self,wx.ID_CANCEL, "Cancel", pos=(115, 30))

        okButton.Bind(wx.EVT_BUTTON, self.onClickOk)

    def onClickOk(self, event):
        collect('haha')
        print('collect')

class RootDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title='Root')
        panel = wx.Panel(self, -1)

        self.flag_ok = 0
        self.pc = prpcrypt('keys1234keys1234')

        sizer = wx.BoxSizer(wx.VERTICAL)
        userStaticText0 = wx.StaticText(panel, -1, 'Username:')
        self.UserText0 = wx.TextCtrl(panel, value='', size=(230, 30))
        pwStaticText0 = wx.StaticText(panel, -1, 'Password:')
        self.pwText0 = wx.TextCtrl(panel, value='', size=(230, 30))
        RootStaticText = wx.StaticText(panel, -1, 'RootPassword:')
        self.RootText = wx.TextCtrl(panel, value='', size=(230, 30))
        openButton = wx.Button(panel, label='root', pos=(120, 100), size=(110, 30))
        self.StatusText = wx.StaticText(panel, -1, 'Administrator login')
        sizer.Add(userStaticText0, 0)
        sizer.Add(self.UserText0, 0)
        sizer.Add(pwStaticText0, 0)
        sizer.Add(self.pwText0, 0)
        sizer.Add(RootStaticText, 0)
        sizer.Add(self.RootText, 0)

        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(openButton, 0)
        sizer.Add(self.StatusText, 0)

        # sizer.Add(resignButton, 0)
        # sizer.Add(openButton, 0)
        panel.SetSizer(sizer)
        sizer.SetSizeHints(self)
        panel.Layout()
        panel.SetFocus()

        openButton.Bind(wx.EVT_BUTTON, self.onClickOpen)

    def onClickOpen(self, event):
        try:
            pw0 = open("./Users/Root.txt", 'r').read()
            pw1 = pw0.encode(encoding='utf-8')
            rootPassword = self.pc.decrypt(pw1)
            print(rootPassword)
        except IOError:
            print('The datafile is missing!')
        readpassword = self.RootText.GetValue()
        if readpassword == rootPassword:
            self.flag_ok = 1
            self.StatusText.SetLabel('Accomplished!')
            self.Username0 = self.UserText0.GetValue()
            self.password0 = self.pwText0.GetValue()
            data = open("./Users/Users.txt", 'a')
            try:
                str = self.Username0 + ':' + self.password0
                bit_data = self.pc.encrypt(str)
                write_data = '\n' + bit_data.decode()
                data.write(write_data)
                data.close()
            except:
                print('write error')
            # Users.users.append(self.Username0)
            # Users.passwords.append(self.password0)
        else:
            self.StatusText.SetLabel('Wrong password!')
        print('root')

class UserDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title='Sign in', size=(300, 200))
        sizer = wx.BoxSizer(wx.VERTICAL)
        okButton = wx.Button(self, wx.ID_OK, 'OK', pos=(20, 120))
        cancelButton = wx.Button(self, wx.ID_CANCEL, 'Cancel', pos=(100, 120))
        staticTextname = wx.StaticText(self, -1, label='Username', pos=(10, 10))
        self.nameText = wx.TextCtrl(self, -1, size=(110, 30))
        staticTextpw = wx.StaticText(self, -1, label='Password', pos=(10, 50))
        self.pwText = wx.TextCtrl(self, -1, size=(110, 30))
        sizer.Add(staticTextname, 0)
        sizer.Add(self.nameText, 0)
        sizer.Add(staticTextpw, 0)
        sizer.Add(self.pwText, 0)

        self.StatusText = wx.StaticText(self, -1, '')

        self.users = []
        self.passwords = []
        self.pc = prpcrypt('keys1234keys1234')

        try:
            data = open("./Users/Users.txt")
            for each_line in data:
                Line = each_line.replace('\n', '')
                line = Line.encode(encoding='utf-8')
                try:
                    decode_line = self.pc.decrypt(line)
                    (user, pw) = decode_line.split(':', 1)
                    self.users.append(user)
                    self.passwords.append(pw)
                    print(user + pw)
                except ValueError:
                    pass
            data.close()
        except:
            print('error')

        okButton.Bind(wx.EVT_BUTTON, wx.onClickOK)

    def onClickOK(self, event):
        user = self.nameText.GetValue()
        password = self.pwText.GetValue()
        try:
            idn = self.users.index(user)
            if password == self.passwords[idn]:
                str = 'opened! Wellcome '+ user
                self.StatusText.SetLabel(str)
            else:
                self.StatusText.SetLabel('Wrong password!')
        except:
            self.StatusText.SetLabel('User is not exist!')
        print('OK')

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
                prediction = names[idx]
            else:
                prediction = 'Unknown'

            for (top, right, bottom, left) in face_location:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, prediction, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('quit!')
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='face recognition')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--collect', help='add a new person into dataset', action="store_true")
    group.add_argument('-r', '--recognition', help='predict the ID of a persion', action="store_true")
    group.add_argument('-u', '--users', help='open the door with passwords', action="store_true")
    group.add_argument('-A', '--add', help='add a new user to open the door', action="store_true")
    parser.add_argument('-n', '--name', help='person name', type=str)
    args = parser.parse_args()
    if args.recognition:
        main()
    elif args.collect:
        collect(args.name)
    elif args.users:
        app = wx.App()
        dialog = UserDialog()
        result = dialog.ShowModal()
        if result == wx.ID_CANCEL:
            print('cancel')
        else:
            pass
        dialog.Destroy()
    elif args.add:
        app =wx.App()
        dialog = RootDialog()
        result = dialog.ShowModal()
        if result == wx.ID_CANCEL:
            print('cancel')
        else:
            pass
        dialog.Destroy()
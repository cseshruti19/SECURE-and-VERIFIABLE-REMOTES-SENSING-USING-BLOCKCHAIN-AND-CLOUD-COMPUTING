from flask import Flask, render_template, flash, request,session
from wtforms import Form, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import mysql.connector
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter.messagebox
import os, shutil
import urllib
import urllib.request
import urllib.parse
import datetime
import hashlib
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def split_into_str_num(string):
    letters = string.rstrip('0123456789-.')
    numbers = string[len(letters):]

    return [letters, numbers]
class Block:
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"

class Blockchain:

    diff = 20
    maxNonce = 2**32
    target = 2 ** (256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                break
            else:
                block.nonce += 1
def split_into_str_num(string):
    letters = string.rstrip('0123456789-.')
    numbers = string[len(letters):]

    return [letters, numbers]
c=1
@app.route("/")
def homepage():

    return render_template('index.html')

@app.route("/eam")

def eam():

    return render_template('server.html')
@app.route("/ownerhome")

def ownerhome():

    return render_template('ownerhome.html')
@app.route("/own")

def own():

    return render_template('owner.html')
@app.route("/reg")

def reg():

    return render_template('register.html')
@app.route("/serverhome")
def serverhome():

    return render_template('serverhome.html')
@app.route("/owndetails")
def owndetails():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM register")
    data = cur.fetchall()
    return render_template('owndetails.html', data=data)

    return render_template('owndetails.html')
@app.route("/fileview")
def fileview():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM file where status='0'")
    data = cur.fetchall()
    return render_template('fileview.html', data=data)
    return render_template('fileview.html')

@app.route("/view")
def view():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM file where uname='"+uname+"'")
    data = cur.fetchall()
    return render_template('view.html', data=data)

    return render_template('view.html')
@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM register")
            data = cur.fetchall()


            return render_template('serverhome.html', data=data)
        else:
            return render_template('index.html', error=error)

@app.route("/register",methods = ['GET', 'POST'])
def register():

    if request.method == 'POST':

        n = request.form['name']

        g = request.form['city']
        # st = request.form['station']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['pnumber']
        uname = request.form['uname']
        password = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO register VALUES ('','" + n + "','" + pnumber + "','" + address + "','" + g + "','" + email + "','"+ uname + "','" + password + "','0')")
        conn.commit()
        conn.close()
        flash("Logged in successfully.")
        return 'file uploaded successfully'
        return render_template('owner.html')

@app.route("/ownlogin",methods = ['GET', 'POST'])
def ownlogin():

    if request.method == 'POST':

        n = request.form['uname']
        session['uname'] = request.form['uname']
        g = request.form['password']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
        cursor = conn.cursor()
        cursor.execute("SELECT * from register where uname='" + n + "' and password='" + g + "' and status='0'")
        data = cursor.fetchone()

        if data is None:
            return 'Username or Password is wrong'
        else:
            return render_template('ownerhome.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():

        if request.method == 'POST':
            n1 = request.form['tlt']
            f = request.files['file']
            f.save("static/uploads/" + secure_filename(f.filename))
            g = request.form['details']
            uname = session['uname']            #pname = request.form['pname']
            drc = "templates/uploads/" + f.filename

            def split_into_str_num(string):
                letters = string.rstrip('0123456789-.')
                numbers = string[len(letters):]

                return [letters, numbers]

            d = os.path.splitext(f.filename)  # returns ('/home/user/somefile', '.txt')
            s = split_into_str_num(d[0])

            g1=s[0]

            #stock = request.form['stock']
            str1 = str(uname) + str(f.filename) + str(n1)
            result = hashlib.sha1(str1.encode())
            # printing the equivalent hexadecimal value.
            print("The hexadecimal equivalent of SHA1 is : ")
            print(result.hexdigest())
            b = result.hexdigest()
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
            cursor = conn.cursor()
            cursor.execute("select * from file");
            data = cursor.fetchone()
            print(data)
            if data is None:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO file VALUES ('','" + n1 + "','" + g + "','" + f.filename + "','"+str(g1)+"','0','"+str(b)+"')")
                conn.commit()
                conn.close()
            else:
                conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
                cursor1 = conn1.cursor()
                cursor1.execute("select max(id) from file")
                da = cursor1.fetchone()
                print(da)
                for i in da:
                    d = i
                print(d)
                # str()

                conn111 = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
                cursor111 = conn111.cursor()
                cursor111.execute("select * from file where id='" + str(d) + "'")
                da11 = cursor111.fetchall()
                for item11 in da11:
                    df1 = item11[6]
                    print(df1)

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO file VALUES ('','" + n1 + "','" + g + "','" + f.filename + "','"+str(g1)+"','" + str(
                        df1) + "','" + str(b) + "')")
                conn.commit()
                conn.close()
            import_file_path='static/uploads/' + f.filename
            image = cv2.imread(import_file_path)
            filename = 'Test.jpg'
            cv2.imwrite(filename, image)
            print("After saving image:")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Original image', image)
            cv2.imshow('Gray image', gray)
            # import_file_path = filedialog.askopenfilename()
            print(import_file_path)
            fnm = os.path.basename(import_file_path)
            print(os.path.basename(import_file_path))

            from PIL import Image, ImageOps

            im = Image.open(import_file_path)
            im_invert = ImageOps.invert(im)
            im_invert.save('lena_invert.jpg', quality=95)
            im = Image.open(import_file_path).convert('RGB')
            im_invert = ImageOps.invert(im)
            im_invert.save('tt.png')
            image2 = cv2.imread('tt.png')
            cv2.imshow("Invert", image2)

            """"-----------------------------------------------"""

            img = image

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Original image', img)
            # cv2.imshow('Gray image', gray)
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            cv2.imshow("Nosie Removal", dst)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            print("\n*********************\nImage : " + fnm + "\n*********************")
            img = cv2.imread(import_file_path)
            if img is None:
                print('no data')

            img1 = cv2.imread(import_file_path)
            print(img.shape)
            img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
            original = img.copy()
            neworiginal = img.copy()
            cv2.imshow('original', img1)
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Original image', img1)
            # cv2.imshow('Gray image', gray)
            p = 0
            for i in range(img.shape[0]):

                for j in range(img.shape[1]):
                    B = img[i][j][0]
                    G = img[i][j][1]
                    R = img[i][j][2]
                    if (B > 110 and G > 110 and R > 110):
                        p += 1

            totalpixels = img.shape[0] * img.shape[1]
            per_white = 100 * p / totalpixels
            if per_white > 10:
                img[i][j] = [500, 300, 200]
                cv2.imshow('color change', img)
            # Guassian blur
            blur1 = cv2.GaussianBlur(img, (3, 3), 1)
            # mean-shift algo
            newimg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            img = cv2.pyrMeanShiftFiltering(blur1, 20, 30, newimg, 0, criteria)
            cv2.imshow('means shift image', img)
            # Guassian blur
            blur = cv2.GaussianBlur(img, (11, 11), 1)
            cv2.imshow('Noise Remove', blur)
            corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10)
            corners = np.int0(corners)

            # we iterate through each corner,
            # making a circle at each point that we think is a corner.
            for i in corners:
                x, y = i.ravel()
                cv2.circle(image, (x, y), 3, 255, -1)

            plt.imshow(image), plt.show()

            return render_template('serverhome.html')

@app.route("/upload1", methods=['GET', 'POST'])
def upload1():

        if request.method == 'POST':

            f = request.files['file']
            f.save("static/uploads/" + secure_filename(f.filename))
            data1=f.filename


            drc = "templates/uploads/" + f.filename



            d = os.path.splitext(f.filename)  # returns ('/home/user/somefile', '.txt')
            s = split_into_str_num(d[0])

            g1=s[0]
            print(g1)

            #stock = request.form['stock']


            import_file_path='static/uploads/' + f.filename
            image = cv2.imread(import_file_path)
            filename = 'Test.jpg'
            cv2.imwrite(filename, image)
            print("After saving image:")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Original image', image)
            cv2.imshow('Gray image', gray)
            # import_file_path = filedialog.askopenfilename()
            print(import_file_path)
            fnm = os.path.basename(import_file_path)
            print(os.path.basename(import_file_path))

            from PIL import Image, ImageOps

            im = Image.open(import_file_path)
            im_invert = ImageOps.invert(im)
            im_invert.save('lena_invert.jpg', quality=95)
            im = Image.open(import_file_path).convert('RGB')
            im_invert = ImageOps.invert(im)
            im_invert.save('tt.png')
            image2 = cv2.imread('tt.png')
            cv2.imshow("Invert", image2)

            """"-----------------------------------------------"""

            img = image

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Original image', img)
            # cv2.imshow('Gray image', gray)
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            cv2.imshow("Nosie Removal", dst)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            print("\n*********************\nImage : " + fnm + "\n*********************")
            img = cv2.imread(import_file_path)
            if img is None:
                print('no data')

            img1 = cv2.imread(import_file_path)
            print(img.shape)
            img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
            original = img.copy()
            neworiginal = img.copy()
            cv2.imshow('original', img1)
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Original image', img1)
            # cv2.imshow('Gray image', gray)
            p = 0
            for i in range(img.shape[0]):

                for j in range(img.shape[1]):
                    B = img[i][j][0]
                    G = img[i][j][1]
                    R = img[i][j][2]
                    if (B > 110 and G > 110 and R > 110):
                        p += 1

            totalpixels = img.shape[0] * img.shape[1]
            per_white = 100 * p / totalpixels
            if per_white > 10:
                img[i][j] = [500, 300, 200]
                cv2.imshow('color change', img)
            # Guassian blur
            blur1 = cv2.GaussianBlur(img, (3, 3), 1)
            # mean-shift algo
            newimg = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            img = cv2.pyrMeanShiftFiltering(blur1, 20, 30, newimg, 0, criteria)
            cv2.imshow('means shift image', img)
            # Guassian blur
            blur = cv2.GaussianBlur(img, (11, 11), 1)
            cv2.imshow('Noise Remove', blur)
            corners = cv2.goodFeaturesToTrack(gray, 27, 0.01, 10)
            corners = np.int0(corners)

            # we iterate through each corner,
            # making a circle at each point that we think is a corner.
            for i in corners:
                x, y = i.ravel()
                cv2.circle(image, (x, y), 3, 255, -1)

            plt.imshow(image), plt.show()



            conn = mysql.connector.connect(user='root', password='', host='localhost', database='clouddc')
            cursor = conn.cursor()
            cursor.execute("SELECT * from file where status='" + str(g1) + "'")
            data = cursor.fetchall()
            print(data)




            return render_template('ownerhome.html',data=data,data1=data1)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

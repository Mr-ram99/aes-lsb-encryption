from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageForm, ImageForm2
from PIL import Image
from .models import ImageModel

import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]
    

def home(request):
    return render(request, 'home.html')

def image_upload_view_encrypt(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            text = img_obj.text

            aes=AESCipher("65")
            cipher=aes.encrypt(text)

            img = img_obj.image
            image = Image.open(img, mode='r')
            data = cipher
            if (len(data) == 0):
                raise ValueError('Data is empty')
            newimg = image.copy()

            newimg = encode_enc(newimg, data)

            newimg.save("static/result.png", 'png')

            return render(request, 'result.html', {'enc_img_obj':ImageModel.objects.last()})
    else:
        form = ImageForm()
    return render(request, 'encrypt.html', {'form': form})

def image_upload_view_decrypt(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            img = img_obj.image
            image = Image.open(img, mode='r')

            text = decode(image)
            aes=AESCipher("65")
            text = aes.decrypt(text)
            return render(request, 'result2.html', {'text':text})
    else:
        form = ImageForm2()
    return render(request, 'decrypt.html', {'form': form})


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [ value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3] ]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def genData(data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):

        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    return newimg
def decode(enc_image):
    image= enc_image

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
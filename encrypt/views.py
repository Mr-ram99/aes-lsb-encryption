from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageForm, ImageForm2
from PIL import Image
from .models import ImageModel
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
            img = img_obj.image
            print(text)
            image = Image.open(img, mode='r')
            data = text
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
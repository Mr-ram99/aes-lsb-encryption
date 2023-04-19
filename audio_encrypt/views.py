from django.http import HttpResponse
from django.shortcuts import render
from .forms import AudioForm, AudioForm2
from .models import AudioModel

import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import wave


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
        try:
            encrypted_text = b64decode(encrypted_text)
            iv = encrypted_text[:self.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
            return self.__unpad(plain_text)
        except:
            return "Exception!!!"

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

def audio_upload_view_encrypt(request):
    """Process audio uploaded by users"""
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            aud_obj = form.instance
            text = aud_obj.text
            key = aud_obj.key
            key = str(key)

            aes=AESCipher(key)
            cipher=aes.encrypt(text)

            aud = aud_obj.audio
            data = cipher
            if (len(data) == 0):
                raise ValueError('Data is empty')

            song = wave.open(aud, mode='rb')
            nframes=song.getnframes()
            frames=song.readframes(nframes)
            frame_list=list(frames)
            frame_bytes=bytearray(frame_list)

            data = data + '*^*^*'

            result = []
            for c in data:
                bits = bin(ord(c))[2:].zfill(8)
                result.extend([int(b) for b in bits])

            j = 0
            for i in range(0,len(result),1): 
                res = bin(frame_bytes[j])[2:].zfill(8)
                if res[len(res)-4]== result[i]:
                    frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
                else:
                    frame_bytes[j] = (frame_bytes[j] & 253) | 2
                    frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
                j = j + 1
            
            frame_modified = bytes(frame_bytes)
            with wave.open("static/result_temp.wav", 'wb') as fd:
                fd.setparams(song.getparams())
                fd.writeframes(frame_modified)
            song.close()

            return render(request, 'audio-result.html', {'enc_aud_obj':AudioModel.objects.last()})
    else:
        form = AudioForm()
    return render(request, 'audio-encrypt.html', {'form': form})

def audio_upload_view_decrypt(request):
    """Process audio uploaded by users"""
    if request.method == 'POST':
        form = AudioForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            aud_obj = form.instance
            aud = aud_obj.audio
            key = aud_obj.key
            key = str(key)

            song = wave.open(aud, mode='rb')
            nframes=song.getnframes()
            frames=song.readframes(nframes)
            frame_list=list(frames)
            frame_bytes=bytearray(frame_list)
            text=""
            extracted = ""
            p=0
            for i in range(len(frame_bytes)):
                if(p==1):
                    break
                res = bin(frame_bytes[i])[2:].zfill(8)
                if res[len(res)-2]==0:
                    extracted+=res[len(res)-4]
                else:
                    extracted+=res[len(res)-1]
            
                all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
                decoded_data = ""
                for byte in all_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*":
                        # print("The Encoded data was :--",decoded_data[:-5])
                        text = decoded_data[:-5]
                        p=1
                        break

            aes=AESCipher(key)
            text = aes.decrypt(text)
            if(text == "Exception!!!"):
                return render(request, 'audio-decrypt.html', {'form': form, 'error':True})
            else:
                return render(request, 'audio-result2.html', {'text':text})
    else:
        form = AudioForm2()
    return render(request, 'audio-decrypt.html', {'form': form})


def decode_aud_data(nameoffile):
    song = wave.open(f"fileDir\{nameoffile}", mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    extracted = ""
    p=0
    for i in range(len(frame_bytes)):
        if(p==1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2]==0:
            extracted+=res[len(res)-4]
        else:
            extracted+=res[len(res)-1]
    
        all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                # print("The Encoded data was :--",decoded_data[:-5])
                return decoded_data[:-5]
                p=1
                break  
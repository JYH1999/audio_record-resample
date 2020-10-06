#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  audio_sample.py
#  
#  Copyright 2020 金煜航 <jinyuhang@whut.edu.cn>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import wave
import pyaudio
import numpy
import pylab

def audio_fft(audio_path):
    wf = wave.open(audio_path, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True)
    nframes = wf.getnframes()
    framerate = wf.getframerate()
    str_data = wf.readframes(nframes)
    wf.close()
    wave_data = numpy.frombuffer(str_data, dtype=numpy.short)
    wave_data.shape = -1,2
    wave_data = wave_data.T
    N=44100
    start=0
    df = framerate/(N-1)
    freq = [df*n for n in range(0,N)]
    wave_data2=wave_data[0][start:start+N]
    c=numpy.fft.fft(wave_data2)*2/N
    d=int(len(c)/2)
    while freq[d]>10000:
        d-=10
    pylab.plot(freq[:d-1],abs(c[:d-1]),'r')
    pylab.title(audio_path)
    pylab.savefig(audio_path[:-4]+".png")
    pylab.show()
    

def audio_resample(audio_path,sample_div,name_output):
    CHUNK = 1
    wf = wave.open(audio_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    datas = []
    while len(data) > 0:
        data = wf.readframes(CHUNK)
        datas.append(data)
    datas_2=[]
    t=0
    for i in datas:
        if t%sample_div==0:
            datas_2.append(i)
        t=t+1
    wr = wave.open(name_output, 'wb')
    wr.setnchannels(wf.getnchannels())
    wr.setsampwidth(wf.getsampwidth())
    wr.setframerate(wf.getframerate()/sample_div)
    wr.writeframes(b''.join(datas_2))
    wr.close()

audio_path_in=input("输入目录下的音频文件名，如audio.wav\n")
div_max=int(input("输入最大采样抽取比例\n"))
if div_max<=5:
    print("抽取比例过低，选用默认设置")
    div_max=10

print("作出目标文件重采样频谱")
audio_fft(audio_path_in)
print("对目标文件进行重采样，div=2")
audio_resample(audio_path_in,2,audio_path_in[:-4]+"_div2.wav")
print("目标文件重采样完成，作出频谱")
audio_fft(audio_path_in[:-4]+"_div2.wav")
print("频谱图已保存")
for i in range(5,div_max+1):
    print("对目标文件进行重采样，div="+str(i))
    audio_resample(audio_path_in,i,audio_path_in[:-4]+"_div"+str(i)+".wav")
    print("目标文件重采样完成，作出频谱")
    audio_fft(audio_path_in[:-4]+"_div"+str(i)+".wav")
    print("频谱图已保存")
temp=input("处理完成，按Enter退出")




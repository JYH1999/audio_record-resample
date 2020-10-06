#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  audio_record.py
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
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 40000
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "临界采样.wav"
temp=0
p = pyaudio.PyAudio()
temp=input("音频采样第一次：临界采样(40000Hz)，时长10s，按回车开始！")

stream1 = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


frames1 = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream1.read(CHUNK)
    frames1.append(data)
print("结束！输出文件 临界采样.wav")
stream1.stop_stream()
stream1.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames1))
wf.close()

RATE=2000
WAVE_OUTPUT_FILENAME = "欠采样.wav"
CHUNK=128
q=pyaudio.PyAudio()
temp=input("音频采样第二次：欠采样(2000Hz)，时长10s，按回车开始！")
stream2 = q.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
frames2 = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream2.read(CHUNK)
    frames2.append(data)
stream2.stop_stream()
stream2.close()
q.terminate()
print("结束！输出文件 欠采样.wav")
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(q.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames2))
wf.close()

RATE=96000
WAVE_OUTPUT_FILENAME = "过采样.wav"
CHUNK=1024
r=pyaudio.PyAudio()
temp=input("音频采样第三次：过采样(96000Hz)，时长10s，按回车开始！")

stream3 = r.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
frames3 = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream3.read(CHUNK)
    frames3.append(data)
stream3.stop_stream()
stream3.close()
r.terminate()

print("结束！输出文件 过采样.wav")
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(r.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames3))
wf.close()

print("采样完成，按回车退出程序")
input()
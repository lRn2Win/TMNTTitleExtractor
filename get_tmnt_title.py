#env python

import sys
import argparse
import os

import pytesseract as pt
from PIL import Image, ImageOps

from matplotlib import pyplot as plt
import io
import ffmpeg
from unidecode import unidecode
import re
import Levenshtein as lev

class TitleParser():
    def __init__(self, filename, datafile):
        self.filename = filename
        self.datafile = datafile
        self.ffmpeg_file = ffmpeg.input(filename)
        with open(self.datafile, "r") as f:
            self.lines = f.readlines()
            
        
    def getCloseMatch(self, test_title):
        best_match = ""
        ratio = 0    
        for line in self.lines:
            r = lev.ratio(test_title.lower(), line.lower())
            if r > ratio:
                ratio = r
                best_match = line
        return best_match, ratio
        
    def findTitle(self):
        titles = {}
        for i in list(range(62, 74)) + list(range(31,40)):
            title = self.getTitleAtTime(i)
            if (len(title) > 0):
                if title not in titles:
                    titles[title] = 0
                titles[title] += 1
                
        best_match = ""
        count = 0
        for key in titles:
            b, r = self.getCloseMatch(key)
            if r > count:
                best_match = b
        return best_match.strip("\n")
            
     
    def getFilterImageAtTime(self, time, lowerthresh=210):
        buf = self.getFrameAtTime(time)
        img = self.getImageFromBuff(buf)
        return self.getFilteredImage(img, lowerthresh) 
        
    def getTitleAtTime(self, time):
        buf = self.getFrameAtTime(time)
        img = self.getImageFromBuff(buf)
        for t in range(120, 221, 25):
            iv = self.getFilteredImage(img, t)
            title = self.getTitle(iv)
            if len(title) > 0:
                return title
        return ""
        
    def getFrameAtTime(self, time):
        t = self.ffmpeg_file.trim(start=time)
        try:
            out, error = ( 
                self.ffmpeg_file.trim(start=time)
                    .filter('select', 'gte(n,{})'.format(1))
                    .output("pipe:", vframes=1, format='image2', vcodec='mjpeg')
                    .run(capture_stdout=True, capture_stderr=True))
        except Exception as e:
            print(e)
            raise Exception(e)
        return out
        
    def getImageFromBuff(self, imgbuf):
        return Image.open(io.BytesIO(imgbuf))
    
    def getFilteredImage(self, image, lowerthresh=210):
        return ImageOps.invert(image.convert('L').point(lambda x:255 if x > lowerthresh else 0))
        
    def showImage(self, image):
        plt.imshow(image)
        plt.show()
        
    def getTitle(self, image):
        extracted = pt.image_to_string(image)
        clean_string = unidecode(extracted.replace("\n"," "))
        matches=re.findall(r'"(?:(?:(?!(?<!\\)")[^a-z])*)"',clean_string)
        if len(matches) > 0:
            for match in matches:
                if len(match) > 3:
                    return match
        return ""
        

def main():
    parser = argparse.ArgumentParser(description='Get the title of the episode')
    parser.add_argument('-f', dest='filename',
                    help='video file', required=True)
    parser.add_argument('-d', dest='db',
                    help='datafile', required=True)
    args = parser.parse_args()
    print(TitleParser(args.filename, args.db).findTitle())
       

if __name__ == "__main__":
    main()

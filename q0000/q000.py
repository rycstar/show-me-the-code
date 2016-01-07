#!/usr/bin/python
#Filename:q0000.py

import Image
import ImageFont
import ImageDraw

#create a 100x100 image
#pic = Image.new('RGBA',(100,100),(120,0,120))

#open a exist image
pic = Image.open('./q000_src.jpg','r')
print 'my size :',pic.size
w,h = pic.size

#load font from ImageFont
#font = ImageFont.load_default()
font = ImageFont.truetype('FreeMonoBold.ttf',36)
draw = ImageDraw.Draw(pic)

#draw.line(((20,20),(80,80)),fill=255);
#draw text on the 'top-right corner' image
draw.text((w-24,3),'3',fill=(255,0,255),font=font)

pic.save("./q000_dst.png",'PNG')
print 'Success, the output file is q000_dst.png'

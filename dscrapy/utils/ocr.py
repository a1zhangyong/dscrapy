#coding=utf-8
'''
Created on 2014年3月13日

@author: ulindows
'''
from utn.common import log, util
import Image
import ImageDraw
import ImageFilter
import os
import subprocess
import sys
import time
import urllib




class CaptchaCracker(object):
    '''
                通过ocr破解验证码
    '''


    def __init__(self):
        '''
        CaptchaCracker构造函数
        '''
        self._ocr = 'tesseract'
        
        
    @property
    def ocr(self):
        return self._ocr
    
    @ocr.setter
    def ocr(self, value):
        self._ocr = value
        
    def get_verifycode(self, url):
        '''
        get verifycode from url
        '''
        temp_file = util.get_tempfile('.jpg', 'utn_ocr_')

        try:
            print url
            urllib.urlretrieve(url, temp_file)
            return self.get_verifycode_fromfile(temp_file)
        except:
            err = str(sys.exc_info()[1])
            log.error('从%s获取验证码失败。原因：%s' % (url, err))
            raise Exception(err)
        finally:
            if temp_file and os.path.isfile(temp_file):
                os.remove(temp_file)
                
            
    def get_verifycode_fromfile(self, img_file):
        '''
        get verifycode from image file
        '''
        temp_file = None

        try:
            img = Image.open(img_file)
            img = self.before_recognize(img)

            suffix = img_file.split('.')[-1].lower()
            temp_file = util.get_tempfile('.%s' % suffix, 'utn_ocr_')
            img.save(temp_file)

            text = self._do_recognize(temp_file)
            return self.after_recognize(text)
        except:
            err = str(sys.exc_info()[1])
            log.error('从文件%s获取验证码失败。原因：%s' % (img_file, err))
            raise Exception(err)
        finally:
            if temp_file and os.path.isfile(temp_file):
                os.remove(temp_file)
                

    def _do_recognize(self, img_file, psm = 7):
        '''
        recognize image file by tesseract
        '''
        temp_file = util.get_tempfile('', 'utn_ocr_txt_')
        try:
            
            cmd = '%s -psm %d %s %s' % (self.ocr, psm, img_file, temp_file)
            with open(os.devnull, 'w') as devnull:
                subprocess.call(cmd, stdout=devnull, stderr=devnull)
                      
            temp_file = str('%s.txt' % (temp_file))
            with open(temp_file, 'r') as f:
                return f.readline()
        finally:
            if temp_file and os.path.isfile(temp_file):
                os.remove(temp_file)
            
    def before_recognize(self, img):
        '''
        process image before recognize
        '''
        new_img = img.convert("L")
        new_img = new_img.filter(ImageFilter.MedianFilter())
        return new_img

    def after_recognize(self, text):
        '''
        process ocr result after recognize
        '''
        if text:
            return text.strip()

        return None

    def draw_margin(self, img, point, color):
        '''
        padding imgae margin with color
        '''
        width = img.size[0]
        height = img.size[1]
        x = point[0]
        y = point[1]

        for i in xrange(x):
            for j in xrange(height):
                img.putpixel((i, j), color)

        for i in xrange(x):
            for j in range(height):
                img.putpixel((width - i - 1, j), color)

        for i in range(width):
            for j in range(y):
                img.putpixel((i, j), color)

        for i in range(width):
            for j in range(y):
                img.putpixel((i, height - j - 1), color)
    
    def is_noise(self, image, x, y, background, threshold=10):
        '''
        adjust point is noise or not
        '''
        color = image.getpixel((x, y))
        
        count = 0
        if color != background:
            if image.getpixel((x -1, y - 1)) == background:
                count = count + 1
            if image.getpixel((x - 1, y)) == background:
                count = count + 1
            if image.getpixel((x - 1, y + 1)) == background:
                count = count + 1
            if image.getpixel((x, y - 1)) == background:
                count = count + 1
            if image.getpixel((x, y + 1)) == background:
                count = count + 1
            if image.getpixel((x + 1, y - 1)) == background:
                count = count + 1
            if image.getpixel((x + 1, y)) == background:
                count = count + 1
            if image.getpixel((x + 1, y + 1)) == background:
                count = count + 1

            if count >= threshold:
                return True

        return False

    def clear_noise(self, image, background, noise_threshold, times):
        '''
        clear noise
        '''
        draw = ImageDraw.Draw(image)
        for i in xrange(0, times):
            for x in xrange(1, image.size[0] - 1):
                for y in xrange(1, image.size[1] - 1):
                    if self.is_noise(image, x, y, background, noise_threshold):
                        draw.point((x, y), background)

class SimpleCaptchaCracker(CaptchaCracker):
    '''
    simple ocr
    '''
    def before_recognize(self, img):
        newImg = img.convert("L")
        newImg.show()
        return newImg
    
    def after_recognize(self, text):
        if text:
            result = ''.join(text.split())
            result = result.replace('‘', '')
            result = result.replace("'", '')
            result = result.replace(",", '')
            result = result.replace(";", '')
            result = result.replace(".", '')
            result = result.replace(":", '')
            result = result.replace('"', '')
            
            return result
        
        return None
            
            
class TestCaptchaCracker(CaptchaCracker):
    '''
    cracker for test
    '''
    def before_recognize(self, img):
        '''
        before recognize
        '''
        #new_img = img.point(lambda i: 255 if i > 80 else i)
        new_img = img.convert("L")
        
        
        self.draw_margin(new_img, (2, 2), 255)
        #self.clear_noise(new_img, 255, 6, 20)
            
        #new_img = new_img.filter(ImageFilter.MedianFilter(1))
        new_img = self.handle_img(new_img)        
        self.clear_noise(new_img, (255,255,255,255), 8, 1)
        
        #end = int(new_img.size[0] * 0.4)
        #height = new_img.size[1]         
        #new_img = new_img.crop((0, 0, end, height))
        
        new_img.show()
        return new_img

    '''
    def after_recognize(self, text):
        
        result = text.strip()[:3]
        result = result.replace("'", '-')
        result = result.replace("x", '*')
        result = eval(result)
        return str(result)
    '''
        
    def handle_img(self, img):
        '''
        handle image for test
        '''
        img = img.convert("RGBA")
        pixdata = img.load()

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] > 80:
                    pixdata[x, y] = (255, 255, 255, 255)

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][1] > 80:
                    pixdata[x, y] = (255, 255, 255, 255)

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][2] > 80:
                    pixdata[x, y] = (255, 255, 255, 255)

        return img



if __name__ == '__main__':

    log.init('test.log')

    cracker = TestCaptchaCracker()
    cracker.ock = 'E:\\tools\\文字识别\\jTessBoxEditor\\tesseract-ocr\\tesseract.exe'
    #img_url = 'http://gsxt.gdgs.gov.cn/verify.html?random=0.42792909010273494'
    #code = cracker.get_verifycode(img_url)
    code = cracker.get_verifycode_fromfile('c:\\test.jpg')
    print code

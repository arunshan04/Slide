#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import urllib2
from BeautifulSoup import BeautifulSoup
from os import walk
from os.path import join

import img2pdf

CURRENT = os.path.dirname(__file__)


def download_images(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    file = soup.title.string.replace(' ', '-')
    filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', file) + '.pdf'
    title = 'pdf_images'  # soup.title.string
    shutil.rmtree('pdf_images', ignore_errors=True)

    images = soup.findAll('img', {'class': 'slide_image'})

    for image in images:
        image_url = image.get('data-full').split('?')[0]
        command = 'wget --no-use-server-timestamps %s -P %s' % (image_url, title)
        os.system(command)

    convert_pdf(title, filename)


def convert_pdf(url, filename='Result.pdf'):
    f = []
    for (dirpath, dirnames, filenames) in walk(join(CURRENT, url)):
        f.extend(filenames)
        break

    f = ["%s/%s" % (url, x) for x in f]
    f.sort(key=lambda x: os.path.getmtime(x))
    print f

    pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
    doc = open(filename, 'wb')
    doc.write(pdf_bytes)
    doc.close()


if __name__ == "__main__":
    # url = raw_input('Slideshare URL : ')
    url = 'https://www.slideshare.net/gregchanan/search-onhadoopoc-bigdata'
    download_images(url)

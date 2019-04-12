#!/usr/bin/python
import re
import sys
import os
import shutil

dir_path = "lottie_ads/RCS/json/"
dirs = os.listdir(dir_path)
dirs.remove('.DS_Store')
for dir in dirs:
    files = ["lottie_ads/RCS/json/" + dir + "/" + dir + "_a.json","lottie_ads/RCS/json/" + dir + "/" + dir + "_b.json"]
    file1 = files[0]
    file2 = files[1]
    json = []
    def getJSON(file1, file2):
        data_a = open(file1, 'rw+')
        data_b = open(file2, 'rw+')
        json_a = data_a.read()
        json_b = data_b.read()
        return [json_a, json_b]

    def getDimensions(json):
        a = json[1]
        w_index = a.find("w")
        h_index = a.find("h")
        w = a[w_index+3:w_index+7]
        h = a[h_index+3:h_index+7]
        w = re.sub('[\W\_]','',w)
        h = re.sub('[\W\_]','',h)
        w = int(w)
        h = int(h)
        dimensions = [w, h]
        return dimensions

    json = getJSON(file1, file2)
    dimensions = getDimensions(json)

    def makeHtml(dimensions):
        os.mkdir("lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]))
        filename = "lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/index.html"
        file = open(filename, 'w')
        file.write("<!DOCTYPE html>")
        file.write("<html lang='en'>")
        file.write("<head>")
        file.write("<meta charset='UTF-8'>")
        file.write("<meta name='ad.size' content='width=" + str(dimensions[0]) + ",height=" + str(dimensions[1]) + "'>")
        file.write("<title>RCS " + str(dimensions[0]) + "x" + str(dimensions[1]) + "</title>")
        file.write("<link rel='stylesheet' href='style.css'>")
        file.write("<script type='text/javascript'> var clickTag = ''; </script>")
        file.write("</head>")
        file.write("<body>")
        file.write("<div id='ad'> </div>")
        file.write("<div id='ad2'> </div>")
        file.write("<script src='scripts/lottie.js'></script>")
        file.write("<script src='scripts/index.js'></script>")
        file.write("</body>")
        file.write("</html>")
        file.close()

    makeHtml(dimensions)

    def makeLottie(dimensions):
        os.mkdir("lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/scripts")
        with open("lottie.js") as f:
            with open("lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/scripts/lottie.js", "w") as f1:
                for line in f:
                    f1.write(line)

    makeLottie(dimensions)

    def makeCss(dimensions):
        filename = "lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/style.css"
        file = open(filename, 'w')
        file.write("#ad, #ad2 { display: block; height: " + str(dimensions[1]) + "px; width: " + str(dimensions[0]) + "px; }")
        file.write("#ad2 { opacity: 0; position: absolute; }")
        file.close()

    makeCss(dimensions)

    def makeImages(dimensions):
        os.mkdir("lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/images")

    def copyImages(dimensions):
        source = 'lottie_ads/RCS/images/'
        dest1 = "lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/images/"
        files = os.listdir(source)
        for f in files:
            shutil.copy(source+f, dest1)

    makeImages(dimensions)
    copyImages(dimensions)

    def insertAssets(json, path):
        assets = json.find("[]")
        first = json[:assets+1]
        second = json[assets+1:]
        new_json = first + path + second
        return new_json

    json[0] = insertAssets(json[0], "{'id':'image_0','w':1920,'h':770,'u':'images/','p':'img_2.png','e':0},{'id':'image_1','w':675,'h':450,'u':'images/','p':'img_1.jpg','e':0}")
    json[1] = insertAssets(json[1], "{'id':'image_0','w':1025,'h':899,'u':'images/','p':'img_0.png','e':0}")

    def makeJs(json):
        filename = "lottie_ads/RCS/rcs_" + str(dimensions[0]) + "x" + str(dimensions[1]) + "/scripts/index.js"
        file = open(filename, 'w')
        file.write("var animate = lottie.loadAnimation({container: document.getElementById('ad'),renderer: 'svg',loop: true, autoplay: true,animationData:"
                    + json[0] + "})\n")
        file.write("var animate = lottie.loadAnimation({container: document.getElementById('ad2'),renderer: 'svg',loop: true, autoplay: true,animationData:"
                    + json[1] + "})\n")
        file.write("console.log(animate.animationData)\n")
        file.write("var ad = document.getElementById('ad');\n")
        file.write("var ad2 = document.getElementById('ad2');\n")
        file.write("ad.addEventListener('mouseenter', function( event ) {\n")
        file.write("document.getElementById('ad').style.display = 'none';\n")
        file.write("document.getElementById('ad2').style.display = 'block';\n")
        file.write("document.getElementById('ad2').style.opacity = 1;\n")
        file.write("}, false);\n")
        file.write("ad2.addEventListener('mouseleave', function( event ) {\n")
        file.write("document.getElementById('ad2').style.display = 'none';\n")
        file.write("document.getElementById('ad').style.display = 'block';\n")
        file.write("}, false);")
        file.close()

    makeJs(json)

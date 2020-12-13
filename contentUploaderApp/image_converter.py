from PIL import Image 
import os
import PIL
from django.conf import settings


class ImageConverter():

    def __init__(self): 
        self.savedImagePath = []
        self.resolutions = [360, 480, 720, 1080]

    def createADirByImageName(self, fileName):
        path = settings.MEDIA_ROOT + fileName
        os.mkdir(path)
        return path

    def saveImageInDiffResolutions(self, rgbImage, fileName, baseWidth, fileExtension):
        widthPercent = (baseWidth / float(rgbImage.size[0]))
        hSize = int((float(rgbImage.size[1]) * float(widthPercent)))
        rgbImage = rgbImage.resize((baseWidth, hSize), PIL.Image.ANTIALIAS)
        savedPath = (settings.MEDIA_ROOT + "{fileName}_{fileExtension}_{baseWidth}.{fileExtension}").format(fileName=fileName, baseWidth=baseWidth, fileExtension=fileExtension)
        rgbImage.save(savedPath)
        self.savedImagePath.append(savedPath)

    def convertToMultipleFormats(self, params):
        image = Image.open(params["fileObject"])
        fileExtension = params["fileFormat"]
        rgbImage = image.convert("RGB")

        for resolution in self.resolutions:
            self.saveImageInDiffResolutions(rgbImage, params["fileName"], resolution, "jpeg")
            self.saveImageInDiffResolutions(rgbImage, params["fileName"], resolution, "png")
            self.saveImageInDiffResolutions(rgbImage, params["fileName"], resolution, "webp")
        
        return self.savedImagePath
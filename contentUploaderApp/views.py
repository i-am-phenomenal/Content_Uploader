from django.shortcuts import render
import json
import glob
from django.views import View
from .utils import Utils
from .models import File
from django.http import HttpResponse
from .decorators import Decorators
import os
from django.conf import settings
from .image_converter import ImageConverter
from .queue import ProcessQueue

class FileView(View): 
    decorators = Decorators()
        
    @decorators.validateFileContentTypeForPOST
    @decorators.checkIfFilePresentInRequest
    @decorators.validateIfImageOrVideoOnly  
    @decorators.checkIfFileDoesNotExist
    @decorators.checkIfFileSizeUnderLimit
    def post(self, request):
        """
        [Uploads the given file(s) to the MEDIA diretory]
        Currenty supported formats are
        Image -> "jpg", "png", "gif", "webp", "tiff", "psd", "raw", "bmp", "heif", "indd", "jfif"
        Video ->  "mp4","m4v","svi","mkv","flv","vob","ogv","ogg","mng","avi","m4p","mp3","mpv","mpeg","mpe","3gp"
        Max File size should be 100  MB

         NOTE: Content Type for this request should be multipart/form-data
         The files in the request should be in this format
         type -> multipart/form-data
         Field Name           Value
         FieldName 1          Uploaded File
         File Name  2          Uploaded File 1      
         and so on. 
        Args:
            request ([WSGI Request Object]): [description]

        Returns:
            [Http Response]
        """
        utils = Utils()
        imageConverter = ImageConverter()
        queue = ProcessQueue()

        params = utils.getFileObjectFromRequest(request)
        savedImagePaths = []
        allFilesDict = dict(request.FILES)
        
        
        if len(allFilesDict) > 1:
            for key, value in allFilesDict.items():
                queue.pushVal(value[0])
            utils.processFiles(queue)
            return HttpResponse(
                "Uploaded All Files",
                content_type="application/json"
            )        

        else:
            if params["fileType"] == "Image":
                savedImagePaths = imageConverter.convertToMultipleFormats(params)
            fileObject = utils.convertDictToFileObject(params, savedImagePaths)
            fileObject.save()
            return HttpResponse(
                json.dumps(utils.convertFileObjectToDict(fileObject)),
                content_type="application/json"
            )
        
    @decorators.validateFileContentTypeForDELETE
    @decorators.checkIfValidParams
    def delete(self, request): 
        """ Deletes all files or the specified files

        Args:
            request ([type]): Expects to be of the following format
            {
                operation: Can be either "all" or { "fileName": ... }
            }
            A 400 error code will be thrown if the format is wrong
        """
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        operationVal = params["operation"]
        goodResponse = utils.getGoodResponse("Deleted the file(s) successfully")
        if operationVal == "all": 
            allFiles = File.objects.all()
            allFiles.delete()
            for file in allFiles:
                file.fileObject.delete()
            return goodResponse
        else: 
            try: 
                filteredFile = File.objects.get(fileName=operationVal["fileName"])
                filteredFile.delete()
                return goodResponse
            except File.DoesNotExist:
                return utils.getBadResponse(
                    "The File with the given name does not exist",
                    400
                )

    @decorators.checkIfValidQueryParam
    @decorators.checkIfFileExists
    def get(self, request): 
        """[summary]

        NOTE Expects query param fileName to be in the
        if fileName == "all"  then all the record would be returned else the specified file would be returned

            A 400 response would be returned if the response is not of this format
        Args:
            request (WSGI Request): [description]
        """
        utils = Utils()
        fileName = request.GET.get("fileName")
        if fileName == "all":
            allFiles = [
                utils.convertFileObjectToDict(file)
                for file in File.objects.all()
            ]
            return HttpResponse(
                json.dumps(allFiles),
                content_type="application/json"
            )
        else:
            fileObject = File.objects.get(fileName=fileName)
            return HttpResponse(
                json.dumps(utils.convertFileObjectToDict(fileObject)),
                content_type="application/json"
            )


def deleteAllFileRecords(request): 
    """Made this View function for my own testing purposes
    """
    try:
        allFiles = File.objects.all()
        allFiles.delete()
        for file in allFiles:
            file.fileObject.delete()
        fileList = glob.glob(settings.MEDIA_ROOT)

        return HttpResponse("Done")
    except Exception as e:
        print(e)
        return HttpResponse("There was an error while deleting records")

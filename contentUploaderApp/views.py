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

class FileView(View): 
    decorators = Decorators()
    
    @decorators.validateFileContentTypeForPOST
    @decorators.checkIfFilePresentInRequest
    @decorators.checkIfFileDoesNotExist
    @decorators.checkIfFileSizeUnderLimit
    def post(self, request):
        """[summary]
         
         NOTE: Content Type for this request should be multipart/form-data
        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        utils = Utils()
        params = utils.getFileObjectFromRequest(request)
        fileObject = File(
            fileName = params["fileName"],
            fileType= params["fileType"],
            fileObject = params["fileObject"],
            fileSize = params["fileSize"],
            fileFormat = params["fileFormat"],
            fileResolution = params["fileResolution"]
        )
        fileObject.save()
        return HttpResponse("Ok")
    
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
    try:
        allFiles = File.objects.all()
        allFiles.delete()
        for file in allFiles:
            file.fileObject.delete()
        fileList = glob.glob(settings.MEDIA_ROOT)
        #WIP
        # for file in fileList:
        #     print(file, "AAAAAAAAAAAAAAa")
        #     os.remove(file)

        return HttpResponse("Done")
    except Exception as e:
        print(e)
        return HttpResponse("There was an error while deleting records")

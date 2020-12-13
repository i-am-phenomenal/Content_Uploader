from django.shortcuts import render
from django.views import View
from .utils import Utils
from .models import File
from django.http import HttpResponse
from .decorators import Decorators

class FileView(View): 
    decorators = Decorators()
    
    @decorators.checkIfFilePresentInRequest
    @decorators.checkIfFileSizeUnderLimit
    def post(self, request):
        utils = Utils()
        params = utils.getFileObjectFromRequest(request)
        print(params, "AAAAAAAAAAAAAAAAAAAA")
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
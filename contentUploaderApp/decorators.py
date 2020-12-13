from django.http import HttpResponse
from .utils import Utils
from .models import File

class Decorators(): 

    def checkIfFilePresentInRequest(self, function):
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileParams = request.FILES.get("File")
            response = utils.getBadResponse("File is a mandatory for File Uploader app and it is not present in the request", 400) if fileParams is None else function(referenceToCurrentObject, request)
            return response
        return innerFunction

    def checkIfFileSizeUnderLimit(self, function): 
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileParams = request.FILES.get("File")
            compareFileSize = lambda fileSize: fileSize < 100000000
            response = function(referenceToCurrentObject, request) if compareFileSize(fileParams.size) else utils.getBadResponse("File size exceeds upper limit of 100 mb", 400)
            return response
        return innerFunction

    def checkIfFileDoesNotExist(self, function):
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileParams = request.FILES.get("File")
            getFileCountByFileName = lambda fileName: File.objects.filter(fileName=fileName).count()
            response = function(referenceToCurrentObject, request) if (getFileCountByFileName(fileParams.name) == 0) else utils.getBadResponse("File with the given name already exists", 400)
            return response
        return innerFunction
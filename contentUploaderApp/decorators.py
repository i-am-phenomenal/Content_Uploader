from django.http import HttpResponse
from .utils import Utils

class Decorators(): 

    def checkIfFilePresentInRequest(self, function):
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileParams = request.FILES.get("file")
            response = utils.getBadResponse("File is a mandatory for File Uploader app and it is not present in the", 400) if fileParams is None else function(referenceToCurrentObject, request)
            return response
        return innerFunction

    def checkIfFileSizeUnderLimit(self, function): 
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileParams = request.FILES.get("file")
            compareFileSize = lambda fileSize: fileSize < 100000000
            response = function(referenceToCurrentObject, request) if compareFileSize(fileParams.size) else utils.getBadResponse("File size exceeds upper limit of 100 mb", 400)
            return response
        return innerFunction


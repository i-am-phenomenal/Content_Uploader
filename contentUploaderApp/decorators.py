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

    def checkIfValidParams(self, function): 
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            params = utils.getParamsFromRequest(request)
            successResponse = function(referenceToCurrentObject, request)
            badResponse =  utils.getBadResponse("Invalid Params", 400)
            if "operation" in params: 
                operationVal = params["operation"]
                if type(operationVal) == str and operationVal == "all":
                    return successResponse
                elif type(operationVal) == dict and "fileName" in operationVal:
                    return successResponse
                else: 
                    return badResponse
            else: 
               return badResponse
        return innerFunction

    def validateFileContentTypeForPOST(self, function): 
        def innerFunction(referenceToCurrentObject, request):
            response = function(referenceToCurrentObject, request) if request.content_type == "multipart/form-data" else utils.getBadResponse("Invalid Content Type", 400)
            return response
        return innerFunction

    def validateFileContentTypeForDELETE(self, function):
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            response = function(referenceToCurrentObject, request) if request.content_type == "application/json" else utils.getBadResponse("Invalid Content Type", 400)
            return response
        return innerFunction

    def checkIfValidQueryParam(self, function): 
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils() 
            queryParams = request.GET.get("fileName")
            if queryParams is None: 
                return utils.getBadResponse("Invalid params !", 400)
            else: 
                return function(referenceToCurrentObject, request)
        return innerFunction


    def checkIfFileExists(self, function):
        def innerFunction(referenceToCurrentObject, request):
            utils = Utils()
            fileName = request.GET.get("fileName")
            if fileName != "all":
                fileExists = lambda fileName: File.objects.filter(fileName=fileName).exists()
                response = function(referenceToCurrentObject, request) if fileExists(fileName) else utils.getBadResponse("File with the given name does not exist", 400)
                return response
            else: 
                return function(referenceToCurrentObject, request)
        return innerFunction
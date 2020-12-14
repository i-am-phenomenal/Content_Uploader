import json 
from django.http import HttpResponse
from .models  import File

class Utils():
    def getParamsFromRequest(self, requestObject): 
        params = requestObject.body.decode("utf-8")
        params = json.loads(params)
        return params

    def getFileObjectFromRequest(self, requestObject): 
        fileParams = requestObject.FILES.get("File")
        allFiles = requestObject.FILES.getlist("File")
        resolution = requestObject.POST.get("resolution")
        resolutionVal = resolution if resolution is not None else 0
        fileContentType = fileParams.content_type.split("/")
        fileProperties = {
            "fileName": fileParams.name.split(".")[0].strip(),
            "fileType": fileContentType[0].capitalize(),
            "fileResolution": resolutionVal,
            "fileSize": str(fileParams.size),
            "fileFormat": fileContentType[1],
            "fileObject": fileParams
        }
        return fileProperties

    def getBadResponse(self, message, statusCode=500):
        return HttpResponse(
            json.dumps(
                {
                    "message": message
                }
            ),
            status=statusCode,
            content_type="application/json"
        )

    def getGoodResponse(self, message):
        return HttpResponse(
            json.dumps(
                {
                    "message": message
                }
            ),
            status=200,
            content_type="application/json"
        )

    def convertFileObjectToDict(self, file):
        return {
            "fileName": file.fileName,
            "fileType": file.fileType,
            "fileSize": file.fileSize,
            "fileFormat": file.fileFormat,
            "fileResolution": file.fileResolution,
            "convertedFilePaths": file.convertedFilePaths
        }

    def convertDictToFileObject(self, params, savedImagePaths):
        return File(
            fileName = params["fileName"],
            fileType= params["fileType"],
            fileObject = params["fileObject"],
            fileSize = params["fileSize"],
            fileFormat = params["fileFormat"],
            fileResolution = params["fileResolution"],
            convertedFilePaths = ";;".join(savedImagePaths)
        )
import json 
from django.http import HttpResponse

class Utils():
    def getParamsFromRequest(self, requestObject): 
        params = requestObject.body.decode("utf-8")
        params = json.loads(params)
        return params

    def getFileObjectFromRequest(self, requestObject): 
        fileParams = requestObject.FILES.get("file")
        resolution = requestObject.POST.get("resolution")
        resolutionVal = resolution if resolution is not None else 0
        fileContentType = fileParams.content_type.split("/")
        fileProperties = {
            "fileName": fileParams.name,
            "fileType": fileContentType[0].capitalize(),
            "fileResolution": resolutionVal,
            "fileSize": str(fileParams.size),
            "fileFormat": fileContentType[1],
            "fileObject": fileParams
        }
        return fileProperties

    def getBadResponse(self, message, statusCode=500):
        return HttpResponse(
            json.loads(
                {
                    "message": message
                }
            ),
            status=statusCode
        )
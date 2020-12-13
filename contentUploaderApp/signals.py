from django.core.exceptions import ValidationError

def validate_file_type(sender, instance, **kwargs): 
    fileType = instance.fileType
    fileExtension = instance.fileObject.file.name.split(".")[1].strip().lower()
    if fileType == "Image": 
        if fileExtension not in ["jpg", "png", "gif", "webp", "tiff", "psd", "raw", "bmp", "heif", "indd", "jfif"]:
            raise ValidationError("Invalid File Type for Image {fileExtension}".format(fileExtension=fileExtension))

    elif fileType == "Video": 
        if fileExtension not in [
            "mp4",
            "m4v",
            "svi",
            "mkv",
            "flv",
            "vob",
            "ogv",
            "ogg",
            "mng",
            "avi",
            "m4p",
            "mp3",
            "mpv",
            "mpeg",
            "mpe",
            "3gp"
        ]:
            raise ValidationError("Invalid File Format for video file {fileExtension}".format(fileExtension=fileExtension))
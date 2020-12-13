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


class FileConvertView(View):
    decorators = Decorators()

    # @decorators.validateParamsForFileConvert
    def post(self, request):
        pass
        """[summary]

        NOTE params should be of the following format
            {
                "fileName": ....,
                "format" : ...
            }
        Args:
            request ([type]): [description]
        """
        

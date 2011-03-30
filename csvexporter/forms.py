# coding: utf-8

import re
from copy import copy

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db import IntegrityError
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode


class CSVFilterForm(forms.Form):
    """
    filter the data of a queryset.
    """
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(CSVFilterForm, self).__init__(*args, **kwargs)
        if not self.model:
            raise ImproperlyConfigured('Seems like there is no model defined. check our urlpatterns (add model to kwargs).')
        
        self.csv_filter_definition = settings.CSV_EXPORTER_FILTER_DEFINITION[self.model._meta.module_name]
        
        self.create_fields(filter_def=self.csv_filter_definition)
    
    def create_fields(self, filter_def={}, prefix=""):
        for key in filter_def:
            if type(filter_def[key]) == dict:
                self.create_fields(filter_def=filter_def[key], prefix=prefix + key + "__")
            elif type(filter_def[key]) == list:
                for filter_type in filter_def[key]:
                    self.fields[prefix + key + "__" + filter_type] = forms.CharField(required=False)
            else:
                self.fields[prefix + key + "__" + filter_def[key]] = forms.CharField(required=False)
    
    def clean(self):
        filters = {}
        for item in self.cleaned_data:
            if self.cleaned_data[item]:
                filters[item] = self.cleaned_data[item]
        if len(filters) == 0:
            raise forms.ValidationError("no filters selected!")
        self.filters = filters
        return super(CSVFilterForm, self).clean()
    
    def save(self):
        return self.model.objects.filter(**self.filters)


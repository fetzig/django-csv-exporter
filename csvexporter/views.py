import csv

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

from csvexporter.forms import CSVFilterForm


def prepare_view(request, kwargs):
    if not kwargs.get("model"):
        raise ValueError("You haven't specified the model")
    else:
        kwargs["app_label"] = kwargs["model"]._meta.app_label
        kwargs["model_name"] = kwargs["model"]._meta.module_name
        kwargs["redirect_url"] = reverse(
                "admin:%s_%s_changelist" % (kwargs["app_label"],
                                            kwargs["model_name"])
                )
        kwargs["extra_context"] = {
            "app_label": kwargs["app_label"],
            "model_name": kwargs["model_name"],
            "redirect_url": kwargs["redirect_url"],
        }
    return kwargs


@staff_member_required
def csv_filter(request, **kwargs):
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'csvexporter/csv_filter.html'
    if not kwargs.get("form_class"):
        kwargs["form_class"] = CSVFilterForm
    kwargs = prepare_view(request, kwargs)
    
    if request.method == 'POST':
        form = kwargs["form_class"](request.POST, **{'model': kwargs["model"]})
        if form.is_valid():
            object_list = form.save()
            if "export" in request.POST:
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=export_' + kwargs["model_name"] + '.csv'
                csv_export_dialect = 'excel'
                #csv_follow_relations = []
                csv_export_fmtparam = {
                   'delimiter': ';',
                   'quotechar': '"',
                   'quoting': csv.QUOTE_MINIMAL,
                }
                
                writer = csv.writer(response, csv_export_dialect, **csv_export_fmtparam)
                writer.writerow(settings.CSV_EXPORTER_CSV_FIELDS[kwargs["model_name"]]["field_names"])
                
                for item in object_list:
                    values = settings.CSV_EXPORTER_CSV_FIELDS[kwargs["model_name"]]["field_value_function"](item)
                    csvrow = [f.encode('utf-8') if isinstance(f, unicode) else f for f in values]
                    writer.writerow(csvrow)
                
                return response
        else:
            object_list = None
    else:
        form = kwargs["form_class"](**{'model': kwargs["model"]})
        object_list = None
    
    object_list_result = []
    
    for item in object_list:
        object_list_result.append(settings.CSV_EXPORTER_CSV_FIELDS[kwargs["model_name"]]["field_value_function"](item))
    
    kwargs["extra_context"].update({
        "form": form,
        "object_list": object_list_result,
        "object_list_header": settings.CSV_EXPORTER_CSV_FIELDS[kwargs["model_name"]]["field_names"],
    })
    
    return render_to_response(kwargs["template_name"],
        kwargs["extra_context"],
        context_instance=RequestContext(request)
    )


@staff_member_required
def csv_result_csv(request, object_id, **kwargs):
    if not kwargs.get("template_name"):
        kwargs["template_name"] = 'csvexporter/csv_import.html'
    if not kwargs.get("form_class"):
        kwargs["form_class"] = CSVImportForm
    kwargs = prepare_view(request, kwargs)
    instance = get_object_or_404(CSV, pk=object_id)
    if request.method == 'POST':
        form = kwargs["form_class"](instance, request.POST)
        if form.is_valid():
            form.save(request)
            request.user.message_set.create(message='CSV imported.')
            kwargs["redirect_url"] = reverse('csv_result', args=[instance.id])
            return HttpResponseRedirect(kwargs["redirect_url"])
    else:
        messages.info(request, 'Uploaded CSV. Please associate fields below.')
        form = CSVImportForm(instance)
    kwargs["extra_context"].update({"form": form})
    return object_detail(request,
        queryset=CSV.objects.all(),
        object_id=object_id,
        template_name=kwargs["template_name"],
        template_object_name='csv',
        extra_context=kwargs["extra_context"],
    )

"""
#this is an example:

# CSV EXPORTER
urlpatterns += patterns('csvexporter.views',
    url(r'^csvexporter/filter/$', 'csv_filter', kwargs={"model": User}, name='csvexporter_filter'),
    url(r'^csvexporter/result/(?P<object_id>\d+)/$', 'csv_result', kwargs={"model": User}, name='csvexporter_result'),
    url(r'^csvexporter/result/(?P<object_id>\d+)/csv/$', 'csv_result_csv', kwargs={"model": User}, name='csvexporter_result_csv'),
)
"""

"""
#this is an example:

# CSV EXPORTER
urlpatterns += patterns('csvexporter.views',
    url(r'^csvexporter/user/filter/$', 'csv_filter', kwargs={"model": User}, name='csvexporter_filter'),
)
"""

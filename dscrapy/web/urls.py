from django.conf.urls import url
from django.contrib import admin 
from . import view
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^include.html$', view.include),
    url(r'^$', view.index),
    url(r'^index.html$', view.index),
    url(r'^welcome.html$', view.welcome),
    
    #job
    url(r'^list/jobs.html$', view.list_jobs),
    url(r'^listAll/jobs.html$', view.list_all_jobs),
    url(r'^clone/job.html$', view.clone_job),
    url(r'^del/job.html$', view.cancel_job),
    url(r'^del/jobs.html$', view.cancel_jobs),
    url(r'^toAdd/job.html$', view.to_add_job),
    url(r'^add/jobs.html$', view.add_jobs),
    url(r'^ajax/add/job.html$', view.ajax_add_job),
    url(r'^show/jobs.html$', view.list_jobs_by_servers),
    
    
    #queue
    url(r'^list/queues.html$', view.list_all_queues),
    url(r'^toAdd/queue.html$', view.to_add_queue),
    url(r'^add/queue.html$', view.add_queue),
    url(r'^del/queue.html$', view.del_queue),
    
    #task
    url(r'^toAdd/tasks.html$', view.to_add_tasks), 
    url(r'^add/tasks.html$', view.add_normal_tasks),
    url(r'^submit/tasks.html$', view.ajax_add_tasks),
    
    #target
    url(r'^deploy/targets.html$', view.deploy_targets),
    url(r'^ajax/deploy/targets.html$', view.ajax_deploy_targets),
    url(r'^list/targets.html$', view.list_targets),
    url(r'^toAdd/target.html$', view.to_add_target),
    url(r'^add/target.html$', view.add_target),
    url(r'^del/target.html$', view.del_target),
    url(r'^ajax/find/servers.html$', view.ajax_find_servers),
    
    #log
    url(r'^find/log.html$', view.find_log),
    
    #node
    url(r'^list/nodes.html$', view.list_nodes),
    url(r'^watch/node.html$', view.watch_node),

    #spider
    url(r'^list/spiders.html$', view.list_spiders),
    
    #monitor
    url(r'^line.html$', view.to_load_line_chart),
    url(r'^ajax/load/line.html$', view.ajax_load_line_chart),
    url(r'^ajax/load/table.html$', view.ajax_load_table),
    url(r'^ajax/load/cpu.html$', view.ajax_load_cpu_line),
    url(r'^ajax/load/node.html$', view.ajax_load_node),
    url(r'^ajax/load/jobs.html$', view.ajax_load_jobs_info),
    url(r'^ajax/get/server.html$', view.ajax_random_get_server),
    
]






















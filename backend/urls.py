from django.contrib import admin

# add include to the path
from django.urls import path, include

# import views from todo
from College import views

# import routers from the REST framework
# it is necessary for routing
from rest_framework import routers
# create a router object
router = routers.DefaultRouter()
# register the router
router.register(r'login',views.LoginView, 'task1')
router.register(r'GuestLogin',views.GuestLoginView, 'task2')
router.register(r'Queryform',views.QueryFormView, 'task3')
router.register(r'AdminLogin',views.AdminLoginView, 'task4')

admin.site.site_header='Grievance Report'
admin.site.site_title=''
admin.site.index_title='Grievance Report Administration'

urlpatterns = [
	path('admin/', admin.site.urls),

	# add another path to the url patterns
	# when you visit the localhost:8000/api
	# you should be routed to the django Rest framework
	path('api/', include(router.urls)),
    path('get_data/',views.get_data,name='get_data'),
    path('update_status/', views.update_status, name='update_status'),
    path('check/', views.check, name='check'),
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('email/',views.sendEmail,name='email')
]

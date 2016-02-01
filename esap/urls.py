from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('',
                       # Keywords
                       url(r'tags/$',  # Listagem/Add
                           KeywordCreateView.as_view(),
                           name='keywords'
                           ),
                       url(r'tags/edit/(?P<pk>\d+)/$',  # Atualizar
                           KeywordUpdateView.as_view(),
                           name='keyword_update'
                           ),
                       url(r'tags/(?P<slug>[A-Za-z0-9_-]+)/$',  # View
                           KeywordDetailView.as_view(),
                           name='keyword_detail'
                           ),


                       # Classes
                       url(r'aulas/add_form/$',  # Formulario (ajax modal)
                           ClassesCreateAjaxFormView.as_view(),
                           name='classes_ajax_form'
                           ),
                       url(r'aulas/add/$',  # Adicionar
                           ClassesCreateView.as_view(),
                           name='classes_add'
                           ),
                       url(r'aulas/edit_form/(?P<pk>\d+)/$',  # Editar (ajax)
                           ClassesAjaxUpdateView.as_view(),
                           name='classes_ajax_update'
                           ),
                       url(r'aulas/edit/(?P<pk>\d+)/$',  # Editar
                           ClassesUpdateView.as_view(),
                           name='classes_update'
                           ),
                       url(r'aulas/(?P<pk>\d+)/$',  # Visualizar aula
                           ClassesDetailView.as_view(),
                           name='classes_detail'
                           ),
                       url(r'aulas/ajax/(?P<pk>\d+)/$',  # Listagem ajax
                           ClassesAjaxDetailView.as_view(),
                           name='classes_ajax_detail'
                           ),
                       url(r'aulas/$',  # Listagem
                           ClassesListView.as_view(),
                           name='classes'
                           ),

                       # Modulos
                       url(r'modulos/$',  # Listagem
                           ModuleListView.as_view(),
                           name='modules'
                           ),
                       url(r'modulos/ajax/(?P<pk>\d+)/$',  # Listagem ajax
                           ModuleAjaxDetailView.as_view(),
                           name='modules_ajax_detail'
                           ),
                       url(r'modulos/add_form/$',  # Formulario (ajax modal)
                           ModuleCreateAjaxFormView.as_view(),
                           name='modules_ajax_form'
                           ),
                       url(r'modulos/add/$',  # Adicionar
                           ModuleCreateView.as_view(),
                           name='modules_add'
                           ),
                       url(r'modulos/edit_form/(?P<pk>\d+)/$',  # Editar (ajax)
                           ModuleAjaxUpdateView.as_view(),
                           name='module_ajax_update'
                           ),
                       url(r'modulos/edit/(?P<pk>\d+)/$',  # Editar
                           ModuleUpdateView.as_view(),
                           name='module_update'
                           ),
                       url(r'modulos/(?P<pk>\d+)/$',  # View
                           ModuleDetailView.as_view(),
                           name='module_detail'
                           ),

                       # Instrutores
                       url(r'instrutores/$',  # List
                           InstructorListView.as_view(),
                           name='instructors'
                           ),
                       url(r'instrutores/add/$',  # Add
                           InstructorCreateView.as_view(),
                           name='instructor_add'
                           ),
                       url(r'instrutores/edit/(?P<pk>\d+)/$',  # Atualizar
                           InstructorUpdateView.as_view(),
                           name='instructor_update'
                           ),
                       url(r'instrutores/(?P<pk>\d+)/$',  # View
                           InstructorDetailView.as_view(),
                           name='instructor_detail'
                           ),

                       # Particular clients
                       url(r'clientes-particulares/$',  # List
                           ParticularClientListView.as_view(),
                           name='particularclients'
                           ),
                       url(r'clientes-particulares/add/$',  # Add
                           ParticularClientCreateView.as_view(),
                           name='particularclient_add'
                           ),
                       url(r'clientes-particulares/edit/(?P<pk>\d+)/$',  # Atualizar
                           ParticularClientUpdateView.as_view(),
                           name='particularclient_update'
                           ),
                       url(r'clientes-particulares/(?P<pk>\d+)/$',  # View
                           ParticularClientDetailView.as_view(),
                           name='particularclient_detail'
                           ),
                       url(r'clientes-particulares/fullname/(?P<pk>\d+)/$',
                           ParticularClientFullNameJsonView.as_view(),
                           name='particularclient_fullname_json'
                           ),

                       # Home
                       url(r'^$', DashboardView.as_view(), name='home'),
                       )

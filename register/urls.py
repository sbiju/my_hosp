from django.conf.urls import url

from .views import (
    DoctorCreatelView,
    DoctorListView,
    DoctorDetailView,
    DoctorUpdatelView,
    DoctorDeleteView,
    HomePageView,
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdatelView,
    PatientDeleteView,
    PaymentCreatelView,
    PaymentListView,
    PaymentDetailView,
    PatientDischargeDetail,
    # DischargeView,
    PatientDischargeList,
    PatientDischargeApprovedList,
    total_patients,
    payment_retrieve,
    PatientApproveView,
    PatientDischargeView,
    )


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^discharge/$', PatientDischargeList.as_view(), name='discharge_list'),
    url(r'^discharge/approved/$', PatientDischargeApprovedList.as_view(), name='discharge_approved_list'),
    url(r'^discharge/(?P<pk>\d+)/$', PatientDischargeDetail.as_view(), name='discharge_detail'),
    # url(r'^discharge/(?P<pk>\d+)/delete/$', DischargeView.as_view(), name='discharge'),
    url(r'^discharge/(?P<pk>\d+)/approve/$', PatientApproveView.as_view(), name='discharge_approve'),
    url(r'^discharge/(?P<pk>\d+)/complete/$', PatientDischargeView.as_view(), name='discharge_complete'),


    url(r'^doctor/$', DoctorListView.as_view(), name='doctor_list'),
    url(r'^doctor/add/$', DoctorCreatelView.as_view(), name='doctor_create'),
    url(r'^doctor/(?P<pk>\d+)/$', DoctorDetailView.as_view(), name='doctor_detail'),
    url(r'^doctor/(?P<pk>\d+)/edit/$', DoctorUpdatelView.as_view(), name='doctor_update'),
    url(r'^doctor/(?P<pk>\d+)/delete/$', DoctorDeleteView.as_view(), name='doctor_delete'),

    url(r'^patient/add/$', PatientCreateView.as_view(), name='patient_create'),
    url(r'^patient/$', PatientListView.as_view(), name='patient_list'),
    url(r'^patient/(?P<pk>\d+)/$', PatientDetailView.as_view(), name='patient_detail'),
    url(r'^patient/(?P<pk>\d+)/edit/$', PatientUpdatelView.as_view(), name='patient_update'),
    url(r'^patient/(?P<pk>\d+)/delete/$', PatientDeleteView.as_view(), name='patient_delete'),

    url(r'^payment/$', PaymentListView.as_view(), name='payment_list'),
    url(r'^payment/add/$', PaymentCreatelView.as_view(), name='payment_create'),
    url(r'^payment/(?P<pk>\d+)/$', PaymentDetailView.as_view(), name='payment_detail'),
    url(r'^total/$', total_patients, name='total_patients'),
    url(r'^bills/$', payment_retrieve, name='bill_view'),

]

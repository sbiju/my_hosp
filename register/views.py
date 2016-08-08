from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal

from .models import Doctor, Patient, Department, Payment
from .mixins import LoginRequiredMixin, StaffRequiredMixin, DoctorRequiredMixin
from .forms import PatientAdmissionForm, PaymentForm
from .pagination import PaymentPagination, PatientPagination
from .serializers import PatientSerializer, PaymenttSerializer


class PatientListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = PatientPagination


class PatientRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymenttSerializer
    pagination_class = PaymentPagination


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    queryset = Payment.objects.all()
    serializer_class = PaymenttSerializer


class HomePageView(TemplateView):
    template_name = "home.html"


class DoctorListView(StaffRequiredMixin, ListView):
    model = Doctor


class DoctorDetailView(StaffRequiredMixin, DetailView):
    model = Doctor
    queryset = Doctor.objects.all()


class DoctorCreatelView(StaffRequiredMixin,CreateView):
    model = Doctor
    fields = ['salutation', 'name', 'speciality', 'house_number', 'street', 'city', 'state', 'pin', ]


class DoctorUpdatelView(StaffRequiredMixin, UpdateView):
    model = Doctor
    fields = ['salutation', 'name', 'speciality', 'house_number', 'street', 'city', 'state', 'pin', ]


class DoctorDeleteView(StaffRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('hospital:doctor_list')


class PatientListView(LoginRequiredMixin,ListView):
    model = Patient
    queryset = Patient.objects.filter(is_discharged=False)

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        return context


class PatientDetailView(StaffRequiredMixin, DetailView):
    model = Patient


class PatientCreateView(StaffRequiredMixin, CreateView):
    model = Patient
    fields = ['salutation', 'name', 'doctor', 'department', 'house_number', 'street', 'city', 'state', 'pin',
                  'time_admitted',]
    template_name = 'register/patient_form.html'


class PatientUpdatelView(DoctorRequiredMixin, UpdateView):
    model = Patient
    queryset = Patient.objects.filter(is_discharged=False)
    fields = ['salutation', 'name', 'doctor', 'department', 'house_number', 'street', 'city', 'state', 'pin',
                  'time_admitted', 'is_approved_discharge','is_discharged']

    def get_context_data(self, **kwargs):
        context = super(PatientUpdatelView, self).get_context_data(**kwargs)
        context['id_updated'] = self.kwargs.get('pk')
        return context


class PatientApproveView(DoctorRequiredMixin, UpdateView):
    model = Patient
    queryset = Patient.objects.filter(is_discharged=False).filter(is_approved_discharge=False)
    fields = ['salutation', 'name', 'doctor', 'department', 'time_admitted', 'is_approved_discharge']


class PatientDischargeView(DoctorRequiredMixin, UpdateView):
    queryset = Patient.objects.filter(is_approved_discharge=True)
    model = Patient
    fields = ['salutation', 'name', 'doctor', 'department', 'time_admitted', 'time_discharged', 'is_discharged']


class PatientDeleteView(StaffRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('hospital:patient_list')


class PatientDischargeApprovedList(DoctorRequiredMixin, ListView):
    model = Patient
    queryset = Patient.objects.filter(is_discharged=False).filter(is_approved_discharge=True)


class PatientDischargeList(StaffRequiredMixin, ListView):
    model = Patient
    queryset = Patient.objects.filter(is_discharged=True)


class PatientDischargeDetail(StaffRequiredMixin, DetailView):
    model = Patient
    template_name = 'register/patient_detail.html'


class PaymentCreatelView(StaffRequiredMixin,CreateView):
    model = Payment
    form_class = PaymentForm

    def get_success_url(self):
        return reverse('hospital:payment_list')


class PaymentListView(LoginRequiredMixin,ListView):
    model = Payment


def payment_retrieve(request):
    queryset_list = Payment.objects.all().order_by("-time_billed")
    if request.user.is_authenticated:
        queryset_list = Payment.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(patient__name__icontains=query)|
                Q(id__icontains=query)|
                Q(time_discharged__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 6)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
    "object_list": queryset,
    "page_request_var": page_request_var,

    }
    return render(request, "register/payment_list.html", context)


class PaymentDetailView(StaffRequiredMixin, DetailView):
    model = Payment
    queryset = Payment.objects.all()


class DischargeView(StaffRequiredMixin, DeleteView):
    model = Patient
    template_name = 'register/discharge_confirm.html'
    success_url = reverse_lazy('hospital:payment_list')


def total_patients(request):
    current_patients = Patient.objects.filter(is_discharged=False).count
    discharge_approved_patient = Patient.objects.filter(is_approved_discharge=True).count
    discharged_patient = Patient.objects.filter(is_discharged=True).count

    context = {
        'curr_patient': current_patients,
        'dis_patient': discharged_patient,
        # 'total_beds_available': total_beds_available,
    }
    return render(request, "register/total_patient.html", context)



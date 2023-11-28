from django.shortcuts import render
from django.views import generic
from .forms import UniversityRegisterationForm, AddressRegisterationForm, FacultyRegisterationForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render





class UniversityPage(generic.CreateView):
    template_name = "university.html"
    form_class =  UniversityRegisterationForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super(UniversityPage, self).get_context_data(**kwargs)
        context['address_form'] = AddressRegisterationForm() 
        return context

    def post(self, request, *args, **kwagrs):
        address =  AddressRegisterationForm(data = request.POST) 
        university =  UniversityRegisterationForm(data = request.POST) 
        if address.is_valid():
            if university.is_valid():
                addr_obj = address.save()
                uni_obj = university.save(commit=False)
                uni_obj.address = addr_obj
                uni_obj.save()
                return redirect(reverse_lazy("home"))
            print("uuu", university.errors)
        print("aaaa",address.errors)
        return redirect(reverse_lazy("login"))


class FacultyPage(generic.CreateView):
    template_name = "Faculty_register.html"
    form_class =  FacultyRegisterationForm
    success_url = reverse_lazy("home")
    def get_context_data(self, **kwargs):
        context = super(UniversityPage, self).get_context_data(**kwargs)
        context['address_form'] = AddressRegisterationForm() 
        return context

    def post(self, request, *args, **kwagrs):
        address =  AddressRegisterationForm(data = request.POST) 
        faculty =  FacultyRegisterationForm(data = request.POST) 
        if address.is_valid():
            if faculty.is_valid():
                addr_obj = address.save()
                fac_obj = fac.save(commit=False)
                fac_obj.address = addr_obj
                fac_obj.save()
                return redirect(reverse_lazy("home"))
            print("uuu", faculty.errors)
        print("aaaa",address.errors)
        return redirect(reverse_lazy("login"))
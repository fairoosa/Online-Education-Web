import cv2 as cv2
import img2pdf
from PIL import Image
import os
from django.shortcuts import render
from django.views import generic

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterationForm, AddressRegisterationForm, UserLoginForm
from Course.models import Course, CourseContent,  Quiz, Enrollment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class LoginPage(generic.TemplateView):
    template_name = "login.html"
    form_class = UserLoginForm

    def post(self, request, *args, **kwagrs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        try:
            user_obj = User.objects.get(username=username)
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("home")) 
            else:
                # print("incorrect username and password")
                messages.error(self.request, "Incorrect username or password")
                return redirect(reverse_lazy("login"))
        except ObjectDoesNotExist:
            try:
                user_obj = User.objects.get(email=username)
                user=authenticate(username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse_lazy("home")) 
                else:
                    print("incorrect username and password")
                    messages.error(self.request, "Incorrect username or password")
                    return redirect(reverse_lazy("login"))
            except:
                print("incorrect username and password")
                return redirect(reverse_lazy("login"))


class RegisterPage(generic.CreateView):
    template_name = "register.html"
    form_class = UserRegisterationForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        user_obj = User.objects.get(username=self.request.POST.get('username'))
        login(self.request, user_obj)
        return super(RegisterPage, self).get_success_url()


class AddressPage(generic.CreateView):
    template_name="address.html"
    form_class =  AddressRegisterationForm
    success_url = '/login'


class HomePage(generic.ListView):
    template_name = "home.html"
    model = Course


class HomePage1(generic.ListView):
    template_name = "home1.html"
    model = Course


class LogoutPage(generic.View):

    def get(self, request, *args, **kwagrs):
        logout(request) 
        return redirect(reverse_lazy("login"))


class CourseDetails(generic.DetailView):
    template_name = "coursedetail.html"
    model = Course

    def get_context_data(self, **kwargs):
        course = Course.objects.get(id=self.kwargs['pk'])
        context_data = super().get_context_data(**kwargs)
        context_data['already_enrolled'] = False

        if self.request.user.is_authenticated:
            enroll_obj = Enrollment.objects.filter(course=course, user=self.request.user)
            if enroll_obj:
                context_data['already_enrolled'] = True
        return context_data


class CoursecontentPage(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = "coursecontent.html"
    model=CourseContent

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(course__id=self.kwargs['pk'])
        week_nos = self.model.objects.filter(course__id=self.kwargs['pk']).values_list('week_no', flat=True).distinct ()
        print(week_nos)
        final_list = []

        for i in week_nos:
            final_list.append([])
        temp = []
        for i in queryset:
            print(i.week_no)
            final_list[i.week_no - 1].append(i) 
        # print(final_list)
        return final_list

        # if i.week_no != num:
        #         num = i.week_no
        #         final_list.append(temp)
        #         temp = []
        #         temp.append(i)
        #     else:
        #         temp.append(i)
    
    def get_context_data(self, **kwargs):
        course = Course.objects.get(id=self.kwargs['pk'])
        enroll_obj = Enrollment.objects.filter(course=course, user=self.request.user)
        context_data = super().get_context_data(**kwargs)
        if enroll_obj.count() > 0 and enroll_obj[0].is_completed:
            context_data['is_completed'] = True
        else:
            context_data['is_completed'] = False
        return context_data

class QuizPage(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = "quiz.html"
    model=Quiz

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(course__id=self.kwargs['pk'])
        return queryset


@method_decorator(csrf_exempt, name='dispatch')
class QuizAssesment(generic.View):

    def post(self, *args, **kwargs):
        import json
        return_dict = {"code": 0, "status": "failed", "response": self.request.POST}
        for i in self.request.POST.items():
            if i[0] == "course_id":
                course_id = i[1]
            else:
                pass
            
        course = Course.objects.get(id=course_id)
        no_of_questions = Quiz.objects.filter(course=course).count()
        mark = 0 
        for i in self.request.POST.items():
            if i[0] == "course_id":
                course_id = i[1]
            else:
                try:
                    ques_obj = Quiz.objects.get(id=i[0])
                    print("Correct answer:", ques_obj.answer)
                    print("User answer:", i[0])
                    if ques_obj.answer.strip() == i[1].strip():
                        print("Anwer correct: ")
                        mark  += 1
                    print("mark: ", mark)
                except:
                    print("incorrect",ques_obj.answer)
        percentage = (mark/no_of_questions) * 100
        print(percentage,no_of_questions)
        if percentage >= 60:
            enroll_obj = Enrollment.objects.get(course=course, user=self.request.user)
            enroll_obj.is_completed = True
            enroll_obj.save()
            return_dict = {"status": "passed", "response": {"percentage": percentage}, 
                        "msg": "You have successfully passed the exam. Go to your profile and check your certificate."}
        else:
            enroll_obj = Enrollment.objects.get(course=course, user=self.request.user)
            return_dict = {"status": "failed", "response": {"percentage": percentage},
                "msg": "Your mark is very low.Please retake."}
        return JsonResponse(return_dict)


class EnrollView(LoginRequiredMixin, generic.View, SuccessMessageMixin):
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        course_id = self.kwargs['pk']
        course = Course.objects.get(id=course_id)
        user = self.request.user
        Enrollment.objects.create(user=user, course=course)
        messages.success(self.request, "You have successfully enrolled. Watch the lectures now.")
        return redirect(reverse_lazy('content', kwargs={'pk': self.kwargs['pk']}))


class CertificateGeneration(LoginRequiredMixin, generic.TemplateView):
    template_name = "certificate.html"

    def get(self, *args, **kwargs):
        from . cert import create_cert
        course = Course.objects.get(id=self.kwargs['pk'])
        enr_obj = Enrollment.objects.get(user=self.request.user, course=course)
        name = f"{self.request.user.first_name} {self.request.user.last_name}"
        cs = f"{course}" 
        if not enr_obj.certificate_generated:
            print('creating certificate starts here')
            # template1.png is the template
            # certificate
            create_cert(f"{name}", r"C:\Users\fairo\OneDrive\Documents\work\Mini-Project-main\edtech\media\certificates\{0}_{1}.png".format(self.request.user.id, self.kwargs['pk']))
            # create_cert(cs, r"C:\Users\fairo\mini\Mini-Project-main\Mini-Project-main\Mini-Project-main\edtech\media\certificates\{0}_{1}.png".format(self.request.user.id, self.kwargs['pk']))
            # Output Paths
            # certificate_template_image = cv2.imread("certificate-template.jpg")
            # cv2.putText(certificate_template_image, name.strip(), (815,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 250), 5, cv2.LINE_AA)
            


            # storing image path
            img_path = r"C:\Users\fairo\OneDrive\Documents\work\Mini-Project-main\edtech\media\certificates\{0}_{1}.png".format(self.request.user.id, self.kwargs['pk'])
            # img_path = r"C:\Users\fairo\mini\Mini-Project-main\Mini-Project-main\Mini-Project-main\edtech\media\certificates\{0}_{1}.png".format(self.request.user.id, self.kwargs['pk'])
            
            # storing pdf path
            pdf_path = r"C:\Users\fairo\OneDrive\Documents\work\Mini-Project-main\edtech\media\certificates\{0}_{1}.pdf".format(self.request.user.id, self.kwargs['pk'])
            # pdf_path = r"C:\Users\fairo\mini\Mini-Project-main\Mini-Project-main\Mini-Project-main\edtech\media\certificates\{0}_{1}.pdf".format(self.request.user.id, self.kwargs['pk'])
            
            # opening image
            image = Image.open(img_path)
            
            # converting into chunks using img2pdf
            pdf_bytes = img2pdf.convert(image.filename)
            
            # opening or creating pdf file
            file = open(pdf_path, "wb")
            
            # writing pdf files with chunks
            file.write(pdf_bytes)
            
            # closing image file
            image.close()
            
            # closing pdf file
            file.close()

            enr_obj.certificate_generated = True
            enr_obj.certificate_path = "{0}_{1}.pdf".format(self.request.user.id, self.kwargs['pk'])
            enr_obj.save()
        return super(CertificateGeneration, self).get(self, **kwargs)

    def get_context_data(self, **kwargs):
        course = Course.objects.get(id=self.kwargs['pk'])
        enr_obj = Enrollment.objects.get(user=self.request.user, course=course)
        context_data = super().get_context_data(**kwargs)
        context_data['certificate'] = enr_obj.certificate_path
        return context_data


class LogoutView(generic.View):

    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse_lazy('login'))


class Profile(generic.ListView):
    model = Enrollment
    template_name = "profile.html"

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(user__id=self.kwargs['pk'])
        return queryset

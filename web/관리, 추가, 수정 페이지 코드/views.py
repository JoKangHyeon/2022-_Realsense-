from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from .models import studentInfoDB,attendanceInfoDB

# Create your views here.
#django 설정이 잘 되었나 확인할 때 사용한 함수
def index(request):
    return HttpResponse('Hello World')

#학생 정보 관리 페이지에 접속할 때 동작하는 함수
def infoManager(request):
    studentInfo = studentInfoDB.objects.all().order_by('stu_no')
    context={'studentInfo' : studentInfo}
    return render(request, 'myApp/infoManager.html',context)

#학생 추가 페이지에 접속할 때 동작하는 함수
def addStudent(request):
    context={}
    return render(request, 'myApp/addStudent.html',context=context)

#학생 추가 페이지에서 추가 버튼을 클릭하면 db에 저장되게 하도록 하는 함수
@csrf_exempt #crsf token 체크 해제(해제하지 않으면 오류 발생)
def add(request):
    #POST 방식으로 전달받은 데이터 값을 변수에 저장
    dept=request.POST['stu_dept']
    no=request.POST['stu_id']
    name=request.POST['stu_name']
    image=request.POST['stu_pic']

    #저장된 데이터 값을 DB에 삽입
    studentInfo = studentInfoDB(dept=dept, stu_no=no, stu_name=name, stu_image=image)

    #삽입된 데이터를 DB에 저장
    studentInfo.save()
    
    #redirect를 사용하여 바로 학생 정보 관리 페이지로 이동
    return HttpResponseRedirect('/infoManager')

#밑에 두 함수는 시간이 부족하여 구현하지 못한 함수들
def stuAttendInfo(request):
    attendanceInfo = attendanceInfoDB.objects.all()
    return render(request,'myApp/stuAttendInfo.html',{'attendanceInfo' : attendanceInfo})

def modify(request, stu_id):
    pass
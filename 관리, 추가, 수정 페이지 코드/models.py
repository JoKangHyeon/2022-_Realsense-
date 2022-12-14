from django.db import models

# Create your models here.

#학생 정보 DB
class studentInfoDB(models.Model):
    dept=models.CharField(max_length=50)
    stu_no=models.CharField(max_length=50, primary_key=True, null=False)
    stu_name=models.CharField(max_length=50)
    stu_image=models.ImageField()

    class Meta :
        managed=False
        db_table='tbl_studentInfo'

#출석 정보 DB
class attendanceInfoDB(models.Model):
    dept=models.CharField(max_length=50)
    stu_no=models.CharField(max_length=50, primary_key=True)
    stu_name=models.CharField(max_length=50)
    att_date=models.DateField()
    att_check=models.CharField(max_length=50)

    class Meta :
        managed=False
        db_table='tbl_attendanceInfo'
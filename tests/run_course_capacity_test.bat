@echo off
REM 运行课程容量测试脚本
cd /d "d:\Study\Project\py_project\python_web_student_system"
call .venv\Scripts\activate
python manage.py shell -c "exec(open('tests\\test_course_capacity.py').read())"
call .venv\Scripts\deactivate
pause
import os
import django
from django.db import connection

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')
django.setup()

# 检查course_course表的字段
def check_course_table_fields():
    with connection.cursor() as cursor:
        # 查询表结构
        cursor.execute("""SHOW COLUMNS FROM course_course;""")
        columns = cursor.fetchall()
        
        print("Course表结构:")
        print("字段名		类型		是否允许为空		键类型		默认值		额外信息")
        print("-" * 100)
        for column in columns:
            field_name, data_type, nullable, key_type, default_value, extra = column
            print(f"{field_name}		{data_type}		{nullable}		{key_type}		{default_value}		{extra}")
    
    # 尝试查询数据，看看是否可以访问total_hours字段
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT id, name, total_hours FROM course_course LIMIT 1;""")
            result = cursor.fetchone()
            if result:
                print(f"\n成功查询到total_hours字段，示例数据: {result}")
            else:
                print("\n表中没有数据，但查询语句执行成功")
    except Exception as e:
        print(f"\n查询total_hours字段失败: {e}")

if __name__ == "__main__":
    check_course_table_fields()
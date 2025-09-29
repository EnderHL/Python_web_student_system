import json
import requests

# 测试基础URL
base_url = 'http://localhost:8000/api/courses/'
teachers_url = 'http://localhost:8000/api/teachers/'
classrooms_url = 'http://localhost:8000/api/classrooms/'

# 测试GET方法 - 获取所有课程
def test_get_all_courses():
    print("\n===== 测试GET - 获取所有课程 =====")
    response = requests.get(base_url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"返回数据数量: {len(data) if isinstance(data, list) else '非列表格式'}")
        print(f"响应内容预览: {json.dumps(data[:3], indent=2) if isinstance(data, list) and data else '无数据'}")
        return data
    else:
        print(f"请求失败: {response.text}")
    return []

# 测试GET方法 - 获取所有教师
def test_get_all_teachers():
    print("\n===== 测试GET - 获取所有教师 =====")
    response = requests.get(teachers_url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"返回数据数量: {len(data) if isinstance(data, list) else '非列表格式'}")
        print(f"响应内容预览: {json.dumps(data[:3], indent=2) if isinstance(data, list) and data else '无数据'}")
        return data
    else:
        print(f"请求失败: {response.text}")
    return []

# 测试GET方法 - 获取所有教室
def test_get_all_classrooms():
    print("\n===== 测试GET - 获取所有教室 =====")
    response = requests.get(classrooms_url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"返回数据数量: {len(data) if isinstance(data, list) else '非列表格式'}")
        print(f"响应内容预览: {json.dumps(data[:3], indent=2) if isinstance(data, list) and data else '无数据'}")
        return data
    else:
        print(f"请求失败: {response.text}")
    return []

# 测试特定课程详情
def test_get_course_detail(course_id):
    if not course_id:
        print("\n无法测试GET课程详情 - 没有有效的课程ID")
        return
    print(f"\n===== 测试GET - 获取课程 {course_id} 详情 =====")
    response = requests.get(f"{base_url}{course_id}/")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容: {json.dumps(data, indent=2)}")
    else:
        print(f"请求失败: {response.text}")

# 运行所有测试
if __name__ == "__main__":
    print("开始测试课程管理API...")
    
    # 测试获取所有课程
    courses = test_get_all_courses()
    
    # 测试获取所有教师
    teachers = test_get_all_teachers()
    
    # 测试获取所有教室
    classrooms = test_get_all_classrooms()
    
    # 测试获取第一个课程的详情（如果有课程）
    if courses and isinstance(courses, list) and courses:
        first_course_id = courses[0].get('id')
        test_get_course_detail(first_course_id)
    
    # 总结测试结果
    print("\n===== 测试总结 =====")
    print(f"课程API状态: {'成功' if isinstance(courses, list) else '失败'}")
    print(f"教师API状态: {'成功' if isinstance(teachers, list) else '失败'}")
    print(f"教室API状态: {'成功' if isinstance(classrooms, list) else '失败'}")
    
    if isinstance(courses, list):
        if len(courses) == 0:
            print("警告: 课程API返回成功，但没有数据，请检查数据库中是否有课程记录。")
        else:
            print(f"成功获取到 {len(courses)} 门课程数据。")
    
    # 诊断建议
    if not isinstance(courses, list) or len(courses) == 0:
        print("\n可能的问题原因：")
        print("1. 后端API可能没有正确配置")
        print("2. 数据库中可能没有课程数据")
        print("3. 后端服务器可能未运行或运行在不同端口")
        print("4. 可能存在权限问题")
    else:
        print("\n后端API工作正常，如果前端仍然无法显示数据，问题可能在前端代码。")
        print("建议检查前端Course.js中的API调用逻辑和数据处理部分。")
    
    print("\n测试完成。")
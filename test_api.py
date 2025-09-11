import requests
import json

# 测试基础URL
base_url = 'http://localhost:8000/api/students/'

# 测试GET方法 - 获取所有学生
def test_get_all_students():
    print("\n测试GET - 获取所有学生:")
    response = requests.get(base_url)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"返回数据数量: {len(data) if isinstance(data, list) else '非列表格式'}")
        print(f"响应内容预览: {json.dumps(data[:1], indent=2) if isinstance(data, list) and data else '无数据'}")
    else:
        print(f"请求失败: {response.text}")

# 测试POST方法 - 创建新学生
def test_post_student():
    print("\n测试POST - 创建新学生:")
    student_data = {
        "name": "测试学生",
        "age": 20,
        "gender": "男",
        "major": "计算机科学",
        "email": "test_student_1@example.com"
    }
    response = requests.post(base_url, json=student_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    return response

# 测试PUT方法 - 更新学生信息
def test_put_student(student_id):
    if not student_id:
        print("\n无法测试PUT - 没有有效的学生ID")
        return
    print(f"\n测试PUT - 更新学生 {student_id}:")
    update_data = {
        "name": "更新后的测试学生",
        "age": 21,
        "gender": "男",
        "major": "软件工程",
        "email": "updated_test_1@example.com"
    }
    response = requests.put(f"{base_url}{student_id}/", json=update_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

# 测试DELETE方法 - 删除学生
def test_delete_student(student_id):
    if not student_id:
        print("\n无法测试DELETE - 没有有效的学生ID")
        return
    print(f"\n测试DELETE - 删除学生 {student_id}:")
    response = requests.delete(f"{base_url}{student_id}/")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

# 运行所有测试
if __name__ == "__main__":
    print("开始测试学生管理API...")
    
    # 先测试GET获取所有学生
    test_get_all_students()
    
    # 测试POST创建新学生
    post_response = test_post_student()
    
    # 提取新创建的学生ID
    student_id = None
    if post_response.status_code == 201:
        try:
            student_id = post_response.json().get('id')
            print(f"新创建的学生ID: {student_id}")
        except:
            print("无法提取学生ID")
    
    # 如果没有获取到学生ID，可以尝试获取第一个学生的ID
    if not student_id:
        print("尝试从现有学生列表中获取第一个学生的ID...")
        get_response = requests.get(base_url)
        if get_response.status_code == 200:
            try:
                data = get_response.json()
                if isinstance(data, list) and data:
                    student_id = data[0].get('id')
                    print(f"获取到的学生ID: {student_id}")
            except:
                print("无法从现有学生列表中获取ID")
    
    # 测试PUT更新学生
    test_put_student(student_id)
    
    # 测试DELETE删除学生
    test_delete_student(student_id)
    
    # 最后再次获取所有学生，确认操作结果
    print("\n测试完成后的学生列表:")
    final_response = requests.get(base_url)
    if final_response.status_code == 200:
        final_data = final_response.json()
        print(f"最终学生数量: {len(final_data) if isinstance(final_data, list) else '非列表格式'}")
    
    print("\nAPI测试完成！")
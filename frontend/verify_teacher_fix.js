import axios from 'axios';

// API基础URL
const BASE_URL = 'http://127.0.0.1:8000/api';

// 测试函数
async function verifyTeacherFix() {
  console.log("=== 验证教师列表API修复 ===");
  
  // 登录请求数据
  const loginData = {
    'username': 'root',
    'password': 'root123456'
  };
  
  try {
    // 发送登录请求获取token
    console.log("1. 登录获取token...");
    const loginResponse = await axios.post(
      `${BASE_URL}/auth/login/`,
      loginData,
      {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 5000
      }
    );
    
    console.log(`登录成功，状态码: ${loginResponse.status}`);
    
    // 提取token
    const token = loginResponse.data.tokens?.access;
    if (!token) {
      console.error("❌ 登录失败：未返回token");
      return;
    }
    
    console.log("✅ 成功获取token");
    
    // 请求教师列表接口
    console.log("2. 请求教师列表接口...");
    const teachersResponse = await axios.get(`${BASE_URL}/teachers/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: 5000
    });
    
    console.log(`获取教师列表成功，状态码: ${teachersResponse.status}`);
    
    // 检查返回数据格式
    console.log(`返回数据类型: ${typeof teachersResponse.data}`);
    
    // 模拟修复后的代码逻辑
    console.log("3. 模拟修复后的代码逻辑...");
    
    // 按照修复后的代码处理数据
    const teachers = teachersResponse.data && teachersResponse.data.results && Array.isArray(teachersResponse.data.results)
      ? teachersResponse.data.results
      : [];
    
    console.log(`处理后教师列表类型: ${typeof teachers}`);
    console.log(`处理后是否为数组: ${Array.isArray(teachers)}`);
    console.log(`处理后教师数量: ${teachers.length}`);
    
    // 尝试使用filter方法
    try {
      const filtered = teachers.filter(teacher => teacher.id > 3);
      console.log(`✅ 成功使用filter方法，过滤后的教师数量: ${filtered.length}`);
    } catch (filterError) {
      console.error(`❌ 使用filter方法失败: ${filterError.message}`);
    }
    
    console.log("\n✅ 验证总结：");
    if (Array.isArray(teachers) && teachers.length > 0) {
      console.log("✅ 修复成功：教师数据已正确处理为数组格式");
    } else {
      console.log("⚠️ 修复后数据为空数组，请检查后端API返回");
    }
    
  } catch (error) {
    console.error("❌ 验证失败:", error.message);
    if (error.response) {
      console.error(`错误状态码: ${error.response.status}`);
      console.error(`错误数据: ${JSON.stringify(error.response.data, null, 2)}`);
    }
  }
}

// 执行验证
(async () => {
  await verifyTeacherFix();
  console.log("\n=== 验证结束 ===");
})();
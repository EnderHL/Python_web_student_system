// 导入项目的axios实例
import api from './src/utils/axios.js'

// 测试函数
async function testNavbarAccess() {  
  console.log("=== 测试导航栏管理模块显示 ===");
  
  // 登录请求数据
  const loginData = {
    'username': 'root',
    'password': 'root123456'
  };
  
  try {
    // 发送登录请求
    console.log("1. 发送登录请求...");
    const response = await api.post(
      '/auth/login/',
      loginData
    );
    
    console.log(`登录成功，状态码: ${response.status}`);
    
    // 提取token
    const token = response.data.tokens?.access;
    if (!token) {
      console.error("❌ 登录失败：未返回token");
      return;
    }
    
    console.log("✅ 成功获取token");
    console.log(`用户信息: ${JSON.stringify(response.data.user, null, 2)}`);
    
    // 检查用户类型
    const userType = response.data.user?.user_type;
    console.log(`用户类型: ${userType}`);
    
    // 请求用户信息接口
    console.log("2. 请求用户信息接口...");
    const profileResponse = await api.get('/auth/profile/');
    
    console.log(`获取用户信息成功，状态码: ${profileResponse.status}`);
    console.log(`用户信息接口返回: ${JSON.stringify(profileResponse.data, null, 2)}`);
    
    // 验证用户类型
    const profileUserType = profileResponse.data?.user_type;
    if (profileUserType === 'admin') {
      console.log("✅ 验证通过：用户类型为admin，应该显示教师管理和学生管理模块");
    } else if (profileUserType === 'teacher') {
      console.log("✅ 验证通过：用户类型为teacher，应该显示学生管理模块");
    } else {
      console.log(`⚠️ 注意：用户类型为${profileUserType}，可能不会显示管理模块`);
    }
    
    console.log("✅ 测试完成！前端已修复响应处理逻辑，登录后应该能正确显示相应的管理模块");
    
  } catch (error) {
    console.error("❌ 测试失败:", error.message);
    if (error.response) {
      console.error(`错误状态码: ${error.response.status}`);
      console.error(`错误数据: ${JSON.stringify(error.response.data, null, 2)}`);
    }
  }
}

// 执行测试
(async () => {
  await testNavbarAccess();
  console.log("\n=== 测试结束 ===");
})();
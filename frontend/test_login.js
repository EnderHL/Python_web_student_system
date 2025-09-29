// 模拟前端登录测试
import api from './src/utils/axios.js';

// 登录函数
async function testFrontendLogin() {
  console.log("=== 测试前端登录功能 ===");
  
  // 登录请求数据
  const loginData = {
    'username': 'root',
    'password': 'root123456'
  };
  
  try {
    // 发送登录请求
    const response = await api.post(
      '/auth/login/',
      loginData
    );
    
    console.log(`响应状态码: ${response.status}`);
    console.log(`响应数据: ${JSON.stringify(response.data, null, 2)}`);
    
    if (response.status === 200) {
      console.log("✅ 登录测试成功！");
      console.log(`是否返回token: ${!!response.data.tokens?.access}`);
      console.log(`是否返回用户信息: ${!!response.data.user}`);
    } else {
      console.log("❌ 登录测试失败！");
    }
  } catch (error) {
    console.error("❌ 登录请求失败:", error.message);
    if (error.response) {
      console.error(`错误状态码: ${error.response.status}`);
      console.error(`错误数据: ${JSON.stringify(error.response.data, null, 2)}`);
    }
  }
}

// 执行测试
(async () => {
  await testFrontendLogin();
  console.log("\n=== 测试完成 ===");
})();
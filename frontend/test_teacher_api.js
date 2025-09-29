// 导入项目的axios实例
import api from './src/utils/axios.js'

// 测试函数
async function testTeacherApi() {
  console.log("=== 测试教师API数据格式 ===");
  
  // 登录请求数据
  const loginData = {
    'username': 'root',
    'password': 'root123456'
  };
  
  try {
    // 发送登录请求获取token
    console.log("1. 登录获取token...");
    const loginResponse = await api.post(
      '/auth/login/',
      loginData
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
    const teachersResponse = await api.get('/teachers/');
    
    console.log(`获取教师列表成功，状态码: ${teachersResponse.status}`);
    
    // 检查返回数据类型
    console.log(`返回数据类型: ${typeof teachersResponse.data}`);
    console.log(`是否为数组: ${Array.isArray(teachersResponse.data)}`);
    
    if (!Array.isArray(teachersResponse.data)) {
      console.error("❌ 错误：教师API返回的不是数组");
      console.log("返回数据结构:", teachersResponse.data);
      
      // 检查是否有data属性包含数组
      if (teachersResponse.data && teachersResponse.data.data) {
        console.log(`data字段类型: ${typeof teachersResponse.data.data}`);
        console.log(`data字段是否为数组: ${Array.isArray(teachersResponse.data.data)}`);
        console.log("data字段内容:", teachersResponse.data.data);
      }
      
      // 检查是否有results属性包含数组
      if (teachersResponse.data && teachersResponse.data.results) {
        console.log(`results字段类型: ${typeof teachersResponse.data.results}`);
        console.log(`results字段是否为数组: ${Array.isArray(teachersResponse.data.results)}`);
        console.log("results字段内容:", teachersResponse.data.results);
      }
    } else {
      console.log("✅ 成功：教师API返回的是数组");
      console.log(`教师数量: ${teachersResponse.data.length}`);
      if (teachersResponse.data.length > 0) {
        console.log("第一个教师数据示例:", teachersResponse.data[0]);
      }
    }
    
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
  await testTeacherApi();
  console.log("\n=== 测试结束 ===");
})();
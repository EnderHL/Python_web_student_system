// 侧边栏修复测试脚本
// 此脚本用于清除localStorage并测试修复后的Navbar组件

// 模拟浏览器环境中的localStorage操作
function clearBrowserState() {
  try {
    console.log("=== 侧边栏修复测试开始 ===");
    
    // 清除localStorage中的用户信息和token
    console.log("1. 清除localStorage中的用户信息和token...");
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // 检查是否清除成功
    const remainingToken = localStorage.getItem('token');
    const remainingUser = localStorage.getItem('user');
    
    if (!remainingToken && !remainingUser) {
      console.log("✅ localStorage清除成功");
    } else {
      console.log("❌ localStorage清除失败");
      return;
    }
    
    console.log("2. 修复说明：");
    console.log("   - 已移除Navbar组件中的路由循环重定向");
    console.log("   - 增强了用户信息验证和错误处理");
    console.log("   - 优化了重定向逻辑，避免无限循环");
    
    console.log("\n=== 测试建议 ===");
    console.log("1. 关闭所有浏览器窗口，清除缓存");
    console.log("2. 重新打开浏览器，访问 http://localhost:5174/");
    console.log("3. 登录系统，验证侧边栏是否正常显示");
    console.log("4. 切换不同页面，确保没有无限加载或循环重定向问题");
    
    console.log("\n=== 侧边栏修复测试完成 ===");
  } catch (error) {
    console.error("测试过程中发生错误:", error);
  }
}

// 运行测试
if (typeof window !== 'undefined') {
  // 如果在浏览器环境中运行
  window.addEventListener('load', clearBrowserState);
} else {
  // 如果在Node.js环境中运行，输出提示信息
  console.log("请在浏览器控制台中运行此脚本:");
  console.log("复制以下代码并粘贴到浏览器控制台:");
  console.log("");
  console.log("// 侧边栏修复测试脚本\n" +
             "localStorage.removeItem('token');\n" +
             "localStorage.removeItem('user');\n" +
             "console.log('✅ localStorage清除成功，请刷新页面并测试');");
}
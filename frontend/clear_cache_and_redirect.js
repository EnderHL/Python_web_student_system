// 清理localStorage中的认证数据
localStorage.removeItem('token');
localStorage.removeItem('user');

// 显示清理成功信息
console.log('浏览器缓存和localStorage数据已清理');

// 重定向到登录页面
window.location.href = '/login';
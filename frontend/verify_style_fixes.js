// 前端样式修复验证脚本
// 此脚本用于验证全局样式修复是否解决了以下问题：
// 1. 页面背景色统一为纯白色
// 2. 表格内文字颜色统一修改为黑色
// 3. container区域尺寸优化

// 在浏览器控制台运行此脚本以验证修复效果
function verifyStyleFixes() {
  console.log('===== 前端样式修复验证结果 =====');
  
  // 1. 验证页面背景色
  const bodyBgColor = window.getComputedStyle(document.body).backgroundColor;
  console.log('页面背景色:', bodyBgColor);
  console.log('背景色是否为白色:', bodyBgColor === 'rgb(255, 255, 255)' || bodyBgColor === '#ffffff');
  
  // 2. 验证表格文字颜色
  const tables = document.querySelectorAll('table');
  if (tables.length > 0) {
    console.log('\n检测到的表格数量:', tables.length);
    
    tables.forEach((table, index) => {
      const tableId = table.id || `table-${index + 1}`;
      const firstCell = table.querySelector('td, th');
      
      if (firstCell) {
        const textColor = window.getComputedStyle(firstCell).color;
        console.log(`表格 ${tableId} 文字颜色:`, textColor);
        console.log(`表格 ${tableId} 文字颜色是否为黑色:`, 
                   textColor === 'rgb(0, 0, 0)' || textColor === '#000000');
      }
    });
  } else {
    console.log('\n未检测到表格，请在有表格的页面运行此脚本');
  }
  
  // 3. 验证容器尺寸
  const appContainer = document.getElementById('app');
  if (appContainer) {
    const appWidth = window.getComputedStyle(appContainer).width;
    const appMaxWidth = window.getComputedStyle(appContainer).maxWidth;
    console.log('\n#app 容器宽度:', appWidth);
    console.log('#app 容器最大宽度:', appMaxWidth);
    console.log('#app 容器是否最大化:', appMaxWidth === '100%' || appMaxWidth === 'none');
  }
  
  // 4. 检查主内容区域
  const mainContent = document.querySelector('.main-content');
  if (mainContent) {
    const mainContentBgColor = window.getComputedStyle(mainContent).backgroundColor;
    console.log('\n.main-content 背景色:', mainContentBgColor);
    console.log('.main-content 背景色是否为白色:', 
               mainContentBgColor === 'rgb(255, 255, 255)' || mainContentBgColor === '#ffffff');
  }
  
  console.log('\n===== 验证完成 =====');
  console.log('提示：若部分验证未通过，请刷新页面或清除浏览器缓存后重试。');
}

// 自动运行验证
verifyStyleFixes();

// 手动验证方法（如果需要再次验证）
// window.verifyStyles = verifyStyleFixes;

/*
使用说明：
1. 在浏览器中打开前端应用（http://localhost:5174/）
2. 按下 F12 打开开发者工具
3. 切换到 Console 标签页
4. 复制并粘贴此脚本，按 Enter 键运行
5. 查看验证结果

预期效果：
- 页面背景色应为白色 (rgb(255, 255, 255))
- 表格文字颜色应为黑色 (rgb(0, 0, 0))
- #app 容器应最大化显示，max-width 应为 100% 或 none
*/
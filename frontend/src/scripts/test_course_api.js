// 课程数据获取测试脚本
// 用于诊断课程管理页面无法查询到数据的问题

// 导入axios以进行API测试
import axios from './../utils/axios.js';

// 配置控制台日志颜色
const consoleColors = {
  success: '\x1b[32m',
  error: '\x1b[31m',
  info: '\x1b[36m',
  warning: '\x1b[33m',
  reset: '\x1b[0m'
};

// 格式化日志函数
function log(color, message) {
  console.log(`${color}[${new Date().toLocaleTimeString()}] ${message}${consoleColors.reset}`);
}

// 测试函数集合
const CourseApiTester = {
  // 测试axios基本配置
  async testAxiosConfig() {
    log(consoleColors.info, '测试axios配置...');
    log(consoleColors.info, `基础URL: ${axios.defaults.baseURL}`);
    log(consoleColors.info, `是否有认证token: ${axios.defaults.headers.common['Authorization'] ? '是' : '否'}`);
    
    // 测试网络连接
    try {
      const response = await fetch(axios.defaults.baseURL || 'http://127.0.0.1:8000', {
        method: 'HEAD',
        timeout: 5000
      });
      log(consoleColors.success, `服务器连接成功，状态码: ${response.status}`);
    } catch (error) {
      log(consoleColors.error, `服务器连接失败: ${error.message}`);
      log(consoleColors.warning, '请确认后端服务器是否正常运行在 http://127.0.0.1:8000');
    }
  },

  // 测试获取课程列表API
  async testFetchCourses(params = {}) {
    log(consoleColors.info, `测试获取课程列表API，参数: ${JSON.stringify(params)}`);
    try {
      const startTime = Date.now();
      const response = await axios.get('/courses/', { params });
      const endTime = Date.now();
      
      log(consoleColors.success, `API调用成功，耗时: ${endTime - startTime}ms`);
      log(consoleColors.info, `状态码: ${response.status}`);
      log(consoleColors.info, `返回数据类型: ${typeof response.data}`);
      
      if (Array.isArray(response.data)) {
        log(consoleColors.info, `返回课程数量: ${response.data.length}`);
        if (response.data.length > 0) {
          log(consoleColors.info, '前3条课程数据样本:');
          response.data.slice(0, 3).forEach((course, index) => {
            log(consoleColors.info, `  ${index + 1}. ${course.name || '无名称'} (ID: ${course.id})`);
          });
        } else {
          log(consoleColors.warning, '返回的课程列表为空');
        }
      } else if (response.data && typeof response.data === 'object') {
        // 检查是否是分页数据
        if (response.data.results && Array.isArray(response.data.results)) {
          log(consoleColors.info, `分页数据 - 总条数: ${response.data.count || 0}`);
          log(consoleColors.info, `分页数据 - 当前页课程数量: ${response.data.results.length}`);
          if (response.data.results.length > 0) {
            log(consoleColors.info, '前3条课程数据样本:');
            response.data.results.slice(0, 3).forEach((course, index) => {
              log(consoleColors.info, `  ${index + 1}. ${course.name || '无名称'} (ID: ${course.id})`);
            });
          } else {
            log(consoleColors.warning, '返回的课程列表为空');
          }
        } else {
          log(consoleColors.warning, '返回的数据不是预期的数组或分页对象格式');
          log(consoleColors.warning, `数据结构: ${JSON.stringify(Object.keys(response.data || {}))}`);
        }
      } else {
        log(consoleColors.error, '返回的数据格式不正确');
      }
      
      return response.data;
    } catch (error) {
      log(consoleColors.error, `API调用失败: ${error.message}`);
      if (error.response) {
        log(consoleColors.error, `  状态码: ${error.response.status}`);
        log(consoleColors.error, `  错误数据: ${JSON.stringify(error.response.data)}`);
        
        // 常见错误处理
        if (error.response.status === 401) {
          log(consoleColors.warning, '  认证失败，请确认是否已登录');
        } else if (error.response.status === 403) {
          log(consoleColors.warning, '  权限不足，您可能没有访问课程数据的权限');
        } else if (error.response.status === 404) {
          log(consoleColors.warning, '  API端点不存在，请检查URL是否正确');
        }
      } else if (error.request) {
        log(consoleColors.error, '  没有收到响应，请确认后端服务器是否运行正常');
      }
      return null;
    }
  },

  // 测试获取单个课程详情
  async testFetchCourseDetail(courseId) {
    log(consoleColors.info, `测试获取单个课程详情，ID: ${courseId}`);
    try {
      const response = await axios.get(`/courses/${courseId}/`);
      log(consoleColors.success, `获取课程详情成功，ID: ${courseId}`);
      log(consoleColors.info, `课程名称: ${response.data.name || '无名称'}`);
      log(consoleColors.info, `课程代码: ${response.data.code || '无代码'}`);
      return response.data;
    } catch (error) {
      log(consoleColors.error, `获取课程详情失败: ${error.message}`);
      if (error.response) {
        log(consoleColors.error, `  状态码: ${error.response.status}`);
      }
      return null;
    }
  },

  // 检查认证状态
  async checkAuthStatus() {
    log(consoleColors.info, '检查认证状态...');
    // 检查localStorage中的token
    const token = localStorage.getItem('token');
    log(consoleColors.info, `localStorage中的token: ${token ? '存在' : '不存在'}`);
    
    // 检查用户信息
    try {
      const response = await axios.get('/api/user/');
      log(consoleColors.success, '用户信息获取成功');
      log(consoleColors.info, `用户名: ${response.data.username}`);
      log(consoleColors.info, `用户角色: ${response.data.role || '未知'}`);
      return response.data;
    } catch (error) {
      log(consoleColors.error, `用户信息获取失败: ${error.message}`);
      return null;
    }
  },

  // 完整测试流程
  async runFullTest() {
    log(consoleColors.info, '=== 开始课程API完整测试 ===');
    
    // 1. 测试axios配置
    await this.testAxiosConfig();
    
    // 2. 检查认证状态
    await this.checkAuthStatus();
    
    // 3. 测试获取所有课程（无参数）
    const allCourses = await this.testFetchCourses();
    
    // 4. 测试带参数的课程查询
    if (allCourses) {
      await this.testFetchCourses({ page: 1, page_size: 10 });
      await this.testFetchCourses({ course_type: '必修' });
    }
    
    // 5. 如果有课程数据，测试获取单个课程详情
    if (allCourses && Array.isArray(allCourses) && allCourses.length > 0) {
      await this.testFetchCourseDetail(allCourses[0].id);
    } else if (allCourses && allCourses.results && allCourses.results.length > 0) {
      await this.testFetchCourseDetail(allCourses.results[0].id);
    }
    
    log(consoleColors.info, '=== 课程API测试完成 ===');
    
    // 生成问题诊断报告
    this.generateDiagnosticReport();
  },

  // 生成问题诊断报告
  generateDiagnosticReport() {
    log(consoleColors.info, '\n=== 问题诊断报告 ===');
    log(consoleColors.info, '请根据以上测试结果检查以下可能的问题:');
    log(consoleColors.info, '1. 后端服务器是否正常运行在 http://127.0.0.1:8000');
    log(consoleColors.info, '2. 是否已成功登录并持有有效的认证token');
    log(consoleColors.info, '3. 用户是否有访问课程数据的权限');
    log(consoleColors.info, '4. 课程数据表中是否存在数据');
    log(consoleColors.info, '5. API响应格式是否符合前端预期（数组或分页对象）');
    log(consoleColors.info, '6. 网络连接是否正常，是否有跨域问题');
    log(consoleColors.info, '==================\n');
  }
};

// 运行测试
if (typeof window !== 'undefined') {
  // 在浏览器环境中运行
  console.log('\n=== 课程数据获取测试工具 ===\n');
  CourseApiTester.runFullTest();
}

// 导出测试器供其他地方使用
export default CourseApiTester;
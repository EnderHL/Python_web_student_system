// 测试课程API的脚本，用于确定是前端还是后端问题
import axios from 'axios';

// 设置axios基础配置
axios.defaults.baseURL = 'http://localhost:8000'; // 假设后端运行在8000端口

// 测试获取所有课程
async function testGetCourses() {
    console.log('===== 测试获取所有课程 =====');
    try {
        const response = await axios.get('/api/courses/');
        console.log('状态码:', response.status);
        console.log('返回数据数量:', response.data.length);
        console.log('前3条数据:', response.data.slice(0, 3));
        return { success: true, data: response.data };
    } catch (error) {
        console.error('获取课程失败:', error.message);
        if (error.response) {
            console.error('响应状态码:', error.response.status);
            console.error('响应数据:', error.response.data);
        }
        return { success: false, error };
    }
}

// 测试获取教师列表
async function testGetTeachers() {
    console.log('\n===== 测试获取教师列表 =====');
    try {
        const response = await axios.get('/api/teachers/');
        console.log('状态码:', response.status);
        console.log('教师数量:', response.data.length);
        console.log('前3条教师数据:', response.data.slice(0, 3));
        return { success: true, data: response.data };
    } catch (error) {
        console.error('获取教师失败:', error.message);
        if (error.response) {
            console.error('响应状态码:', error.response.status);
            console.error('响应数据:', error.response.data);
        }
        return { success: false, error };
    }
}

// 测试获取教室列表
async function testGetClassrooms() {
    console.log('\n===== 测试获取教室列表 =====');
    try {
        const response = await axios.get('/api/classrooms/');
        console.log('状态码:', response.status);
        console.log('教室数量:', response.data.length);
        console.log('前3条教室数据:', response.data.slice(0, 3));
        return { success: true, data: response.data };
    } catch (error) {
        console.error('获取教室失败:', error.message);
        if (error.response) {
            console.error('响应状态码:', error.response.status);
            console.error('响应数据:', error.response.data);
        }
        return { success: false, error };
    }
}

// 测试数据库连接状态
async function testDatabaseConnection() {
    console.log('\n===== 测试数据库连接状态 =====');
    // 尝试访问一个需要数据库连接的简单接口
    try {
        // 假设存在一个健康检查接口
        const response = await axios.get('/api/health/');
        console.log('数据库连接状态:', response.data.database_status || '未知');
        return { success: true, data: response.data };
    } catch (error) {
        console.error('健康检查失败:', error.message);
        // 如果没有健康检查接口，就跳过具体错误显示
        return { success: false, error: '健康检查接口可能不存在' };
    }
}

// 运行所有测试
async function runAllTests() {
    console.log('开始测试课程系统API...\n');
    
    const coursesResult = await testGetCourses();
    const teachersResult = await testGetTeachers();
    const classroomsResult = await testGetClassrooms();
    await testDatabaseConnection();
    
    console.log('\n===== 测试总结 =====');
    console.log('课程API可用:', coursesResult.success);
    console.log('教师API可用:', teachersResult.success);
    console.log('教室API可用:', classroomsResult.success);
    
    if (coursesResult.success && coursesResult.data.length === 0) {
        console.log('警告: 课程API返回成功，但没有数据，请检查数据库中是否有课程记录。');
    }
    
    if (coursesResult.success) {
        console.log('\n结论: 后端API工作正常，问题可能在前端代码。');
        console.log('建议检查:');
        console.log('1. Course.js中的axios配置是否正确');
        console.log('2. API调用的URL是否与后端匹配');
        console.log('3. 数据加载后是否正确更新到界面');
    } else {
        console.log('\n结论: 后端API可能存在问题，请检查:');
        console.log('1. Django服务器是否正常运行');
        console.log('2. 后端API端点是否正确配置');
        console.log('3. 数据库连接是否正常');
        console.log('4. 是否有相关的权限问题');
    }
}

// 执行测试
runAllTests().catch(err => {
    console.error('测试过程中出现错误:', err);
});
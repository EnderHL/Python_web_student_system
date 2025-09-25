# 前端优化需求记录文件

## 紧急程度排序

### 1. 最高优先级：表格文字颜色修复
目前多数模块表格内文字为白色，与白色背景对比度不足导致内容模糊，需要将所有表格内文字颜色统一修改为黑色。

### 2. 中优先级：页面背景色统一
当前前端页面背景色非纯白色，向下滚动时可见黑色底色，需要将页面背景色统一调整为纯白色。

### 3. 中优先级：container区域尺寸优化
各模块点击后展开的container区域尺寸偏小，需要优化点击交互，使展开后的container区域在不与侧边栏及header区域重叠的前提下，尽可能最大化占据屏幕空间。

### 4. 中优先级：Element Plus样式应用
目前项目已全局引入Element Plus，但各页面尚未完全应用Element Plus组件和样式，需要逐步将各页面原生组件替换为Element Plus组件。

## 详细需求描述

### 1. 表格文字颜色修复
- 问题：表格内文字为白色，与白色背景对比度不足
- 目标：将所有表格内文字颜色统一修改为黑色
- 影响范围：所有包含表格的页面和组件

### 2. 页面背景色统一
- 问题：页面背景色非纯白色，向下滚动时可见黑色底色
- 目标：将页面背景色统一调整为纯白色
- 影响范围：全局样式

### 3. container区域尺寸优化
- 问题：展开后的container区域尺寸偏小
- 目标：优化点击交互，使展开后的container区域在不与侧边栏及header区域重叠的前提下，尽可能最大化占据屏幕空间
- 影响范围：所有包含可展开container的组件

### 4. Element Plus样式应用
- 问题：项目已全局引入Element Plus，但各页面尚未完全应用Element Plus组件和样式
- 目标：逐步将各页面原生组件替换为Element Plus组件，统一UI风格
- 影响范围：所有页面和组件

## Element Plus样式应用情况记录

### 当前应用状态

| 页面名称 | 是否已使用Element Plus组件 | 使用的组件 | 需要替换的组件 |
|---------|--------------------------|-----------|---------------|
| Login.vue | 是 | el-form, el-form-item, el-input, el-button, el-message, User图标, Lock图标 | 无
| Register.vue | 是 | el-form, el-form-item, el-input, el-select, el-button, el-message, User图标, Message图标, Lock图标 | 无
| Home.vue | 否 | 无 | 导航、用户信息展示 |
| Student.vue | 是 | el-form, el-form-item, el-input, el-select, el-button, el-table, el-dialog, el-message, el-message-box | 无 |
| Teacher.vue | 是 | el-form, el-form-item, el-input, el-select, el-button, el-table, el-dialog, el-message, el-message-box | 无 |
| Classroom.vue | 是 | el-dialog (详情和编辑弹窗) | 表格、表单、按钮、搜索框、分页 |
| Course.vue | 否 | 无 | 表格、表单、按钮、搜索框、分页、弹窗 |
| Schedule.vue | 否 | 无 | 表格、按钮 |

### 实施计划
1. 首先完成全局样式修复（已完成：表格文字颜色、页面背景色、container区域尺寸）
2. 按照页面优先级逐步替换原生组件为Element Plus组件
3. 确保组件替换后功能保持不变，交互体验一致
4. 统一各页面的UI风格和交互模式
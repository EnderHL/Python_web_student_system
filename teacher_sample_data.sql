-- 教师表示例数据插入语句
-- 注意：MySQL中NOW()函数会自动生成当前时间
INSERT INTO teacher_teacher (
    name, age, gender, title, department, 
    email, phone, avatar, hire_date, created_at, updated_at
) VALUES
    -- 记录1
    ('张三', 35, '男', '副教授', '计算机科学系', 
     'zhangsan@example.com', '13800138001', 'avatars/zhangsan.jpg', '2018-09-01', NOW(), NOW()),
    
    -- 记录2
    ('李四', 42, '女', '教授', '数学系', 
     'lisi@example.com', '13800138002', 'avatars/lisi.jpg', '2015-03-15', NOW(), NOW()),
    
    -- 记录3
    ('王五', 28, '男', '讲师', '物理系', 
     'wangwu@example.com', '13800138003', NULL, '2020-07-01', NOW(), NOW()),
    
    -- 记录4
    ('赵六', 45, '男', '教授', '化学系', 
     'zhaoliu@example.com', '13800138004', 'avatars/zhaoliu.jpg', '2012-09-01', NOW(), NOW()),
    
    -- 记录5
    ('钱七', 32, '女', '讲师', '英语系', 
     'qianqi@example.com', '13800138005', 'avatars/qianqi.jpg', '2019-02-18', NOW(), NOW()),
    
    -- 记录6
    ('孙八', 38, '男', '副教授', '历史系', 
     'sunba@example.com', '13800138006', NULL, '2016-08-01', NOW(), NOW()),
    
    -- 记录7
    ('周九', 50, '女', '教授', '生物系', 
     'zhoujiu@example.com', '13800138007', 'avatars/zhoujiu.jpg', '2008-05-20', NOW(), NOW()),
    
    -- 记录8
    ('吴十', 30, '男', '讲师', '地理系', 
     'wushi@example.com', '13800138008', 'avatars/wushi.jpg', '2021-01-10', NOW(), NOW()),
    
    -- 记录9
    ('郑十一', 40, '女', '副教授', '音乐系', 
     'zhengshiyi@example.com', '13800138009', NULL, '2014-09-01', NOW(), NOW()),
    
    -- 记录10
    ('王十二', 33, '男', '讲师', '体育系', 
     'wangshier@example.com', '13800138010', 'avatars/wangshier.jpg', '2017-11-05', NOW(), NOW());
<template>
  <div class="register-container">
    <div class="register-form">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            required
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            class="form-control"
            placeholder="请输入邮箱"
          />
        </div>

        <div class="form-group">
          <label for="first_name">名字</label>
          <input
            type="text"
            id="first_name"
            v-model="form.first_name"
            class="form-control"
            placeholder="请输入名字"
          />
        </div>

        <div class="form-group">
          <label for="last_name">姓氏</label>
          <input
            type="text"
            id="last_name"
            v-model="form.last_name"
            class="form-control"
            placeholder="请输入姓氏"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="form-control"
            placeholder="请输入密码"
          />
        </div>
        <div class="form-group">
          <label for="password2">确认密码</label>
          <input
            type="password"
            id="password2"
            v-model="form.password2"
            required
            placeholder="请再次输入密码"
          />
        </div>
        <div class="form-group">
          <label for="user_type">用户类型</label>
          <select id="user_type" v-model="form.user_type" required>
            <option value="student">学生</option>
            <option value="teacher">教师</option>
          </select>
        </div>
        <button type="submit" :disabled="loading" class="register-btn">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
    </div>
  </div>
</template>

<script src="../scripts/Register.js"></script>

<style scoped src="../styles/Register.css"></style>
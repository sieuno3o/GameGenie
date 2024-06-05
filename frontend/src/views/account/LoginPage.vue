<template>
  <div class="flex-col-center loginPageBox">
    <span class="loginTitle heading3">로그인</span>
    <div id="id" class="loginInputBox flex-row-left">
      <img src="../../assets/image/account/idIcon.png" class="loginIconImg">
      <input v-model="username" @keydown.enter="login" type="text" class="loginInput button2" id="inputId"
        placeholder="아이디">
    </div>
    <div id="password" class="loginInputBox flex-row-left">
      <img src="../../assets/image/account/passwordIcon.png" class="loginIconImg">
      <input v-model="password" @keydown.enter="login" type="password" class="loginInput button2" id="inputPassword"
        placeholder="비밀번호">
    </div>
    <button @click="login" type="submit" class="loginInputBox" id="loginButton">로그인</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <div class="flex-row-center">
      <span>아직 계정이 없으신가요?</span>
      <router-link to="/signup">
        <span class="goSignup">회원가입</span>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/api/accounts/login/', {
          username: this.username,
          password: this.password
        });
        if (response.status === 200) {
          const tokens = response.data;
          localStorage.setItem('access', tokens.access);
          localStorage.setItem('refresh', tokens.refresh);

          this.$router.push({ name: 'main' });
        }
      } catch (error) {
        console.error('Login failed:', error);
        if (error.response && error.response.status === 401) {
          this.errorMessage = '아이디 또는 비밀번호가 잘못되었습니다.';
        } else {
          this.errorMessage = '로그인 중 오류가 발생했습니다. 다시 시도해주세요.';
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.loginPageBox {
  margin-top: 100px;
}

.loginTitle {
  margin-bottom: 50px;
  font-size: 35px;
}

.loginInput {
  width: 100%;
  height: 100%;
  border: 0px;
  outline: none;
  padding-left: 15px;
  border-radius: 5px;
}

.loginIconImg {
  width: 50px;
  padding: 15px;
  border-right: 1px solid rgb(178, 178, 178);
}

.loginInputBox {
  border-width: 1px;
  border-style: solid;
  border-color: rgb(178, 178, 178);
  border-radius: 5px;
  width: 310px;
  height: 50px;
  margin-bottom: 23px;
}

#loginButton {
  background-color: $MAIN-COLOR-SKYBLUE;
  height: 48px;
  margin-bottom: 35px;
}

.goSignup {
  padding-left: 5px;
}
</style>

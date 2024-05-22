<template>
  <div class="flex-col-center loginPageBox">
    <span class="loginTitle heading3">로그인</span>
    <div id="id" class="loginInputBox flex-row-left">
      <img src="../../assets/image/loginIdIcon.png" class="loginIconImg">
      <input type="text" class="loginInput button2" id="inputId" placeholder="아이디">
    </div>
    <div id="password" class="loginInputBox flex-row-left">
      <img src="../../assets/image/loginPasswordIcon.png" class="loginIconImg">
      <input type="text" class="loginInput button2" id="inputPassword" placeholder="비밀번호">
    </div>
    <button type="submit" class="loginInputBox" id="loginButton">로그인</button>
    <div class="flex-row-center">
      <span>아직 계정이 없으신가요?</span>
      <router-link to="/signup">
        <span class="goSignup">회원가입</span>
      </router-link>
    </div>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
.loginPageBox {
  margin-top: 70px;
}

.loginTitle {
  margin-bottom: 50px;
  font-size: 35px;
}

.loginInput {
  border: 0px;
  outline: none;
  padding-left: 15px;
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
  width: 310px; height: 50px;
  margin-bottom: 23px;
}

#loginButton {
  background-color: $MAIN-COLOR-SKYBLUE;
  height: 43px;
  margin-bottom: 35px;
}

.goSignup {
  padding-left: 5px;
}
</style>

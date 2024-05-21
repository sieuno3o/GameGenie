<template>
  <div id="navbar" class="flex-center">
    <router-link to="/">
      <img src="../assets/image/logo2.png" class="navLogoImg">
    </router-link>
    <router-link to="/community">
      <span class="navCommunity">커뮤니티</span>
    </router-link>
    <div class="navAccount">
      <router-link to="/login">
        <span class="navLogin">로그인</span>
      </router-link>
      <router-link to="/signup">
        <span class="navSignup">회원가입</span>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "TheNavbar",
};
</script>

<style lang="scss" scoped>
#navbar {
  width: auto;
  height: 55px;
  background-color: $MAIN-COLOR-SKYBLUE;
  justify-content: space-between;
}

.navLogoImg {
  width: 130px;
  margin-top: -4px;
  padding-left: 25px;
}

a, 
a.router-link-exact-active,
a.router-link-active {
  text-decoration: none;
  color: inherit;
}

.navAccount {
  padding-right: 25px;
}

.navLogin {
  padding-right: 30px;
}
</style>

<template>
  <div id="navbar" class="flex-center">
    <router-link to="/">
      <img src="../assets/image/logo.png" class="navLogoImg">
    </router-link>
    <div class="flex-center">
      <router-link to="/community">
        <span class="navCommunity">커뮤니티</span>
      </router-link>
      <div class="navAccount">
        <router-link to="/login">
          <span class="navLogin">로그인</span>
        </router-link>
      </div>
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
  width: 140px;
  margin-top: -4px;
  padding-left: 25px;
}

a, 
a.router-link-exact-active,
a.router-link-active {
  text-decoration: none;
  color: inherit;
}

.navLogin {
  padding-right: 30px;
  margin-left: 30px;
}

.navCommunity:hover,
.navLogin:hover {
  color: $HOVER-COLOR;
}
</style>

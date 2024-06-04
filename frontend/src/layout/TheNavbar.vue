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
        <router-link v-if="!isLoggedIn" to="/login">
          <span class="navLogin">로그인</span>
        </router-link>
        <div v-else>
          <router-link :to="`/profile/${userId}`">
            <span class="navLogin">{{ username }}</span>
          </router-link>
          <span class="navLogout" @click="logout">로그아웃</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TheNavbar",
  data() {
    return {
      isLoggedIn: false,
      userId: null,
      username: '',
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('access');
      const userId = localStorage.getItem('userId');
      const username = localStorage.getItem('username');

      if (token && userId && username) {
        this.isLoggedIn = true;
        this.userId = userId;
        this.username = username;
      } else {
        this.isLoggedIn = false;
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
      }
    },
    logout() {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      this.isLoggedIn = false;
      this.userId = null;
      this.username = '';
      this.$router.push('/');
    }
  }
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

.navLogout {
  padding-right: 30px;
  cursor: pointer;
  color: inherit;
}

.navCommunity:hover,
.navLogin:hover,
.navLogout:hover {
  color: $HOVER-COLOR;
}
</style>

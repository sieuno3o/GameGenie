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
        <div v-else class="dropdown">
          <span class="navLogin" @click="toggleDropdown">{{ username }}</span>
          <div v-if="isDropdownOpen" class="dropdown-content">
            <router-link :to="`/profile/${userId}`">내 프로필</router-link>
            <a @click="logout">로그아웃</a>
          </div>
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
      isDropdownOpen: false
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
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    logout() {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      this.isLoggedIn = false;
      this.$router.push('/login');
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
  display: flex;
  align-items: center;
}

.flex-center {
  display: flex;
  align-items: center;
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
  cursor: pointer;
}

.navCommunity:hover,
.navLogin:hover {
  color: $HOVER-COLOR;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  position: absolute;
  background-color: #f9f9f9;
  max-width: 120px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  margin-top: 10px;
  margin-left: 13px;
  text-align: center;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown .dropdown-content {
  display: block;
}
</style>
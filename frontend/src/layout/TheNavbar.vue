<template>
  <div id="navbar" class="flex-center">
    <router-link to="/">
      <img src="../assets/image/logo.png" class="navLogoImg">
    </router-link>
    <div class="flex-center navLinks">
      <router-link to="/community">
        <span class="navCommunity NAV">커뮤니티</span>
      </router-link>
      <div class="navAccount">
        <router-link v-if="!isLoggedIn" to="/login">
          <span class="navLogin NAV">로그인</span>
        </router-link>
        <div v-else class="dropdown">
          <span class="navLogin NAV" @click="toggleDropdown">{{ nickname }}</span>
          <div v-if="isDropdownOpen" class="dropdown-content">
            <router-link :to="{ name: 'profile', params: { nickname: nickname } }" class="dropdown-item flex-center">
              <span class="dropdown-font button2">내 프로필</span>
            </router-link>
            <a @click="logout" class="dropdown-item flex-center">
              <span class="dropdown-font button2">로그아웃</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "TheNavbar",
  data() {
    return {
      isLoggedIn: false,
      nickname: '',
      isDropdownOpen: false
    };
  },
  created() {
    this.checkLoginStatus();
  },
  mounted() {
    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick);
  },
  methods: {
    async checkLoginStatus() {
      try {
        const token = localStorage.getItem('access');
        if (token) {
          const response = await axios.get('http://localhost:8000/api/accounts/profile/', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (response.data) {
            this.isLoggedIn = true;
            this.nickname = response.data.nickname;
          } else {
            this.isLoggedIn = false;
          }
        }
      } catch (error) {
        this.isLoggedIn = false;
      }
    },
    async logout() {
      try {
        const refreshToken = localStorage.getItem('refresh');
        await axios.post('http://localhost:8000/api/accounts/logout/', { refresh: refreshToken }, {
          headers: {} // 인증 헤더를 비웁니다.
        });
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('nickname');
        this.isLoggedIn = false;
        this.nickname = '';
        this.$router.push({ name: 'main' });
      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    handleOutsideClick(event) {
      if (!event.target.closest('.dropdown')) {
        this.isDropdownOpen = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
#navbar {
  width: 100%;
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

.navLinks {
  margin-left: 15px;
  display: flex;
  align-items: center;
}

a,
a.router-link-exact-active,
a.router-link-active {
  text-decoration: none;
  color: inherit;
}

.navLogin {
  cursor: pointer;
}

.NAV {
  margin-right: 35px;
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
  width: 110px;
  box-shadow: 0px 5px 15px 0px rgba(0, 0, 0, 0.1);
  z-index: 1;
  margin-top: 10px;
  margin-left: -40px;
}

.dropdown-content .dropdown-item {
  display: flex;
  align-items: center;
  padding: 14px 12px;
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.dropdown-content .dropdown-item:hover {
  background-color: #f1f1f1;
}

.logout-button {
  cursor: pointer;
}
</style>

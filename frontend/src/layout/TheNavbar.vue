<template>
  <div id="navbar" class="flex-center">
    <router-link to="/">
      <img src="../assets/image/logo.png" class="navLogoImg">
    </router-link>
    <div class="flex-center navLinks">
      <router-link to="/community">
        <span class="navCommunity">커뮤니티</span>
      </router-link>
      <div class="navAccount">
        <router-link v-if="!isLoggedIn" to="/login">
          <span class="navLogin">로그인</span>
        </router-link>
        <div v-else class="dropdown">
          <span class="navLogin" @click="toggleDropdown">{{ nickname }}</span>
          <div v-if="isDropdownOpen" class="dropdown-content">
            <router-link :to="`/profile/${userId}`" class="dropdown-item">
              <span class="dropdown-font button2">내 프로필</span>
            </router-link>
            <a @click="logout" class="dropdown-item">
              <span class="dropdown-font button2">로그아웃</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: "TheNavbar",
  data() {
    return {
      isLoggedIn: false,
      userId: null,
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
        const response = await api.get('accounts/profile/');
        if (response.data) {
          this.isLoggedIn = true;
          this.userId = response.data.id;
          this.nickname = response.data.nickname;
        } else {
          this.isLoggedIn = false;
        }
      } catch (error) {
        this.isLoggedIn = false;
      }
    },
    async logout() {
      try {
        const refreshToken = localStorage.getItem('refresh');
        await api.post('accounts/logout/', { refresh: refreshToken });
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        this.isLoggedIn = false;
        this.userId = null;
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
  /* 전체 너비를 차지하도록 설정 */
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
  /* navLinks 요소에 왼쪽 마진 추가 */
  display: flex;
  /* Flexbox 사용 */
  align-items: center;
  /* 세로 정렬 */
}

a,
a.router-link-exact-active,
a.router-link-active {
  text-decoration: none;
  color: inherit;
}

.navLogin {
  padding-right: 30px;
  margin-left: 15px;
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
  width: 150px;
  /* 너비를 고정하여 글자가 일직선으로 정렬되도록 함 */
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  margin-top: 10px;
  margin-left: -25px;
  /* 드롭다운 위치 조정 */
}

.dropdown-content .dropdown-item {
  display: flex;
  /* Flexbox 사용 */
  align-items: center;
  /* 세로 정렬 */
  padding: 8px 12px;
  /* padding 조정 */
  color: black;
  text-decoration: none;
  cursor: pointer;
  /* 마우스를 올렸을 때 클릭 가능한 모양 */
}

.dropdown-content .dropdown-item:hover {
  background-color: #f1f1f1;
}

.logout-button {
  cursor: pointer;
}</style>

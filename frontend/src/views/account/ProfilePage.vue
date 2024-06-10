<template>
  <div class="profile-page">
    <!-- 프로필 영역 -->
    <div class="profileInfoBox">
      <span class="titleText">프로필</span>
      <div class="userInfo" v-if="user">
        <span class="body1">사용자 이름: {{ user.username }}</span>
        <span class="body1">닉네임: {{ user.nickname }}</span>
        <span class="body1">이메일: {{ user.email }}</span>
        <v-btn color="primary" @click="showEditModal = true">정보 수정</v-btn>
      </div>
    </div>

    <!-- 즐겨찾기한 게임 목록 영역 -->
    <div v-if="favorites && favorites.length" class="bookmarkGamebox">
      <span class="titleText">즐겨찾기한 게임</span>
      <div class="bookmarkGameList">
        <v-row class="game-cards flex-row-center">
          <game-card v-for=" game in paginatedFavorites" :key="game.id" :game="game" class="gameCards" />
        </v-row>
        <v-pagination v-model="currentPage" :length="pageCount" :total-visible="4"
          @input="handlePageChange"></v-pagination>
      </div>
    </div>

    <div v-else>
      <p>즐겨찾기한 게임이 없습니다.</p>
    </div>

    <!-- 프로필 수정 모달 -->
    <v-dialog v-model="showEditModal" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">계정 정보 수정</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editData.email" label="이메일" /> <!-- 이메일 필드 추가 -->
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editData.nickname" label="닉네임" /> <!-- 닉네임 필드 추가 -->
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editData.currentPassword" label="현재 비밀번호" type="password" />
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editData.newPassword" label="새 비밀번호" type="password" />
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editData.confirmPassword" label="새 비밀번호 확인" type="password" />
              </v-col>
            </v-row>
            <v-row v-if="updateError">
              <v-col cols="12">
                <p class="error-message">{{ updateError }}</p>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showEditModal = false">취소</v-btn>
          <v-btn color="blue darken-1" text @click="updateProfile">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import GameCard from '@/views/GameCard.vue';

export default {
  components: {
    GameCard
  },
  data() {
    return {
      user: null,
      favorites: [],
      showEditModal: false,
      editData: {
        email: '',
        nickname: '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      updateError: '',
      errorMessage: '',
      currentPage: 1,
      itemsPerPage: 8
    };
  },
  computed: {
    formattedFavorites() {
      return this.favorites.map(favorite => ({
        image_url: favorite.game_image,
        name: favorite.game_name,
        review_summary: favorite.game_review,
        price: favorite.game_price,
        store_url: favorite.game_url,
        id: favorite.id
      }));
    },
    paginatedFavorites() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.formattedFavorites.slice(start, end);
    },
    pageCount() {
      return Math.ceil(this.formattedFavorites.length / this.itemsPerPage);
    }
  },
  async mounted() {
    try {
      const accessToken = localStorage.getItem('access');
      if (accessToken) {
        console.log('Fetching user data...');
        const userResponse = await axios.get('http://localhost:8000/api/accounts/profile/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        this.user = userResponse.data;
        this.editData.email = this.user.email; // 이메일 설정
        this.editData.nickname = this.user.nickname; // 닉네임 설정
        console.log('User data:', this.user);

        console.log('Fetching favorite games...');
        const favoritesResponse = await axios.get('http://localhost:8000/api/recommendations/favorites/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        this.favorites = favoritesResponse.data;
        console.log('Favorite games:', this.favorites);
      } else {
        this.errorMessage = '로그인이 필요합니다.';
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        this.errorMessage = '인증되지 않았습니다. 다시 로그인해주세요.';
        this.$router.push({ name: 'login' });
      } else {
        console.error('Error fetching user or favorites:', error);
        this.errorMessage = '정보를 가져오는 중 오류가 발생했습니다.';
      }
    }
  },
  methods: {
    handlePageChange(page) {
      this.currentPage = page;
    },
    async updateProfile() {
      const { email, nickname, currentPassword, newPassword, confirmPassword } = this.editData;
      if (newPassword !== confirmPassword) {
        this.updateError = '새 비밀번호가 일치하지 않습니다.';
        return;
      }

      try {
        const accessToken = localStorage.getItem('access');
        const response = await axios.patch('http://localhost:8000/api/accounts/profile/', {
          email, // 이메일 추가
          nickname,
          old_password: currentPassword,
          new_password: newPassword
        }, {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (response.status === 200) {
          this.user.email = email; // 업데이트된 이메일 반영
          this.user.nickname = nickname;
          this.showEditModal = false;
          alert('프로필이 성공적으로 업데이트되었습니다.');
        } else {
          this.updateError = response.data.message || '프로필 업데이트에 실패했습니다.';
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.updateError = error.response.data.message || '프로필 업데이트 중 오류가 발생했습니다.';
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.profile-page {
  display: flex;
  justify-content: space-between;
  padding: 50px;
}

.profileInfoBox {
  width: calc(25% - 15px);
  box-sizing: border-box;
}

.bookmarkGamebox {
  width: calc(75% - 15px);
  box-sizing: border-box;
}

.titleText {
  font-size: 25px;
  background-color: white;
  padding: 20px 30px;
  border-radius: 10px 10px 0px 0px;
}

.userInfo,
.bookmarkGameList {
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 30px 50px;
  border-radius: 0px 10px 10px 10px;
}

.gameCards {
  margin-bottom: 20px;
}
  
.error-message {
  color: red;
  font-size: 14px;
}
</style>

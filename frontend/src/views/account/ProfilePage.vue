<template>
  <div class="profile-page">
    <!-- 프로필 영역 -->
    <div class="profileInfoBox">
      <span class="titleText">프로필</span>
      <div class="userInfo" v-if="user">
        <img :src="user.profileImage || defaultProfileImage" alt="Profile Image" class="profileImage"
          @click="triggerProfileImageUpload" />
        <input type="file" ref="profileImageInput" @change="handleProfileImageChange" accept="image/*"
          style="display: none;" />
        <div> <span class="body1 userName">아이디</span> <span class="body1">{{ user.username }}</span> </div>
        <div> <span class="body1 userNickName">닉네임</span> <span class="body1">{{ user.nickname }}</span> </div>
        <span class="body1 userEmail">{{ user.email }}</span>
        <v-btn @click="showEditModal = true" class="editButton">정보 수정</v-btn>
      </div>
    </div>

    <!-- 즐겨찾기한 게임 목록 영역 -->
    <div>
      <span class="titleText">즐겨찾기한 게임</span>
      <div class="bookmarkGameList">
        <div v-if="favorites && favorites.length" class="bookmarkGamebox">
          <v-row class="game-cards flex-row-center">
            <game-card v-for="game in paginatedFormattedFavorites" :key="game.id" :game="game" class="gameCards" />
          </v-row>
          <v-pagination class="pagination" v-model="currentPage" :length="pageCount" :total-visible="3"
            @input="handlePageChange"></v-pagination>
          </div>
        <div v-else>
          <p>즐겨찾기한 게임이 없습니다.</p>
        </div>
      </div>
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
                <v-text-field v-model="editData.email" label="이메일" />
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editData.nickname" label="닉네임" />
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
import api from '../../api';
import GameCard from '@/views/GameCard.vue';
import defaultProfileImage from '@/assets/image/account/profileImgIcon.png'; // Corrected import path

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
        confirmPassword: '',
        profileImage: null
      },
      updateError: '',
      currentPage: 1,
      itemsPerPage: 8,
      defaultProfileImage: defaultProfileImage
    };
  },
  computed: {
    paginatedFormattedFavorites() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      const paginatedFavorites = this.favorites.slice(start, end);
      return paginatedFavorites.map(favorite => ({
        image_url: favorite.game_image,
        name: favorite.game_name,
        review_summary: favorite.game_review,
        price: favorite.game_price,
        store_url: favorite.game_url,
        id: favorite.id
      }));
    },
    pageCount() {
      return Math.ceil(this.favorites.length / this.itemsPerPage);
    }
  },
  async mounted() {
    try {
      const accessToken = localStorage.getItem('access');
      if (accessToken) {
        console.log('Fetching user data...');
        const userResponse = await api.get('accounts/profile/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        this.user = userResponse.data;
        this.editData.email = this.user.email;
        this.editData.nickname = this.user.nickname;
        console.log('User data:', this.user);

        console.log('Fetching favorite games...');
        const favoritesResponse = await api.get('recommendations/favorites/', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        this.favorites = favoritesResponse.data;
        console.log('Favorite games:', this.favorites); // 로그 추가
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
    triggerProfileImageUpload() {
      this.$refs.profileImageInput.click();
    },
    handleProfileImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.editData.profileImage = file;
        this.updateProfileImage();
      }
    },
    async updateProfileImage() {
      try {
        const accessToken = localStorage.getItem('access');
        const formData = new FormData();
        formData.append('profile_image', this.editData.profileImage);

        const response = await api.patch('accounts/profile/', formData, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.status === 200) {
          this.user.profileImage = URL.createObjectURL(this.editData.profileImage);
          alert('프로필 사진이 성공적으로 업데이트되었습니다.');
        } else {
          this.updateError = response.data.message || '프로필 사진 업데이트에 실패했습니다.';
        }
      } catch (error) {
        console.error('Error updating profile image:', error);
        this.updateError = error.response.data.message || '프로필 사진 업데이트 중 오류가 발생했습니다.';
      }
    },
    async updateProfile() {
      const { email, nickname, currentPassword, newPassword, confirmPassword, profileImage } = this.editData;
      if (newPassword !== confirmPassword) {
        this.updateError = '새 비밀번호가 일치하지 않습니다.';
        return;
      }

      try {
        const accessToken = localStorage.getItem('access');
        const formData = new FormData();
        formData.append('email', email);
        formData.append('nickname', nickname);
        formData.append('old_password', currentPassword);
        formData.append('new_password', newPassword);
        if (profileImage) {
          formData.append('profile_image', profileImage);
        }

        const response = await api.patch('accounts/profile/', formData, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.status === 200) {
          this.user.email = email;
          this.user.nickname = nickname;
          if (profileImage) {
            this.user.profileImage = URL.createObjectURL(profileImage);
          }
          this.showEditModal = false;
          this.editData.currentPassword = '';
          this.editData.newPassword = '';
          this.editData.confirmPassword = '';
          alert('프로필이 성공적으로 업데이트되었습니다.');
        } else {
          this.updateError = response.data.message || '프로필 업데이트에 실패했습니다.';
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        this.updateError = error.response.data.message || '프로필 업데이트 중 오류가 발생했습니다.';
      }
    },
    handlePageChange(page) {
      this.currentPage = page;
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
  width: 250px;
  margin-right: 40px;
}

.profileImage {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 20px;
  cursor: pointer;
}

.bookmarkGamebox {
  width: 1100px;
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
  box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
}

.bookmarkGameList {
  padding: 60px 70px;
}

.error-message {
  color: red;
  font-size: 14px;
}

.pagination {
  padding-right: 32px;
  margin-bottom: -40px;
  margin-top: 10px;
}

.body1 {
  margin-bottom: 10px;
}

.userName,
.userNickName {
  margin-right: 5px;
  font-weight: bold;
}

.editButton {
  border: none;
  cursor: pointer;
  height: 35px;
  box-shadow: none;
  color: white;
  background-color: $MAIN-COLOR-NAVY;
  font-weight: bold;
}
</style>
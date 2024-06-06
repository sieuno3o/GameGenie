<template>
  <div class="communityProfile" v-if="communityItem">
    <h1>{{ communityItem.title }}</h1>
    <h3>카테고리 : {{ communityItem.category }}</h3>
    <h3>작성 일 : {{ formatDate(communityItem.created_at) }}</h3>
    <h3>작성자 : {{ communityItem.author_nickname }}</h3>
    <div>{{ communityItem.image }}</div>
    <p>{{ communityItem.content }}</p>
    <div class="likeRow">
      <button class="likeButton" @click="toggleLike">♥</button>
      <h3>{{ communityItem.community_like ? communityItem.community_like.length : 0 }}</h3>
    </div>
    <div class="detailButtonList">
      <router-link to="/community/">
        <button class="detailButton">목록으로</button>
      </router-link>
      <v-btn class="detailButton" color="primary" @click="showEditModal = true">게시글 수정</v-btn>
      <button class="detailButton" style="background-color: #FF9393;" @click="deletePost">삭제하기</button>
    </div>
    <v-dialog v-model="showEditModal" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">게시글 수정</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="editData.title" label="제목" />
                            </v-col>
                            <v-col cols="12">
                                <v-textarea v-model="editData.content" label="내용" />
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showEditModal = false">취소</v-btn>
                    <v-btn color="blue darken-1" text @click="updatePost">저장</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
  </div>
</template>

<script>
import api from '../../api';

export default {
  data() {
    return {
      communityItem: null,
      isLiked: false,
      isLoggedIn: false,
      userId: null,
      newComment: '',
      post: null,
      showEditModal: false,
      editData: {
        title: '',
        content: '',
      },
      errorMessage: ''
    };
  },
  async created() {
    await this.checkLoginStatus();
    const id = this.$route.params.id;
    await this.fetchCommunityItem(id);
  },
  methods: {
    async fetchCommunityItem(id) {
      try {
        const response = await api.get(`community/${id}/`);
        this.communityItem = response.data;
      } catch (error) {
        console.error("게시글을 가져오는 중 오류가 발생했습니다:", error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      const hours = ('0' + date.getHours()).slice(-2);
      const minutes = ('0' + date.getMinutes()).slice(-2);
      const seconds = ('0' + date.getSeconds()).slice(-2);
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    async checkLoginStatus() {
      const token = localStorage.getItem('access');
      if (token) {
        try {
          const response = await api.get('accounts/profile/', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          this.isLoggedIn = true;
          this.userId = response.data.username;
        } catch (error) {
          console.error("로그인 상태를 확인하는 중 오류가 발생했습니다:", error);
        }
      }
    },
    async toggleLike() {
      try {
        const response = await api.patch(`community/${this.communityItem.id}/like/`);
        this.isLiked = response.data.is_liked;
        this.communityItem.community_like = [...response.data.community_like];
      } catch (error) {
        console.error("좋아요 처리 중 오류가 발생했습니다:", error);
        this.isLiked = !this.isLiked;
      }
    },
    async addComment() {
      if (this.newComment.trim() === '') return;
      const id = this.$route.params.id;
      try {
        const response = await api.post(`community/comments/${id}/create/`, {
          content: this.newComment
        });
        this.communityItem.comments.push(response.data);
        this.newComment = '';
      } catch (error) {
        console.error("댓글 작성 중 오류가 발생했습니다:", error);
      }
    },
    goBack() {
      this.$router.push({ name: 'communityMain' });
    },
    async fetchData() {
      try {
        const communityId = this.$route.params.id;
        const accessToken = this.getAccessToken();
        if (!accessToken) {
          this.errorMessage = '로그인이 필요합니다.';
          return;
        }
        const response = await api.get(`community/${communityId}/`, {
          headers: { 'Authorization': `Bearer ${accessToken}` },
        });
        this.communityItem = response.data;
        this.editData.title = this.communityItem.title;
        this.editData.content = this.communityItem.content;
      } catch (error) {
        console.error("게시글을 가져오는 중 오류가 발생했습니다:", error);
        this.errorMessage = '게시글을 가져오는 중 오류가 발생했습니다.';
      }
    },
    getAccessToken() {
      // 이 함수는 예시입니다. 실제로는 HttpOnly 쿠키를 사용하는 것이 좋습니다.
      return localStorage.getItem('access');
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    async updatePost() {
      const { title, content } = this.editData;
      try {
        const communityId = this.$route.params.id;
        const accessToken = this.getAccessToken();
        const response = await api.patch(`community/${communityId}/`, {
          title,
          content,
        }, {
          headers: { 'Authorization': `Bearer ${accessToken}` },
        });

        if (response.status === 200) {
          this.communityItem.title = title;
          this.communityItem.content = content;
          this.closeEditModal();
          alert('게시글이 성공적으로 업데이트되었습니다.');
        }
      } catch (error) {
        console.error('Error updating post:', error);
        alert('게시글 업데이트 중 오류가 발생했습니다.');
      }
    },
    async deletePost() {
      if (confirm('정말 삭제하시겠습니까?')) {
        try {
          await api.delete(`community/${this.communityItem.id}/`);
          this.$router.push({ name: 'communityMain' });
        } catch (error) {
          console.error('게시글 삭제 중 오류가 발생했습니다:', error);
          alert('게시글 삭제에 실패했습니다. 다시 시도해주세요.');
        }
      }
    }
  }
};
</script>

<style>
.communityProfile {
  width: 100%;
  font-size: 30px;
  margin: 40px;
  text-align: center;
}

.detailButtonList {
  display: flex;
  margin: 10px;
  gap: 10px;
  justify-content: center;
}

.detailButton {
  padding: 10px;
  font-size: 16px;
  border-radius: 10px;
  background-color: white;
  border: 0.3px solid rgba(0, 0, 0, 0.3);
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.3);
  text-decoration: none;
  color: black;
}

h1 {
  font-size: 2em;
  margin-bottom: 10px;
}

h3 {
  font-size: 14px;
  text-align: center;
}

.likeRow {
  display: flex;
  justify-content: center;
}

.likeButton {
  color: red;
  height: 30px;
  font-size: 25px;
  text-align: center;
}

.content {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 8px;
}

.actions {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.like-section {
  font-size: 1.5em;
  cursor: pointer;
}

.comments-section {
  margin-top: 40px;
}

.comment {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.comment img {
  height: 40px;
  width: 40px;
  border-radius: 50%;
}

.add-comment {
  margin-top: 20px;
}

.add-comment textarea {
  width: 100%;
  height: 80px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.add-comment button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>

<template>
  <div class="communityProfile" v-if="communityItem">
    <!-- 제목 부분 -->
    <div>
      <div>
        <span class="communityItemTitle heading1">{{ communityItem.title }}</span>
      </div>
      <div class="flex-between communityItemBox">
        <div class="flex-center">
          <span class="communityItemDeatil">카테고리 {{ getCategoryName(communityItem.category) }}</span>
          <span class="communityListInfoContour">|</span>
          <span class="communityItemDeatil">작성자 {{ communityItem.author_nickname }}</span>
          <span class="communityListInfoContour">|</span>
          <span class="communityItemDeatil">작성 일 {{ formatDate(communityItem.created_at) }}</span>
        </div>
        <div class="flex-center">
          <span class="communityItemDeatil">조회 수 {{ communityItem.view_count }}</span>
          <span class="communityListInfoContour">|</span>
          <span class="communityItemDeatil">좋아요 수 {{ likesCount }}</span>
          <!-- <span class="communityItemDeatil">댓글 수 {{ commentCount }}</span> -->
        </div>
      </div>
    </div>
    <!-- 이미지 -->
    <div v-if="communityItem.image"><img :src="getImageUrl(communityItem.image)" alt="게시글 이미지" class="communityItemImg">
    </div>
    <!-- 내용 -->
    <span class="communityItemContent body3 flex-left">{{ communityItem.content }}</span>
    <!-- 좋아요 -->
    <div class="likeRow">
      <button class="likeButton" :class="{ liked: isLiked }" @click="toggleLike">
        ♥
      </button>
      <span class="likesCount">{{ likesCount }}</span>
    </div>
    <!-- 버튼 -->
    <div class="detailButtonList">
      <button class="detailButton" @click="goToCommunity">목록으로</button>
      <div v-if="communityItem.author_id === userId" class="editDeleteButtons">
        <v-btn class="detailButton" @click="showEditModal = true">수정하기</v-btn>
        <button class="detailButton" @click="deletePost">삭제하기</button>
      </div>
    </div>
    <div class="commentsList">
      <h2>댓글</h2>
      <div v-if="comments && comments.length > 0" class="commentBox">
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <img :src="comment.author_profile_image || defaultProfileImage" alt="프로필 이미지" class="commentProfileImage" />
          <div>
            <h2><strong>{{ comment.author_nickname }}</strong></h2>
            <span>{{ formatDate(comment.created_at) }}</span>
            <p>{{ comment.comments }}</p>
            <v-btn v-if="comment.author_id === userId" small @click="editComment(comment)">수정</v-btn>
            <v-btn v-if="comment.author_id === userId" small color="error" @click="deleteComment(comment.id)">삭제</v-btn>
          </div>
        </div>
      </div>
      <div v-if="isLoggedIn">
        <v-textarea v-model="newComment" label="댓글 작성"></v-textarea>
        <v-btn @click="addComment">댓글 달기</v-btn>
      </div>
      <div v-else>
        <p>로그인 후 댓글을 작성할 수 있습니다.</p>
      </div>
    </div>
    <v-dialog v-model="showEditCommentModal" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">댓글 수정</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-textarea v-model="editCommentData.comments" label="내용" />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showEditCommentModal = false">취소</v-btn>
          <v-btn color="blue darken-1" text @click="updateComment">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '../../api';
import defaultProfileImage from '@/assets/image/account/profileImgIcon.png';

export default {
  data() {
    return {
      communityItem: null,
      comments: [],
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
      editCommentData: {
        id: null,
        comments: '',
      },
      showEditCommentModal: false,
      errorMessage: '',
      defaultProfileImage: defaultProfileImage,
      likesCount: 0, // 좋아요 숫자 변수 추가
      categories: [] // 카테고리 목록
    };
  },
  async created() {
    await this.checkLoginStatus();
    const id = this.$route.params.id;
    await this.fetchCommunityItem(id);
    await this.fetchComments(id);
    await this.fetchCategories(); // 카테고리 목록 불러오기
  },
  methods: {
    async fetchCommunityItem(id) {
      try {
        const response = await api.get(`community/${id}/`);
        this.communityItem = response.data;
        this.likesCount = this.communityItem.community_like ? this.communityItem.community_like.length : 0; // 좋아요 숫자 설정
        this.isLiked = this.communityItem.community_like.some(like => like.user_id === this.userId);
      } catch (error) {
        console.error("게시글을 가져오는 중 오류가 발생했습니다:", error);
      }
    },
    async fetchCategories() {
      try {
        const response = await api.get('community/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('카테고리를 불러오는 중 오류가 발생했습니다:', error);
      }
    },
    getCategoryName(key) {
      const category = this.categories.find(category => category.key === key);
      return category ? category.value : '알 수 없음';
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
    getImageUrl(imagePath) {
      return `http://localhost:8000${imagePath}`;
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
          this.userId = response.data.id;
        } catch (error) {
          console.error("로그인 상태를 확인하는 중 오류가 발생했습니다:", error);
        }
      }
    },
    async toggleLike() {
      if (!this.isLoggedIn) {
        console.error("로그인이 필요합니다.");
        return;
      }

      try {
        const response = await api.patch(`community/${this.communityItem.id}/like/`, null, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access')}`
          }
        });
        if (response.data && typeof response.data.likes_count !== 'undefined') {
          this.likesCount = response.data.likes_count;
          this.isLiked = response.data.liked; // Update the isLiked state based on the response
        } else {
          console.error("Invalid response data", response.data);
        }
      } catch (error) {
        console.error("좋아요 처리 중 오류가 발생했습니다:", error);
      }
    },
    async fetchComments(id) {
      try {
        const response = await api.get(`community/${id}/comments/`);
        this.comments = response.data.results;
      } catch (error) {
        console.error("댓글을 가져오는 중 오류가 발생했습니다:", error);
        this.errorMessage = "댓글을 가져오는 중 오류가 발생했습니다.";
      }
    },
    async addComment() {
      if (this.newComment.trim() === '') return;
      const id = this.$route.params.id;
      try {
        await api.post(`community/${id}/comments/create/`, {
          comments: this.newComment
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access')}`
          }
        });
        await this.fetchComments(id);  // 댓글 목록을 다시 가져옴
        this.newComment = '';
      } catch (error) {
        console.error("댓글 작성 중 오류가 발생했습니다:", error);
        this.errorMessage = "댓글 작성 중 오류가 발생했습니다.";
      }
    },
    editComment(comment) {
      this.editCommentData.id = comment.id;
      this.editCommentData.comments = comment.comments;
      this.showEditCommentModal = true;
    },
    async updateComment() {
      const { id, comments } = this.editCommentData;
      try {
        console.log(`Updating comment ${id} with content: ${comments}`);
        const response = await api.patch(`community/${this.communityItem.id}/comments/${id}/`, { comments }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access')}`
          }
        });
        if (response.status === 200) {
          const updatedComment = this.comments.find(c => c.id === id);
          if (updatedComment) {
            updatedComment.comments = comments;
          }
          this.showEditCommentModal = false;
          alert('댓글이 성공적으로 수정되었습니다.');
        }
      } catch (error) {
        console.error("댓글 업데이트 중 오류가 발생했습니다:", error);
        alert('댓글 업데이트 중 오류가 발생했습니다.');
      }
    },
    async deleteComment(commentId) {
      if (confirm('정말 삭제하시겠습니까?')) {
        try {
          await api.delete(`community/${this.communityItem.id}/comments/${commentId}/`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access')}`
            }
          });
          this.comments = this.comments.filter(comment => comment.id !== commentId);
          alert('댓글이 성공적으로 삭제되었습니다.');
        } catch (error) {
          console.error("댓글 삭제 중 오류가 발생했습니다:", error);
          alert('댓글 삭제 중 오류가 발생했습니다.');
        }
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
    },
    goToCommunity() {
      this.$router.push('/community/');
    },
  }
};
</script>

<style lang="scss" scoped>
.communityProfile {
  width: 70%;
  font-size: 30px;
  margin: 40px;
}

.detailButtonList {
  display: flex;
  margin: 10px;
  gap: 10px;
  justify-content: center;
}

.editDeleteButtons {
  display: flex;
  gap: 10px;
}

.detailButton {
  width: 110px;
  height: 50px;
  padding: 10px;
  font-size: 16px;
  border-radius: 10px;
  background-color: white;
  border: 0.3px solid rgba(0, 0, 0, 0.3);
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.3);
  text-decoration: none;
  color: black;
}

.communityItemTitle {
  font-size: 45px;
}

.likeRow {
  display: flex;
  justify-content: center;
}

.likeButton {
  color: #d3d3d3;
  height: 30px;
  font-size: 25px;
  text-align: center;
  border: none;
  background: none;
  cursor: pointer;
}

.likeButton.liked {
  color: #ff7171;
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

.commentsList {
  margin: 10px;
}

.commentsList>h2 {
  margin: 50px;
}

.commentBox {
  display: grid;
  justify-content: center;
}

.comment {
  display: flex;
  background-color: #EEF1F6;
  border-radius: 15px;
  margin: 15px;
  width: 600px;
  align-items: center;
  padding: 10px;
}

.commentProfileImage {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
}

.communityItemImg {
  margin-top: 30px;
  height: 300px;
  width: auto;
}

.communityItemContent {
  margin-top: 30px;
  height: auto;
  line-height: 1.7;
}

.communityListInfoContour {
  margin: 0px 8px;
  font-size: 13px;
  color: rgb(200, 200, 200)
}

.communityItemDeatil,
.likesCount {
  font-size: 15px;
  font-weight: bold;
  color: rgb(164, 164, 164);
  margin: 0;
  font-size: 14px;
}

.communityItemBox {
  margin-top: 5px;
}

.likesCount {
  color: black;
}


</style>

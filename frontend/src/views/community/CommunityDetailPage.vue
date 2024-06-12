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
          <span class="communityItemDeatil">작성일 {{ formatDate(communityItem.created_at) }}</span>
        </div>
        <div class="flex-center">
          <span class="communityItemDeatil">조회 수 {{ communityItem.view_count }}</span>
          <span class="communityListInfoContour">|</span>
          <span class="communityItemDeatil">좋아요 수 {{ likesCount }}</span>
        </div>
      </div>
    </div>
    <!-- 이미지 -->
    <div v-if="communityItem.image"><img :src="getImageUrl(communityItem.image)" alt="게시글 이미지" class="communityItemImg">
    </div>
    <!-- 내용 -->
    <span class="communityItemContent body3 flex-left">{{ communityItem.content }}</span>
    <div class="flex-between bottomBox">
      <!-- 좋아요 -->
      <div class="likeRow flex-center">
        <button class="likeButton flex-center" :class="{ liked: isLiked }" @click="toggleLike">♥</button>
        <span class="likesCount flex-center">{{ likesCount }}</span>
      </div>
      <!-- 버튼 -->
      <div class="flex-row-center">
        <button class="detailButton flex-center" @click="goToCommunity">목록으로</button>
        <div v-if="communityItem.author_id === userId" class="editDeleteButtons flex-center">
          <button class="detailButton flex-center" @click="editPost">수정하기</button>
          <button class="detailButton flex-center" @click="deletePost">삭제하기</button>
        </div>
      </div>
    </div>
    <!-- 댓글 표시 영역 -->
    <span class="commentTitle flex-left">댓글 (개수)개</span>
    <div v-if="comments && comments.length > 0" class="commentBox">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <img :src="comment.author_profile_image || defaultProfileImage" alt="프로필 이미지" class="commentProfileImage" />
        <div class="flex-row">
          <span><strong>{{ comment.author_nickname }}</strong></span>
          <span>{{ formatDate(comment.created_at) }}</span>
          <p>{{ comment.comments }}</p>
          <v-btn v-if="comment.author_id === userId" small @click="editComment(comment)">수정</v-btn>
          <v-btn v-if="comment.author_id === userId" small color="error" @click="deleteComment(comment.id)">삭제</v-btn>
        </div>
      </div>
    </div>
    <!-- 댓글 작성 -->
    <div v-if="isLoggedIn">
      <v-textarea v-model="newComment" label="댓글 작성"></v-textarea>
      <v-btn @click="addComment">댓글 달기</v-btn>
    </div>
    <div v-else>
      <span>로그인 후 댓글을 작성할 수 있습니다.</span>
    </div>
    <!-- 댓글 수정 모달 -->
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

        const likedItems = JSON.parse(localStorage.getItem('likedItems')) || {};
        this.isLiked = likedItems[this.communityItem.id] || false; // 로컬 스토리지에서 좋아요 상태 가져오기
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
    formatContent(content) {
      return content.replace(/\n/g, '<br>');
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
    toggleLike() {
      if (!this.isLoggedIn) {
        alert("로그인이 필요합니다.");
        return;
      }

      this.isLiked = !this.isLiked;
      const likedItems = JSON.parse(localStorage.getItem('likedItems')) || {};
      if (this.isLiked) {
        likedItems[this.communityItem.id] = true;
        this.likesCount += 1; // 좋아요 수 증가
      } else {
        delete likedItems[this.communityItem.id];
        this.likesCount -= 1; // 좋아요 수 감소
      }
      localStorage.setItem('likedItems', JSON.stringify(likedItems));
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
      if (!this.newComment.trim()) {
        return;
      }

      try {
        const token = localStorage.getItem('access');
        const response = await api.post(`community/${this.communityItem.id}/comments/`, {
          comments: this.newComment,
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 201) {
          this.comments.push(response.data);
          this.newComment = ''; // Clear the new comment input
        }
      } catch (error) {
        console.error("댓글을 추가하는 중 오류가 발생했습니다:", error);
        this.errorMessage = "댓글을 추가하는 중 오류가 발생했습니다.";
      }
    },
    async editComment(comment) {
      this.editCommentData = {
        id: comment.id,
        comments: comment.comments,
      };
      this.showEditCommentModal = true;
    },
    async updateComment() {
      try {
        const token = localStorage.getItem('access');
        await api.patch(`community/comments/${this.editCommentData.id}/`, {
          comments: this.editCommentData.comments,
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // Update the comment in the local comments array
        const index = this.comments.findIndex(comment => comment.id === this.editCommentData.id);
        if (index !== -1) {
          this.comments[index].comments = this.editCommentData.comments;
        }

        // Hide the edit comment modal
        this.showEditCommentModal = false;
      } catch (error) {
        console.error("댓글을 수정하는 중 오류가 발생했습니다:", error);
        this.errorMessage = "댓글을 수정하는 중 오류가 발생했습니다.";
      }
    },
    async deleteComment(commentId) {
      try {
        const token = localStorage.getItem('access');
        await api.delete(`community/comments/${commentId}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // Remove the comment from the local comments array
        this.comments = this.comments.filter(comment => comment.id !== commentId);
      } catch (error) {
        console.error("댓글을 삭제하는 중 오류가 발생했습니다:", error);
        this.errorMessage = "댓글을 삭제하는 중 오류가 발생했습니다.";
      }
    },
    async deletePost() {
      try {
        const token = localStorage.getItem('access');
        await api.delete(`community/${this.communityItem.id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        // Redirect to the community list page
        this.$router.push('/community');
      } catch (error) {
        console.error("게시글을 삭제하는 중 오류가 발생했습니다:", error);
        this.errorMessage = "게시글을 삭제하는 중 오류가 발생했습니다.";
      }
    },
    goToCommunity() {
      this.$router.push('/community');
    },
    editPost() {
      this.$router.push({ name: 'communityCreate', params: { id: this.communityItem.id } });
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

.detailButton {
  margin-left: 10px;
  width: 80px; height: 35px;
  padding: 10px;
  font-size: 14px;
  border-radius: 10px;
  background-color: white;
  border: 1px solid rgb(178, 178, 178);
  box-shadow: 0 2px 1px rgb(216, 216, 216);
  color: black;
}

.detailButton:hover {
  background-color: #f5f5f5;
}

.communityItemTitle {
  font-size: 45px;
}

.bottomBox {
  margin-top: 30px;
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
  white-space: pre-line;
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

.commentsList>span {
  margin: 50px;
}

.comment {
  display: flex;
  background-color: #EEF1F6;
  border-radius: 15px;
  width: 600px;
  align-items: center;
  padding: 20px;
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

.communityItemDeatil {
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
  margin-left: 10px;
  font-size: 15px;
  color: black;
}

.commentTitle {
  margin-top: 10%; 
}

.comment {
  width: 100%;
}
</style>

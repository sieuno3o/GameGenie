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
          <span class="communityItemDeatil">댓글 수 {{ pagination.totalCount }}</span>
        </div>
      </div>
    </div>
    <!-- 이미지 -->
    <div v-if="communityItem.image">
      <img :src="getImageUrl(communityItem.image)" alt="게시글 이미지" class="communityItemImg">
    </div>
    <!-- 내용 -->
    <span class="communityItemContent body3 flex-left" v-html="formatContent(communityItem.content)"></span>
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
    <div class="flex-row commentTopBox">
      <span class="commentTitle flex-left">댓글 {{ pagination.totalCount }}개</span>
      <!-- 페이지 네이션 버튼 -->
      <div class="pagination flex-left" v-if="pagination.totalPages > 1">
        <button v-for="page in pagination.totalPages" :key="page" :class="{ active: page === pagination.page }"
          @click="goToPage(page)" class="paginationButton flex-center">
          {{ page }}
        </button>
      </div>
    </div>
    <div v-if="comments && comments.length > 0" class="commentBox">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="flex-between" style="padding: 10px 0px;">
          <div class="flex-row-center">
            <img :src="comment.author_profile_image || defaultProfileImage" alt="프로필 이미지" class="commentProfileImage" />
            <div class="flex-col">
              <div class="flex-row-center">
                <span id="commentNickname" class="commentTextStyle body1">{{ comment.author_nickname }}</span>
                <span id="commentDate" class="commentTextStyle body1">{{ formatDate(comment.created_at) }}</span>
              </div>
              <span id="commentComments" class="commentTextStyle body1">{{ comment.comments }}</span>
            </div>
          </div>
          <div>
            <v-btn v-if="comment.author_id === userId" small @click="editComment(comment)"
              style="margin-right: 10px">수정</v-btn>
            <v-btn v-if="comment.author_id === userId" small color="error" @click="deleteComment(comment.id)">삭제</v-btn>
          </div>
        </div>
      </div>
    </div>
    <!-- 댓글 작성 -->
    <div v-if="isLoggedIn" class="flex-row commentWriteBox">
      <v-textarea v-model="newComment" label="댓글 작성" rows="1" class="commentWrite"></v-textarea>
      <v-btn @click="addComment" class="commentAdd">댓글 달기</v-btn>
    </div>
    <div v-else class="beforeLoginText">
      <span class="body3">로그인 후 댓글을 작성할 수 있습니다.</span>
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
      categories: [], // 카테고리 목록
      pagination: { // 페이지 네이션 관련 변수
        page: 1,
        pageSize: 5,
        totalPages: 1,
        totalCount: 0, // 전체 댓글 수 추가
      },
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
        this.isLiked = this.communityItem.liked_by_user; // 사용자가 좋아요를 눌렀는지 여부 설정
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
      return `http://52.79.116.122${imagePath}`;
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
        alert("로그인이 필요합니다.");
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
          this.isLiked = response.data.liked;
        } else {
          console.error("Invalid response data", response.data);
        }
      } catch (error) {
        console.error("좋아요 처리 중 오류가 발생했습니다:", error);
      }
    },
    async fetchComments(id, page = 1) {
      try {
        const response = await api.get(`community/${id}/comments/`, {
          params: {
            page: page,
          },
        });
        this.comments = response.data.results;
        this.pagination.page = page;
        this.pagination.totalPages = Math.ceil(response.data.count / this.pagination.pageSize);
        this.pagination.totalCount = response.data.count; // 전체 댓글 수 설정
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
        await this.fetchComments(id, this.pagination.page);  // 현재 페이지의 댓글 목록을 다시 가져옴
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
    editPost() {
      this.$router.push({ name: 'communityCreate', params: { id: this.communityItem.id } });
    },
    async goToPage(page) {
      const id = this.$route.params.id;
      await this.fetchComments(id, page);
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
  width: 80px;
  height: 35px;
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

.comment {
  width: 600px;
  align-items: center;
  margin: 20px 0;
  width: 100%;
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

.commentTopBox {
  margin-top: 10%;
  height: 45px;
}

.beforeLoginText {
  padding: 10px;
}

#commentNickname {
  font-weight: bold;
}

#commentDate {
  color: rgb(164, 164, 164);
  margin-left: 10px;
  font-size: 14px;
}

#commentComments {
  margin-top: 5px;
}

.commentWrite {
  margin-right: 20px;
}

.commentAdd {
  height: 56px;
}

.pagination {
  height: auto;
  margin-left: 25px;
  background: white;
  font-size: 16px;
  box-shadow: 0 2px 1px rgb(216, 216, 216);
  border: 1px solid rgb(216, 216, 216);
  border-radius: 10px;
}

.pagination button {
  height: 42px;
  padding: 15px;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  color: #9a9a9a;
}

.pagination button.active {
  font-weight: bolder;
  color: black;
}
</style>

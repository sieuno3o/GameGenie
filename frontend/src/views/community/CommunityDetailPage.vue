<template>
  <div class="communityProfile">
    <div v-if="communityItem">
      <h1>{{ communityItem.title }}</h1>
      <p>작성자: {{ communityItem.author }}</p>
      <img :src="communityItem.image" alt="Community Image">
      <div class="content">{{ communityItem.content }}</div>
      <div class="actions">
        <button @click="goBack">목록으로</button>
        <button v-if="isAuthor" @click="editPost">수정하기</button>
        <button v-if="isAuthor" @click="deletePost">삭제하기</button>
      </div>
      <div class="like-section">
        <span @click="toggleLike">❤️ {{ communityItem.likes }}</span>
      </div>
      <div class="comments-section">
        <h2>댓글</h2>
        <div v-for="comment in communityItem.comments" :key="comment.id" class="comment">
          <img :src="comment.user.avatar" alt="User Avatar">
          <p>{{ comment.user.username }}: {{ comment.content }}</p>
          <span @click="toggleCommentLike(comment.id)">❤️ {{ comment.likes }}</span>
        </div>
        <div v-if="isLoggedIn" class="add-comment">
          <textarea v-model="newComment" placeholder="댓글을 입력하세요..."></textarea>
          <button @click="addComment">댓글 작성</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api';  
import accountsAPI from '@/accountsAPI';  

export default {
  data() {
    return {
      communityItem: null,
      isLoggedIn: false,
      userId: '',
      isAuthor: false,
      newComment: '',
    };
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchCommunityItem(id);
    this.checkLoginStatus();
  },
  methods: {
    async fetchCommunityItem(id) {
      try {
        const response = await api.get(`community/${id}/`);
        this.communityItem = response.data;
        this.isAuthor = this.communityItem.author === this.userId;
      } catch (error) {
        console.error("게시글을 가져오는 중 오류가 발생했습니다:", error);
      }
    },
    async checkLoginStatus() {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          const response = await accountsAPI.get('profile/', {
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
      const id = this.$route.params.id;
      try {
        const response = await api.post(`community/${id}/like/`);
        this.communityItem.likes = response.data.likes;
      } catch (error) {
        console.error("좋아요 처리 중 오류가 발생했습니다:", error);
      }
    },
    async toggleCommentLike(commentId) {
      try {
        const response = await api.post(`community/comments/${commentId}/like/`);
        const comment = this.communityItem.comments.find(comment => comment.id === commentId);
        if (comment) {
          comment.likes = response.data.likes;
        }
      } catch (error) {
        console.error("댓글 좋아요 처리 중 오류가 발생했습니다:", error);
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
    editPost() {
      // 수정하기 기능 구현
    },
    deletePost() {
      // 삭제하기 기능 구현
    }
  }
};
</script>

<style>
.communityProfile {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}
h1 {
  font-size: 2em;
  margin-bottom: 10px;
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

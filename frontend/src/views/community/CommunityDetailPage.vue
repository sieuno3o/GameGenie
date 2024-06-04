<template>
  <div class="communityProfile" v-if="communityItem">
    <h1>{{ communityItem.title }}</h1>
    <h3>카테고리 : {{ communityItem.category }}</h3>
    <h3>작성 일 : {{ formatDate(communityItem.created_at) }}</h3>
    <p>작성자 : {{ communityItem.author }}</p>
    <div>{{ communityItem.image }}</div>
    <p>{{ communityItem.content }}</p>
    <div class="detailButtonList">
      <router-link to="/community/">
        <button class="detailButton">목록으로</button>
      </router-link>
      <button class="detailButton">수정하기</button>
      <button class="detailButton" style="background-color: #FF9393;">삭제하기</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import api from '../../api';
import accountsAPI from '../../accountsAPI';

export default {
  data() {
    return {
      communityItem: null,
      authorName: '알 수 없음',
    };
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchCommunityItem(id);
  },
  methods: {
    async fetchCommunityItem(id) {
      try {
        const response = await api.get(`community/${id}/`);
        this.communityItem = response.data;
        const user = await accountsAPI.getUser();
        this.author = user.username;
      } catch (error) {
        console.error("게시글을 가져오는 중 오류가 발생했습니다 :", error);
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
    async deleteCommunity() {
      const id = this.$route.params.id;
      try {
        const response = await axios.delete(`/api/community/${id}/`);
        alert(response.data.message);
        this.$router.push('/community');
      } catch (error) {
        console.error('삭제 오류:', error.response.data);
        alert('삭제 중 오류가 발생했습니다.');
      }
    },
  },
};
</script>

<style>
.communityProfile {
  width: 100%;
  height: 100px;
  font-size: 30px;
  margin: 40px;
  text-align: center;
}

.detailButtonList {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.detailButton {
  border-radius: 10px;
  padding: 10px;
  font-size: 16px;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.3);
  text-decoration: none;
  color: black;
}
</style>
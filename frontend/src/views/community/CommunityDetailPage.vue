<template>
  <div class="communityProfile" v-if="communityItem">
    <h1>게시글 상세 페이지</h1>
    <h1>{{ communityItem.title }}</h1>
    <p>작성자: {{ communityItem.author }}</p>
    <p>{{ communityItem.content }}</p>
  </div>
</template>

<script>
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
</style>
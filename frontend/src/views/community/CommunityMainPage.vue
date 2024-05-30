<template>
  <div class="community flex-col">
    <span class="communityTitle heading1 flex-center">커뮤니티</span>
    <img class="banner" src="" alt="배너 사진">
    <div class="communityMain">
      <div class="communityRow1">
        <div class="categoryButton">
          <div class="categorylist">
            <img class="hamburgericon" src="../../assets/image/community/hamburger.png" alt="카테고리" />
          </div>
          <div class="categorySelected">
            <h3 class="subtitle">액션</h3>
          </div>
          <div class="categorySortButton">
            <h3 class="subtitle">시간순</h3>
            <img class="image1" src="../../assets/image/community/dropdown.png" width="20px;" height="20px;">
          </div>
        </div>
      </div>
      <div class="communityRow2">
        <input type="text" v-model="query" @input="fetchSuggestions" @keyup.enter="searchGames"
          class="mainSearchInput body1" placeholder="게임 이름 또는 장르 검색" />
        <div class="communityCreate">
          <router-link to="/communityCreate">
            <span class="Create">글 작성</span>
          </router-link>
        </div>
      </div>
      <div>
        <ul>
          <li v-for="item in filteredCommunityList" :key="item?.id">
            {{ item?.name }}
          </li>
        </ul>
        <p v-if="!filteredCommunityList.length">There are no posts in the community.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api';

export default {
  data() {
    return {
      communityList: [],
    };
  },
  computed: {
    filteredCommunityList() {
      // null 또는 undefined 항목을 필터링
      return this.communityList.filter(item => item && item.id);
    }
  },
  created() {
    this.fetchCommunityList();
  },
  methods: {
    async fetchCommunityList() {
      try {
        const response = await api.get('posts/');
        // null 값이나 잘못된 항목이 없는지 확인
        this.communityList = response.data.filter(item => item && item.id);
      } catch (error) {
        console.error("There was an error fetching the community list:", error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>

.community {
  align-items: center;
  min-height: 100vh;
  width: 100%;
}

.communityTitle {
  width: 100%;
  height: 100px;
  font-size: 30px;
}

.banner {
  position: relative;
  width: 100%;
  top: 10px;
  background-color: lightgray;
}

.communityRow1 {
  position: relative;
  display: flex;
  gap: 0px 14px;
  margin: 12px;
}

.communityRow2 {
  display: flex;
}

.categorylist {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 40px;
  border-radius: 10px;
  background-color: beige;
}

.categoryButton {
  display: flex;
  align-items: center;
  gap: 30px;
}

.subtitle {
  font-size: 16px;
}

.categorySortButton {
  display: flex;
}

.hamburgericon {
  width: 25px;
  height: 25px;
}
</style>

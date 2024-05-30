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
          <router-link to="/community/Create">
            <a>글 작성</a>
          </router-link>
        </div>
      </div>
      <div>
        <ul class="communityList">
          <li class="community" v-for="item in filteredCommunityList" :key="item.id">
            {{ item.title }}, 작성자: {{ item.author }}
          </li>
        </ul>
        <p v-if="!filteredCommunityList.length">커뮤니티에 게시물이 없습니다.</p>
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
      query: '',
    };
  },
  computed: {
    filteredCommunityList() {
      // null 또는 undefined 항목을 필터링하고, 각 항목에서 id와 author만 포함하는 객체를 생성
      return this.communityList
        .filter(item => item && item.id)
        .slice(0, 10);
    }
  },
  created() {
    this.fetchCommunityList();
  },
  methods: {
    async fetchCommunityList() {
      try {
        const response = await api.get('community/');
        // API에서 받은 데이터의 'results' 배열을 communityList에 저장
        this.communityList = response.data.results;
      } catch (error) {
        console.error("There was an error fetching the community list:", error);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.communityList{
  list-style:none;
}

.community {
  align-items: center;
  height: 40px;
  width: 100%;
}

.communityTitle {
  width: 100%;
  height: 100px;
  font-size: 30px;
  margin: 40px;
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
  margin: 20px;
}

.communityCreate{
  padding: 10px;
  width: 80px;
  height: 40px;
  text-align: center;
  border-radius: 10px;
  background-color: beige;
}
.communityCreate > a {
  text-decoration: none;
  color: black;
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
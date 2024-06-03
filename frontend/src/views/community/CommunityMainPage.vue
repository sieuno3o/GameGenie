<template>
  <div class="community flex-col">
    <span class="communityTitle heading1 flex-center">커뮤니티</span>
    <img class="banner" src="" alt="배너 사진">
    <div class="communityMain">
      <div class="communityRow1">
        <div class="categoryButton">
          <div class="categorylist">
            <img class="hamburgericon" src="../../assets/image/community/hamburger.png" alt="카테고리" @click="toggleDropdown" />
            <ul v-if="showDropdown" class="category-dropdown">
              <li v-for="category in categories" :key="category.key" @click="selectCategory(category)">{{ category.value }}</li>
            </ul>
          </div>
          <div class="categorySelected">
            <h3 class="subtitle">{{ selectedCategoryName }}</h3>
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
          <li 
            class="community" 
            v-for="item in filteredCommunityList" 
            :key="item.id"
            @click="goToDetail(item.id)">
            {{ item.title }}, 작성자: {{ item.author }}
          </li>
        </ul>
        <p v-if="!filteredCommunityList.length">커뮤니티에 게시물이 없습니다.</p>
      </div>
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
      communityList: [],
      accountsUsers: [],
      showDropdown: false,
      categories: [],
      query: '',
      selectedCategoryName: '카테고리를 선택하세요',
    };
  },
  computed: {
    filteredCommunityList() {
      return this.communityList
        .filter(item => item && item.id)
        .slice(0, 10)
        .map(item => {
          const user = this.accountsUsers.find(user => user.id === item.author);
          const username = user ? user.username : '알 수 없음';
          return { ...item, author: username };
        });
    }
  },
  created() {
    this.fetchCommunityList();
    this.fetchAccountsUsers();
    this.fetchCategories();
  },
  methods: {
    async fetchCommunityList() {
      try {
        const response = await api.get('community/');
        this.communityList = response.data.results;
      } catch (error) {
        console.error("커뮤니티 목록을 가져오는 중 오류가 발생했습니다 :", error);
      }
    },
    async fetchAccountsUsers() {
      try {
        this.accountsUsers = await accountsAPI.getUsers();
      } catch (error) {
        console.error("유저 정보를 가져오는 중 오류가 발생했습니다 :", error);
      }
    },
    goToDetail(id) {
      this.$router.push({ name: 'communityDetail', params: { id } });
    },
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    fetchCategories() {
      axios.get('http://localhost:8000/api/community/categories/')
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error('카테고리를 불러오는 중 오류가 발생했습니다:', error);
        });
    },
    selectCategory(category) {
    this.selectedCategoryName = category.value;
    this.showDropdown = false;
    console.log('선택한 카테고리:', category);
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

.communitys {
  display: flex;
  align-items: center;
  height: 40px;
  width: 100%;
  margin: 10px;
}

.communitys:hover {
  background-color: lightgray
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

.category-dropdown {
  position: absolute;
  background-color: #f9f9f9;
  opacity: 0.9;
  padding: 10px;
  list-style-type: none;
  border: 1px solid #ccc;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  transform: translateY(55%);
}

.category-dropdown li {
  padding: 5px 0;
  width: 100px;
  margin: 10px;
  text-align: center;
  align-content: center;
  cursor: pointer;
}

.category-dropdown li:hover {
  background-color: #e0e0e0;
}
</style>
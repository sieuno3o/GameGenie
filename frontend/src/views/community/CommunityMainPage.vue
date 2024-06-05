<template>
  <div class="community flex-col">
    <span class="communityTitle heading1 flex-center">커뮤니티</span>
    <img class="banner" src="" alt="배너 사진">
    <div class="communityMain">
      <div class="communityRow1">
        <div class="categoryButton">
          <div class="categorylist">
            <img class="hamburgericon" src="../../assets/image/community/hamburger.png" alt="카테고리"
              @click="toggleDropdown" />
            <ul v-if="showDropdown" class="categoryDropdown">
              <li v-for="category in categories" :key="category.key" @click="selectCategory(category)">{{ category.value
              }}</li>
            </ul>
          </div>
          <div class="categorySelected">
            <h3 class="subtitle">{{ selectedCategoryName }}</h3>
          </div>
          <div class="categorySortButton" @click="toggleSortDropdown">
            <h3 class="subtitle">{{ sortOption === 'time' ? '최신 순' : sortOption === 'oldest' ? '오래된 순' : '좋아요 순' }}</h3>
            <img class="image1" src="../../assets/image/community/dropdown.png" width="20px;" height="20px;">
            <div v-if="showSortDropdown" class="sortDropdown">
              <p @click="selectSortOption('time')">최신 순</p>
              <p @click="selectSortOption('oldest')">오래된 순</p>
              <p @click="selectSortOption('likes')">좋아요 순</p>
            </div>
          </div>
        </div>
      </div>
      <div class="communityRow2">
        <input type="text" v-model="query" class="mainSearchInput body1" placeholder="게임 이름 또는 장르 검색" />
        <div class="communityCreate">
          <a @click.prevent="checkLogin">글 작성</a>
        </div>
      </div>
      <div>
        <ul class="communityList">
          <li class="communitys" v-for="item in sortedAndFilteredCommunityList" :key="item.id" @click="goToDetail(item.id)">
            {{ item.title }}, 작성자: {{ item.author }}, 좋아요: {{ item.community_like.length }}
          </li>
        </ul>
        <p v-if="!sortedAndFilteredCommunityList.length">커뮤니티에 게시물이 없습니다.</p>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">이전</button>
          <button v-for="page in totalPages" :key="page" @click="goToPage(page)"
            :class="{ active: currentPage === page }">{{ page }}</button>
          <button @click="nextPage" :disabled="currentPage === totalPages">다음</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api';
import accountsAPI from '../../accountsAPI';

export default {
  data() {
    return {
      communityList: [],
      accountsUsers: [],
      likedCommunities: [],
      categories: [],
      showDropdown: false,
      query: '',
      selectedCategory: 'all',
      selectedCategoryName: '카테고리를 선택하세요',
      showSortDropdown: false,
      sortOption: 'time',
      currentPage: 1,
      totalPages: 0,
      pageSize: 10,
    };
  },
  computed: {
    sortedAndFilteredCommunityList() {
      let filteredList = [...this.communityList];

      if (this.query) {
        filteredList = filteredList.filter(item =>
          item.title.toLowerCase().includes(this.query.toLowerCase())
        );
      }

      if (this.selectedCategory !== 'all') {
        filteredList = filteredList.filter(item => item.category === this.selectedCategory);
      }

      filteredList = filteredList.filter(item => item && item.id)
        .map(item => {
          const user = this.accountsUsers.find(user => user.id === item.author);
          const username = user ? user.username : '알 수 없음';
          return { ...item, author: username };
        });

      if (this.sortOption === 'time') {
        filteredList.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      } else if (this.sortOption === 'oldest') {
        filteredList.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
      } else if (this.sortOption === 'likes') {
        filteredList.sort((a, b) => b.community_like.length - a.community_like.length);
      }

      return filteredList;
    },
    currentPageCommunities() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.communityList.slice(start, end)
    },
  },
  created() {
    this.fetchCommunityList();
    this.fetchAccountsUsers();
    this.fetchCategories();
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    },
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 1)
      this.fetchCommunityList()
    },
    nextPage() {
      this.currentPage = Math.min(this.currentPage + 1, this.totalPages)
      this.fetchCommunityList()
    },
    goToPage(page) {
      this.currentPage = page
      this.fetchCommunityList()
    },
    async fetchCommunityList() {
      api.get(`community/?page=${this.currentPage}`)
        .then(response => {
          this.communityList = response.data.results
          this.totalPages = Math.ceil(response.data.count / this.pageSize)
        })
        .catch(error => {
          console.error('커뮤니티 목록을 가져오는 중 오류가 발생했습니다: ', error)
        })
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
      api.get('community/categories/')
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error('카테고리를 불러오는 중 오류가 발생했습니다:', error);
        });
    },
    selectCategory(category) {
      this.selectedCategory = category.key;
      this.selectedCategoryName = category.value;
      this.showDropdown = false;
      console.log('선택한 카테고리:', category);
    },
    toggleSortDropdown() {
      this.showSortDropdown = !this.showSortDropdown;
    },
    selectSortOption(option) {
    this.sortOption = option;
    this.showSortDropdown = false;
    },
    checkLogin() {
      if (!localStorage.getItem('access')) {
        alert('로그인이 필요합니다. 로그인 페이지로 이동합니다.');
        this.$router.push({ name: 'login' });
      } else {
        this.$router.push({ name: 'communityCreate' });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.communityList {
  list-style: none;
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
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
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

.communityCreate {
  padding: 10px;
  width: 80px;
  height: 40px;
  text-align: center;
  border-radius: 10px;
  background-color: beige;
  cursor : pointer;
}

.communityCreate>a {
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
  cursor: pointer;
}

.hamburgericon {
  width: 25px;
  height: 25px;
}

.categoryDropdown {
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

.categoryDropdown li {
  padding: 5px 0;
  width: 100px;
  margin: 10px;
  text-align: center;
  align-content: center;
  cursor: pointer;
}

.categoryDropdown li:hover {
  background-color: #e0e0e0;
}

.sortDropdown {
  display: block;
  position: absolute;
  right: -100px;
  background-color: #f9f9f9;
  min-width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.sortDropdown p {
  color: black;
  margin: 10px;
  text-decoration: none;
  display: block;
  cursor: pointer;
}

.sortDropdown p:hover {
  background-color: #f1f1f1
}

.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.pagination button {
  margin: 10px;
}

.pagination .active {
  font-weight: bold;
}
</style>

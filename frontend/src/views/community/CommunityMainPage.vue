<template>
  <div class="community flex-col">
    <!-- <img class="banner" src="" alt="배너 사진"> -->
    <div class="communityMain">
      <div class="communityRow1 flex-between">
        <!-- 카테고리 -->
        <div class="categoryButton flex-row-center">
          <div class="categorylist flex-row-center">
            <img class="hamburgericon" src="../../assets/image/community/hamburger.png" alt="카테고리"
              @click="toggleDropdown" />
            <ul v-if="showDropdown" class="categoryDropdown">
              <li v-for="category in categories" :key="category.key" @click="selectCategory(category)">{{ category.value
                }}</li>
            </ul>
          </div>
          <div class="categorySelected">
            <span class="subtitle body3">{{ selectedCategoryName }}</span>
          </div>
        </div>
        <div class="flex-row-center">
          <!-- 정렬 -->
          <div class="categorySortButton flex-row-center" @click="toggleSortDropdown">
            <span class="subtitle body3">{{ sortOption === 'time' ? '최신 순' : sortOption === 'oldest' ? '오래된 순' : '좋아요 순'
              }}</span>
            <img class="image1" src="../../assets/image/community/dropdown.png" width="20px;" height="20px;">
            <div v-if="showSortDropdown" class="sortDropdown">
              <p @click="selectSortOption('time')">최신 순</p>
              <p @click="selectSortOption('oldest')">오래된 순</p>
              <p @click="selectSortOption('likes')">좋아요 순</p>
            </div>
          </div>
          <!-- 글 작성 버튼 -->
          <div class="communityCreate flex-row-center body3" @click.prevent="checkLogin">글 작성</div>
        </div>
      </div>
      <!-- 검색 -->
      <div class="communityRow2">
        <input type="text" v-model="query" class="communitySearch" placeholder="게임 이름 또는 장르 검색" />
      </div>
      <!-- 게시물 목록 -->
      <div class="communityList">
        <ul>
          <li class="communitys flex-left" v-for="item in sortedAndFilteredCommunityList" :key="item.id"
            @click="goToDetail(item.id)">
            {{ item.title }}, 작성자: {{ item.author_nickname }}, 좋아요: {{ item.community_like.length }}
          </li>
        </ul>
        <span v-if="!sortedAndFilteredCommunityList.length">커뮤니티에 게시물이 없습니다.</span>
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
        filteredList = filteredList.filter(item => item.title.toLowerCase().includes(this.query.toLowerCase()));
      }

      if (this.selectedCategory !== 'all') {
        filteredList = filteredList.filter(item => item.category === this.selectedCategory);
      }

      filteredList = filteredList.map(item => {
        const user = this.accountsUsers.find(user => user.id === item.author);
        const author_nickname = user ? user.nickname : '알 수 없음';
        return { ...item, author_nickname };
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
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.sortedAndFilteredCommunityList.slice(start, end);
    },
  },
  mounted() {
    this.fetchAccountsUsers();
    this.fetchCommunityList();
    this.fetchCategories();
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    },
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 1);
      this.fetchCommunityList();
    },
    nextPage() {
      this.currentPage = Math.min(this.currentPage + 1, this.totalPages);
      this.fetchCommunityList();
    },
    goToPage(page) {
      this.currentPage = page;
      this.fetchCommunityList();
    },
    async fetchCommunityList() {
      api.get(`community/?page=${this.currentPage}`)
        .then(response => {
          this.communityList = response.data.results;
          this.totalPages = Math.ceil(response.data.count / this.pageSize);
        })
        .catch(error => {
          console.error('커뮤니티 목록을 가져오는 중 오류가 발생했습니다: ', error);
        });
    },
    async fetchAccountsUsers() {
      try {
        const response = await api.get('/accounts/users/');
        this.accountsUsers = response.data;
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
ul {
  list-style: none;
  padding: 0;
}

.communityList {
  margin-top: 5px;
  padding: 5px;
}

.community {
  height: auto;
  width: 650px;
  min-width: 400px;
}

.communitys {
  height: 40px;
  width: 100%;
  padding: 23px 15px;
  cursor: pointer;
}

.communitys:hover {
  background-color: $HOVER-COLOR;
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

.categorySelected {
  margin-left: -30px;
}

.communityRow1 {
  margin-top: 40px;
  width: 100%;
}

.communityRow2 {
  margin: 15px 0px 0px 12px;
}

.communityCreate {
  margin-left: 20px; 
  padding: 5px 8px;
  border-radius: 5px;
  cursor: pointer;
  border: 1px solid rgb(178, 178, 178);
  box-shadow: none;
  color: #000;
  background-color: $MAIN-COLOR-SKYBLUE;
}

.communityCreate:hover {
  background-color: $HOVER-COLOR;
}

.categorylist {
  width: 50px;
  height: 40px;
  border-radius: 10px;
}

.categoryButton {
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
  background-color: #f1f1f1;
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

.communitySearch {
  background-color: #ffffff;
  height: 35px;
  width: 100%;
  padding: 5px;
  padding-bottom: 10px;
  border: none;
  border-bottom: 1px solid rgb(178, 178, 178);
  outline: none;
}

.communitySearch:focus {
  border-bottom: 1px solid rgb(178, 178, 178);
}
</style>

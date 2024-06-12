<template>
  <div class="backgroundMain">
    <div class="box"></div>
    <img src="../assets/image/logo.png" class="mainLogoImg">
    <div class="flex-col-center">
      <div :class="{ 'mainSearchbar': true, 'active': suggestions.length > 0 }" class="flex-left mainSearchbar">
        <img src="../assets/image/searchIcon.png" class="searchIcon" @click="searchGames">
        <input type="text" v-model="query" @input="fetchSuggestions" @keyup.enter="searchGames"
          class="mainSearchInput body1" placeholder="검색어를 입력하세요" />
      </div>
      <ul v-if="suggestions.length > 0" class="suggestions-list body1">
        <li v-for="suggestion in suggestions" :key="suggestion.key" @click="selectSuggestion(suggestion)">
          {{ suggestion.value }}
        </li>
      </ul>
    </div>

    <!-- HTTPS 알림 모달 -->
    <v-dialog v-model="showHttpsModal" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">보안 경고</span>
        </v-card-title>
        <v-card-text>
          <p>개발단계라 https 사용이 어렵습니다. http로 접속해주세요.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showHttpsModal = false">확인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 사용법 안내 모달 -->
    <v-dialog v-model="showGuideModal" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">게임 추천 기능 사용법</span>
        </v-card-title>
        <v-card-text>
          <p>검색어를 입력하고 엔터 키를 누르거나 검색 아이콘을 클릭하여 게임을 추천받으세요.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showGuideModal = false">확인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '../api'; // `api.js`에서 가져온 인스턴스 사용
import { mapState } from 'vuex';

export default {
  data() {
    return {
      query: "",
      suggestions: [],
      showHttpsModal: false,
      showGuideModal: false
    };
  },
  computed: {
    ...mapState(['user']),
  },
  methods: {
    fetchSuggestions() {
      if (this.query.trim() === "") {
        this.suggestions = [];
        return;
      }
      api
        .get(`community/categories/?query=${this.query}`)
        .then((response) => {
          this.suggestions = response.data.filter(item =>
            item.value.toLowerCase().includes(this.query.toLowerCase())
          ).map(item => ({
            key: item.key,
            value: item.value
          }));
        })
        .catch((error) => {
          console.error("Error fetching suggestions:", error);
        });
    },
    selectSuggestion(suggestion) {
      this.query = suggestion.value;
      this.suggestions = [];
    },
    searchGames() {
      if (this.query.trim() !== "") {
        this.$router.push({ path: '/recommendations', query: { user_input: this.query } });
      }
    },
    checkHttps() {
      if (window.location.protocol === 'https:') {
        this.showHttpsModal = true;
      }
    },
    showGuide() {
      if (!localStorage.getItem('guideShown')) {
        this.showGuideModal = true;
        localStorage.setItem('guideShown', 'true');
      }
    }
  },
  created() {
    this.checkHttps();
    this.showGuide();
  }
};
</script>

<style lang="scss" scoped>
.backgroundMain {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mainLogoImg {
  width: 480px;
}

.mainSearchbar {
  margin-top: 30px;
  background-color: white;
  width: 800px;
  height: 80px;
  border-radius: 90px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding-left: 30px;
  display: flex;
  align-items: center;
}

.mainSearchbar.active {
  border-radius: 45px 45px 0 0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.mainSearchInput {
  border: 0;
  outline: none;
  width: 80%;
  height: 100%;
  padding-left: 20px;
}

.searchIcon {
  width: 20px;
  cursor: pointer;
}

.suggestions-list {
  margin: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  background-color: white;
  border-radius: 0 0 45px 45px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: -5px;
}

.suggestions-list li {
  padding: 15px;
  cursor: pointer;
}

.suggestions-list li:hover {
  background-color: #f0f0f0;
}
</style>

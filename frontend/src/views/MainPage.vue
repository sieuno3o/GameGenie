<template>
  <div class="backgroundMain flex-col-center">
    <img src="../assets/image/logo2.png" class="mainLogoImg">
    <div class="mainSearchbar flex-left" id="mainSearchbar">
      <img src="../assets/image/searchIcon.png" class="searchIcon">
      <input type="text" v-model="query" @input="fetchSuggestions" placeholder="검색어를 입력하세요" />
      <ul v-if="suggestions.length > 0" class="suggestions-list">
        <li v-for="suggestion in suggestions" :key="suggestion.key" @click="selectSuggestion(suggestion)">
          {{ suggestion.value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      query: "",
      suggestions: [],
    };
  },
  methods: {
    fetchSuggestions() {
      if (this.query.trim() === "") {
        this.suggestions = [];
        return;
      }

      axios
        .get(`http://localhost:8000/api/community/categories/?query=${this.query}`)
        .then((response) => {
          console.log(response.data); // 응답 데이터 로그 출력
          this.suggestions = response.data.map(item => ({
            key: item.key,
            value: item.value
          }));
        })
        .catch((error) => {
          console.error("Error fetching suggestions:", error);
        });
    },
    selectSuggestion(suggestion) {
      this.query = suggestion.value; // 선택된 suggestion의 value를 query로 설정
      this.suggestions = [];
    },
  },
};
</script>

<style lang="scss" scoped>
.backgroundMain {
  width: 100vw;
  height: 100vh;
  background-color: $MAIN-COLOR-SKYBLUE;
}

.mainLogoImg {
  margin-top: -200px;
  width: 480px;
}

.mainSearchbar {
  margin-top: 30px;
  background-color: white;
  width: 800px; height: 80px;
  border-radius: 90px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding-left: 30px;
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
}

#mainSearchbar {
  position: relative;
}

input {
  width: 100%;
  padding: 10px;
  border:none;
}

.suggestions-list {
  position: absolute;
  top: 80px;
  width: 100%;
  border-top: none;
  background-color: white;
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  padding: 10px;
  cursor: pointer;
}

.suggestions-list li:hover {
  background-color: white;
}
</style>

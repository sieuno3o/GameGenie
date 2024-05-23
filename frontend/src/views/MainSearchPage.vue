<template>
  <div class="backgroundMain">
    <div class="box"></div>
    <img src="../assets/image/logo.png" class="mainLogoImg">
    <div class="flex-col-center">
      <div :class="{ 'mainSearchbar': true, 'active': suggestions.length > 0 }" class="flex-left mainSearchbar">
        <img src="../assets/image/searchIcon.png" class="searchIcon">
        <input type="text" v-model="query" @input="fetchSuggestions" class="mainSearchInput body1"
          placeholder="검색어를 입력하세요" />
      </div>
      <ul v-if="suggestions.length > 0" class="suggestions-list body1">
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
        .get('http://localhost:8000/api/community/categories/?query=${this.query}')
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
  },
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
  background-color: white;
}
</style>

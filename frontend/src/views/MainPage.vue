<template>
  <div class="backgroundMain flex-col-center">
    <img src="../assets/image/logo2.png" class="mainLogoImg">
    <div class="mainSearchbar flex-left">
      <img src="../assets/image/searchIcon.png" class="searchIcon" @click="search">
      <input 
        type="text" 
        class="mainSearchInput body1" 
        placeholder="장르 또는 게임 이름 검색"
        v-model="searchQuery"
        @keyup.enter="search"
      >
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    search() {
      if (this.searchQuery.trim()) {
        this.$router.push({ 
          name: 'recommendations', 
          query: { user_input: this.searchQuery }
        });
      }
    }
  }
}
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
  width: 800px; 
  height: 80px;
  border-radius: 90px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding-left: 30px;
  display: flex;
  align-items: center;
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
</style>

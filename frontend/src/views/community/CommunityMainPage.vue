<template>
  <div class="community">
    <div class="communityTitle">
      <h1>커뮤니티</h1>
    </div>
    <img class="banner" src="">
    <div class="communityMain">
      <div class="communityRow1">
        <div class="categoryButton">
          <div class="categorylist">
            <img class="hamburgericon" src="../../assets/image/community/hamburger.png" alt="카테고리"/>
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
        <input type="text" v-model="query" @input="fetchSuggestions" @keyup.enter="searchGames" class="mainSearchInput body1"
          placeholder="게임 이름 또는 장르 검색"/>
        <div class="communityCreate">
          <router-link to="/communityCreate">
            <span class="communityCreate">로그인</span>
          </router-link>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
.communityTitle {
  background-color: beige;
  width: 100%;
  height: 100px;
  text-align: center;
  align-content: center;
}
.banner {
  position: relative;
  width: 100%;
  height: 100px;
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

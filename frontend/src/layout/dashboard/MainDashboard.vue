<template>
  <div class="flex-center" :class="{ 'main-page': isMainPage }" id="contents-wrapper">
    <div class="flex-row-around" id="contents">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    isMainPage() {
      return this.$route.name === 'main';
    }
  }
};
</script>

<style lang="scss" scoped>
#contents {
  background-color: $MAIN-COLOR-SKYBLUE;
  min-height: calc(100vh - 55px);
}

#contents-wrapper {
  background-color: $MAIN-COLOR-SKYBLUE;
}

.main-page #contents {
  margin-top: 150px;
}
</style>

<template>
  <div class="flex-center" id="contents-wrapper">
    <div class="flex-row-around" id="contents">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: "DefaultDashboard",
  components: {},
};
</script>

<style lang="scss" scoped>
#contents {
  max-width: 1920px;
  min-height: calc(100vh - 55px);
  margin-top: 150px;
}

#contents-wrapper {
  background-color: $MAIN-COLOR-SKYBLUE;
}
</style>

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
  min-height: calc(100vh - 130px - 70px);
  margin-top: 135px
}

#contents-wrapper {
  background-color: $MAIN-COLOR-SKYBLUE;
}
</style>

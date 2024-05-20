<template>
  <div class="flex-center" id="contents-wrapper">
    <div class="flex-row-around" id="contents">
      <div class="contents-edge"></div>
      <div id="contents-body">
        <router-view></router-view>
      </div>
      <div class="contents-edge"></div>
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
  padding-top: 60px;
  max-width: 1920px;
  min-height: calc(100vh - 130px - 70px);
}

#contents-body {
  max-width: 1260px;
}

.contents-edge {
  max-width: 330px;
  padding: 80px 64px 0 64px;
}
</style>

<template>
  <div class="flex-row-around" id="contents">
    <router-view></router-view>
  </div>
</template>

<script>
</script>

<style lang="scss" scoped>
#contents {
  max-width: 1920px;
  min-height: calc(100vh - 55px);
}
</style>

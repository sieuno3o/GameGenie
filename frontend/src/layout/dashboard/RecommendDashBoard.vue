<template>
    <div class="flex-row-around" id="contents">
      <router-view></router-view>
    </div>
</template>

<script>
</script>

<style lang="scss" scoped>
#contents {
  background-color: $MAIN-COLOR-SKYBLUE;
  min-height: calc(100vh - 55px);
}
</style>

<template>
  <div class="log-wrapper">
    <log />
  </div>
</template>
<script>
import log from "@/components/log.vue";

export default {
  components: {
    log,
  },
  setup() {},
};
</script>
<style scoped>
.log-wrapper {
  position: absolute; 
  top: 0;
  left: 0;
  width: 100vw; 
  height: 100vh; 
  min-width: 100%; 
  min-height: 100%; 
  display: flex;
  justify-content: center; 
  align-items: center; 
}
</style>

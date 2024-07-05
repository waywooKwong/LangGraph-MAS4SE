<template>
  <div class="log-wrapper">
    <log />
  </div>
</template>
<script>
import log from "@/components/log.vue"
import { onMounted } from "vue"

export default {
  components: {
    log,
  },
  setup() {
    // 设置图标
    onMounted(() => {
      setFavicon("/icons/favicon-log.ico")
    })
  },
}
function setFavicon(href) {
  let link =
    document.querySelector("link[rel*='icon']") ||
    document.createElement("link")
  link.type = "image/x-icon"
  link.rel = "shortcut icon"
  link.href = href
  document.getElementsByTagName("head")[0].appendChild(link)
}
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

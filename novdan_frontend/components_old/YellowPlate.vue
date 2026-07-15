<template>
  <div class="yellow-plate">
    {{ text }}
    <div v-for="i in 2" :key="i" class="yellow-plate-layer" :style="`${bg}: ${i*2}px; left: ${i*2}px; z-index:${-1*i}`" />
  </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: ''
    },
    bg: {
      type: String,
      default: 'top'
    }
  },
  data () {
    return {
      tilted: 0
    }
  }
}
</script>

<style scoped lang="scss">
.yellow-plate-layer {
  position: absolute;
  background-color: #ffd700;
  border: 1px solid #000000;
  height: 100%;
  width: 100%;
}
</style>

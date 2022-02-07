<template>
  <div class="error">
    <p>Prišlo je do napake: {{ errorMessage }}</p>
  </div>
</template>

<script>

export default {
  props: {
    errorMessage: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="scss" scoped>
.error {
  color: red;
}
</style>

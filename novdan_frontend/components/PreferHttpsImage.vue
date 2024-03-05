<template>
  <img :src="imageSrc" :alt="alt" @error="onError" />
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      default: null
    },
    alt: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      fallback: false
    }
  },
  computed: {
    imageSrc() {
      if (!this.src || typeof this.src !== 'string') {
        return null
      }
      if (this.fallback) {
        return this.src
      }
      if (this.src.startsWith('https://')) {
        return this.src
      }
      return this.src.replace(/^http:\/\//i, 'https://')
    }
  },
  methods: {
    onError(event) {
      this.fallback = true
    }
  }
}
</script>

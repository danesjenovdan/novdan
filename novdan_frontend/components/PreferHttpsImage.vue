<template>
  <img :src="imageSrc" :alt="alt" @error="onError" />
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      required: true
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
    isSecure() {
      return this.src.startsWith('https://')
    },
    imageSrc() {
      if (this.isSecure || this.fallback) {
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

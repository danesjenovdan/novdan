<template>
  <div>
    <h2>
      <span v-for="(chunk, index) in splitText" :key="index" :class="{'syne': index%2===0, 'murmure': index%2===1}">{{ chunk }}</span>
    </h2>
  </div>
</template>

<script>
export default {
  name: 'SpinningBannerText',
  data () {
    return {
      text: 'Fake news. Fašizem. Pozni kapitalizem. Svoboda govora. Teorije zarote. Politična korektnost. Deep fake. Tribalizem. Mnenjski mehurčki. Kultura zgražanja. Kultura kenslanja. Psyop. Slamnati mož. Propaganda. Laž. Lažna sled.'
    }
  },
  computed: {
    splitText () {
      return this.text.match(/.{1,3}/g)
    }
  }
}
</script>

<style scoped lang="scss">
.murmure {
  font-family: 'wf-le-murmure', serif;
}
</style>

<template>
  <svg viewBox="-0.05 -0.05 2.1 2.1" xmlns="http://www.w3.org/2000/svg">
    <g
      v-for="sector in sectors"
      :key="sector.text"
      :transform="`rotate(${sector.R}, ${sector.L}, ${sector.L})`"
    >
      <path
        :d="`M${sector.L},${sector.L} L${sector.L},0 A${sector.L},${sector.L} 0 ${sector.arcSweep},1 ${sector.X}, ${sector.Y} z`"
      />
      {{ sector }}
      <text
        font-size="0.15"
        x="1"
        y="0.3"
        text-anchor="middle"
        transform-origin="50% 50%"
        :transform="`rotate(${sector.a / 2})`"
      >{{ sector.text }}</text>
    </g>
  </svg>
</template>

<script>
export default {
  name: 'PieChart',
  props: {
    sectionData: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    sectors() {
      let a = 0 // Angle
      let aRad = 0 // Angle in Rad
      let aCalc = 0
      let arcSweep = 0
      let z = 0 // Size z
      let x = 0 // Side x
      let y = 0 // Side y
      let X = 0 // SVG X coordinate
      let Y = 0 // SVG Y coordinate
      let R = 0 // Rotation
      return this.sectionData.map((item) => {
        a = 360 * item.percentage
        if (a === 360) {
          a = 359.999
        }
        aCalc = a > 180 ? 360 - a : a
        aRad = (aCalc * Math.PI) / 180
        z = Math.sqrt(2 - 2 * Math.cos(aRad))
        if (aCalc <= 90) {
          x = Math.sin(aRad)
        } else {
          x = Math.sin(((180 - aCalc) * Math.PI) / 180)
        }
        y = Math.sqrt(z * z - x * x)
        Y = y
        if (a <= 180) {
          X = 1 + x
          arcSweep = 0
        } else {
          X = 1 - x
          arcSweep = 1
        }
        const oldR = R
        R += a
        return {
          class: item.type,
          arcSweep,
          L: 1,
          X,
          Y,
          R: oldR,
          a,
          text: item.user.full_name
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
path {
  fill: transparent;
  stroke: #1103b1;
  stroke-width: 0.03;
}
</style>

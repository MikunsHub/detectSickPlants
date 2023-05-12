<template>
  <Camera @picture-taken="imageSrc = $event"/>
  <img :src="imageSrc" />
</template>

<script>
import Camera from './components/Camera.vue'

export default {
  name: 'App',
  components: {
    Camera
  },
  data() {
    return {
      imageSrc: null
    }
  }
}
</script>

<style>
  
</style>

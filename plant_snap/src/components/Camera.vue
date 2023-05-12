<template>
    <video class="camera-video" ref="video" @canplay="initCanvas()" ></video>
    <canvas style="display:none" ref="canvas"></canvas>
    <div class="modes-container">
        <nav class="modes">
          <button>Pods</button>
          <button>Leaves</button>
          <button>Upload</button>
        </nav>
        <button class="snap-button" @click="takePicture()"></button>
      </div>
</template>

<script>
export default {
    name:"Camera",
    mounted() {
        this.canvas = this.$refs.canvas
        this.video = this.$refs.video
        this.startCapture()
    },
    methods: {
        startCapture() {
            navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
                this.video.srcObject = stream
                this.video.play()
            }).catch(error => {
                console.log(error)
            })
        },
        takePicture() {
            let context = this.canvas.getContext('2d')
            context.drawImage(this.video, 0,0, this.video.videoWidth,this.video.videoHeight)
            this.$emit('picture-taken', this.canvas.toDataURL('img/png'))
        },
        initCanvas() {
            this.canvas.setAttribute('width', this.video.videoWidth)
            this.canvas.setAttribute('height', this.video.videoHeight)
        }
    },
    data(){
        return {
            video: null,
            canvas: null,
        }
    }
}
</script>

<style>
  .camera-video {
    display: block;
    width: 90%;
    height: auto;
    margin: auto;
    padding: 20px;

  }
  .modes-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .modes {
    display: flex;
    justify-content: space-evenly;
    gap: 10px;
  }
  .modes button {
    flex: 1;
    max-width: 100px;
  }
  button .snap-button {
    padding: 20px;
  }
  .snap-button {
    font-size: 50px;
    margin-top: 10px;
    outline: 0;
    border: 1px solid black;
    border-radius: 50%;
    cursor: pointer;
    background-color: white;
    width: 70px;
    height:70px;
  }
</style>
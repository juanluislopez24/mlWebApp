<template>
  <div id="mobilenet">
    <v-container>
      <v-row algin="center" justify="center">
        <v-col></v-col>
        <v-col align-self="center">
          <img id="img" crossOrigin :src="fileData" width=227 height=227 style="display:none"/>
          <v-img
            :style="'display:'+displayImg"
            id="imageToInfer"
            :src="fileData"
            lazy-src="https://picsum.photos/id/11/10/6"
            aspect-ratio="1"
            max-width="500"
            min-width="200"
          ></v-img>
          <video :style="'display:'+display" autoplay playsinline muted id="webcam" width="227" height="227"></video>
        </v-col>

        <v-col>

        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <v-col cols=5>
          <v-file-input
            v-model="file"
            accept="image/png, image/jpeg, image/bmp, image/jpg"
            placeholder="Pick an image to process"
            prepend-icon="mdi-camera"
            label="Image"
            @change="loadFile"
          ></v-file-input>          
        </v-col>
        <v-col cols=5> 
          <v-btn v-if="stop==true" large width=100% color="primary" @click="captureCam">Use Camera</v-btn>
          <v-btn v-else large width=100% color="primary" @click="stop=true">Stop Camera</v-btn>
        </v-col>
      </v-row>
      <!-- <v-row class="mb-6" algin="start" justify="center">
        <v-col cols=1>
          <v-btn :disabled="fileTrue" color="primary" @click="inferImage()">Infer</v-btn>
        </v-col>
      </v-row> -->
      <v-row class="mb-6" algin="start" justify="center">
        <v-col cols=7>
          <v-simple-table>
            <thead>
              <tr>
                <th class="text-left">Class</th>
                <th class="text-left">Probability</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in results" :key="item.className">
                <td>{{ item.className }}</td>
                <td>{{ item.probability }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-col>
      </v-row>
    </v-container>
    

    

    
    
  </div>
</template>

<script>
import * as mobilenet from '@tensorflow-models/mobilenet'
import * as tf from '@tensorflow/tfjs'
// import camera from 'vue-camera'
import { WebCam } from "vue-web-cam";

const NUMBER_OF_CHANNELS = 3

export default {
  name: 'MobileNet',
  data: () => ({
    net:null,
    fileTrue: true,
    file: null,
    stop: true,
    display: 'none',
    displayImg: 'flex',
    fileName: '  .',
    fileData: 'https://66.media.tumblr.com/898419954d6ff3f7b307c8d128db94c6/tumblr_p814cuvBqb1wzvt9qo3_500.gif',
    results: [],
    rules: [
      value => !value || value.size < 2000000 || 'Avatar size should be less than 2 MB!',
    ],
  }),
  methods: {
    loadFile(e){
      // console.log(e)
      var reader = new FileReader();
      reader.onload = (e) => {
        this.fileData = e.target.result
      };
      reader.readAsDataURL(e)
    },

    createMobileNet(){
      mobilenet.load().then((net) => {
        this.net = net
      })
    },

    inferImage(){
      this.stop=true
      if(this.file != null){
        console.log('Loading mobilenet..')
        mobilenet.load().then((net) => {
          console.log('Sucessfully loaded model')
          const imgEl = document.getElementById('img')
          const image = {
            'data': this.fileData,

          }
          net.classify(imgEl).then((result) => {
            console.log(result)
            this.results = result
          })
        })        
      }
    },


    async captureCam(){
      this.stop=false
      const webcamElement = document.getElementById('webcam')
      await this.setupWebcam()
      while (true) {
        const result = await this.net.classify(webcamElement);
        this.results = result
        console.log(result)
        if(this.stop == true){
          break
        }
        await tf.nextFrame();
        
      }
    },
      
    setupWebcam: async() => {
      const webcamElement = document.getElementById('webcam')
      return new Promise((resolve, reject) => {
        const navigatorAny = navigator
        navigator.getUserMedia = navigator.getUserMedia ||
            navigatorAny.webkitGetUserMedia || navigatorAny.mozGetUserMedia ||
            navigatorAny.msGetUserMedia
        if (navigator.getUserMedia) {
          navigator.getUserMedia({video: true},
            stream => {
              webcamElement.srcObject = stream
              webcamElement.addEventListener('loadeddata',  () => resolve(), false)
            },
            error => reject())
        } else {
          reject()
        }
      })
      
    }
  },
  beforeMount(){
    this.createMobileNet()
  },
  components: {
    // camera
    'vue-web-cam': WebCam
  },
  watch: {
    stop: function(val) {
      if(val){
        this.display = 'none'
        this.displayImg = 'flex'
      }
      else{
        this.display = 'inline'
        this.displayImg = 'none'
      }
    },
    file: function (val) {
      this.fileName = this.file.name
      console.log(this.file)
      if(val != null){
        this.fileTrue = false
        
      }
      else{
        this.fileTrue = true
      }
      
    },
    fileData: function (val){
      console.log(val)
      this.inferImage()
    }
  }
};
</script>

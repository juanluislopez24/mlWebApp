<template>
  <div id="mobilenet">
    <img id="img" crossOrigin :src="fileData" width=227 height=227 style="display:none"/>
    <v-container>
      <v-row align="start" justify="center">
        <v-col cols="5">
          <v-img
            :style="'display:'+displayImg"
            id="imageToInfer"
            :src="fileData"
            lazy-src="https://picsum.photos/id/11/10/6"
            max-height="300px"
            max-width="500px"
            min-height="300px"
            min-width="500px"
          ></v-img>
          <video :style="'display:'+display" autoplay playsinline muted id="webcam" width="500" height="300"></video>
          <video style="display:none" autoplay playsinline muted id="webcam" width="227" height="227" ></video>
          <!-- <img id="webcamimg" crossOrigin :src="fileData" width=227 height=227 style="display:none"/> -->
        </v-col>

        <v-col cols="5">
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
      <v-row align="center" justify="center">
        <v-col cols="5">
          <v-file-input
            v-model="file"
            accept="image/png, image/jpeg, image/bmp, image/jpg"
            placeholder="Pick an image to process"
            prepend-icon="mdi-camera"
            label="Image"
            @change="loadFile"
          ></v-file-input>          
        </v-col>
        <v-col cols="5"> 
          <v-btn v-if="stop==true" large width=100% color="primary" @click="captureCam">Use Camera</v-btn>
          <v-btn v-else large width=100% color="primary" @click="stop=true">Stop Camera</v-btn>
        </v-col>
      </v-row>
      <!-- <v-row class="mb-6" algin="start" justify="center">
        <v-col cols=1>
          <v-btn :disabled="fileTrue" color="primary" @click="inferImage()">Infer</v-btn>
        </v-col>
      </v-row> -->
      <v-row align="start" justify="center">
        <v-col cols="2">
          <v-switch v-model="knn" label="Activate Knn"></v-switch>
        </v-col>
        <v-col cols=5>
          <v-text-field
            :disabled="!knn"
            label="New Class"
            v-model="newClass"
            placeholder="Type your new class to train..."
            outlined
          ></v-text-field>
        </v-col>
        <v-col cols="3">
          <v-btn :disabled="!knn" color="primary" width=100% large @click="addExample()">Train</v-btn>
        </v-col>
      </v-row>
      
    </v-container>
    

    

    
    
  </div>
</template>

<script>
import * as mobilenet from '@tensorflow-models/mobilenet'
import * as knnClassifier from '@tensorflow-models/knn-classifier'
import * as tf from '@tensorflow/tfjs'
// import camera from 'vue-camera'
import { WebCam } from "vue-web-cam";

const NUMBER_OF_CHANNELS = 3

export default {
  name: 'MobileNet',
  data: () => ({
    newClass: '',
    net:null,
    classifier: knnClassifier.create(),
    fileTrue: true,
    file: null,
    stop: true,
    knn: false,
    display: 'none',
    displayImg: 'flex',
    fileName: '  .',
    classes:[],
    fileData: 'https://t2.rbxcdn.com/d7326f4e0a63faf7aaa4080900380614',
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

    addExample() {
      console.log()
      let activation
      if(this.newClass != '' || this.newClass != null){
        if(stop == true){
          activation = this.net.infer(document.getElementById('img'), 'conv_preds')
        }
        else{
          activation = this.net.infer(document.getElementById('webcam'), 'conv_preds')
        }
        this.classifier.addExample(activation, this.newClass)
        console.log('added')
      }
    },

    async inferImage(){
      this.stop=true
      if(this.file != null){
        const result = await this.classify(document.getElementById('img'))
        this.results = result
        // console.log(result)
        // mobilenet.load().then((net) => {
        //   console.log('Sucessfully loaded model')
        //   const imgEl = document.getElementById('img')
        //   net.classify(imgEl).then((result) => {
        //     console.log(result)
        //     this.results = result
        //   })
        // })        
      }
    },


    async captureCam(){
      this.stop=false
      const webcamElement = document.getElementById('webcam')
      await this.setupWebcam()
      while (true) {
        this.fileDataVid = webcamElement.src
        // use mobilenet
        // const result = await this.net.classify(webcamElement);

        // use knn
        // const activation = net.infer(webcamElement, 'conv_preds')
        // const result = await this.classifier.predictClass(activation)
        const result = await this.classify(webcamElement)

        this.results = result
        console.log(result)
    
        if(this.stop == true){
          break
        }
        await tf.nextFrame();
        
      }
    },

    async classify(img){
      if(this.knn == true){
        if(this.classifier.getNumClasses() > 0){
          const activation = this.net.infer(img, 'conv_preds')
          const result = await this.classifier.predictClass(activation)
          var res = result.confidences
          var response = []

          for (var key in res) {
            console.log(key, res[key]);
            var obj = {"className": key, "probability": res[key]}
            response.push(obj)
          }
          console.log(response)
          return response
        }
        return []
      }
      else{
        // use standard mobilenet
        const result = await this.net.classify(img)
        return result
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
      // console.log(this.file)
      if(val != null){
        this.fileTrue = false
        
      }
      else{
        this.fileTrue = true
      }
      
    },
    fileData: function (val){
      // console.log(val)
      this.inferImage()
    }
  }
};
</script>

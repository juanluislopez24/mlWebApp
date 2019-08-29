<template>
  <div id="mobilenet">
    <v-container>
      <v-row algin="start" justify="center">
        <v-col></v-col>
        <v-col align-self="center">
          <img id="img" crossOrigin :src="fileData" width=227 height=227 style="display:none"/>
          <v-img
            id="imageToInfer"
            :src="fileData"
            lazy-src="https://picsum.photos/id/11/10/6"
            aspect-ratio="1"
            max-width="500"
            min-width="200"
          ></v-img>
        </v-col>
        <v-col></v-col>
      </v-row>
      <v-row algin="start" justify="center">
        <v-col md=5 lg=8>
          <v-file-input
            v-model="file"
            accept="image/png, image/jpeg, image/bmp, image/jpg"
            placeholder="Pick an image to process"
            prepend-icon="mdi-camera"
            label="Image"
            @change="loadFile"
          ></v-file-input>
          <!-- <p>{{ fileName }}</p> -->
          
        </v-col>
      </v-row>
      <v-row class="mb-6" algin="start" justify="center">
        <v-col cols=1>
          <v-btn :disabled="fileTrue" color="primary" @click="inferImage()">Infer</v-btn>
        </v-col>
      </v-row>
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

const NUMBER_OF_CHANNELS = 3

export default {
  name: 'MobileNet',
  data: () => ({
    fileTrue: true,
    file: null,
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
    inferImage(){
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
    }
  },
  components: {
    
  },
  watch: {
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
    }
  }
};
</script>

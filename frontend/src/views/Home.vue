<template>
  <v-container>
    <v-row algin="start" justify="center">
      <v-col
          v-for="card in cards"
          :key="card.title"
          :cols="cards.length"
        >
        <v-card hover :to="card.route">
          <v-img
            :src="card.src"
            class="white--text"
            height="200px"
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          >
            <v-card-title
              class="fill-height align-end"
              v-text="card.title"
            ></v-card-title>
          </v-img>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  data: () => ({
    cards: [
      { title: 'MobileNet', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 3, route: 'mobilenet'},
      { title: 'YOLO', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 3, route: 'yolo' },
      { title: 'DCGAN', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 3, route: 'dcgan' },
    ],
  }),
  components: {
  },
};
</script>

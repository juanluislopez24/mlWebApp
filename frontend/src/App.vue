<template>
  <v-app>
    <v-navigation-drawer app temporary v-model="drawer">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Models
          </v-list-item-title>
          <v-list-item-subtitle>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.route"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar dark app elevate-on-scroll color='primary'>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="headline text-uppercase" @click="$router.push('/')">
        Juan's ML webpage
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-menu
        left
        bottom
      >
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="n in 5"
            :key="n"
            @click="() => {}"
          >
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-content>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-content>

    <v-footer app padless>
      <v-card
      class="flex"
      flat
      tile
    >
        <v-card-title class="">
          <strong class="subheading">Lets talk!</strong>

          <div class="flex-grow-1"></div>

          <v-btn
            v-for="item in socialMedia"
            :key="item.icon"
            class="mx-4"
            icon
            :href="item.link"
          >
            <v-icon size="24px">{{ item.icon }}</v-icon>
          </v-btn>
        </v-card-title>
      </v-card>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    items: [
      { title: 'MobileNet', route:'mobilenet',  icon: 'mdi-view-dashboard' },
      { title: 'YOLO',route:'yolo', icon: 'mdi-image' },
      { title: 'DCGAN',route:'dcgan', icon: 'mdi-help-box' },
    ],
    right: null,
    socialMedia: [
      {icon: 'mdi-linkedin', link: 'https://linkedin.com/in/juanluislopez24'},
      {icon: 'mdi-github-circle', link: 'https://github.com/juanluislopez24'},
    ],
    icons: [
        'mdi-linkedin',
        'mdi-github-circle',
        'mdi-email',
        'mdi-airplane',
      ],
    drawer: false
  }),
};
</script>

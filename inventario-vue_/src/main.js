import { ApolloClient, InMemoryCache } from '@apollo/client/core'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { createApp } from 'vue'
import App from './App.vue'

const apolloClient = new ApolloClient({
  uri: 'http://localhost:5000/graphql',
  cache: new InMemoryCache()
})

const app = createApp(App)
app.provide(DefaultApolloClient, apolloClient)
app.mount('#app')
import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import router from './router';
import $ from 'jquery';


window.jQuery = $;

const app = createApp(App);

app.use(router);

app.mount('#app');

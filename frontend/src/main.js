import { createApp } from "vue";
import ElementPlus from "element-plus";
import { BootstrapVue3, IconsPlugin } from 'bootstrap-vue-3';
import App from "./App.vue";
import router from "./router";

import 'bootstrap/dist/css/bootstrap.css';
import 'element-plus/dist/index.css';

const app = createApp(App);

app.use(ElementPlus);
app.use(BootstrapVue3);
app.use(IconsPlugin);
app.use(router);

app.mount("#app");

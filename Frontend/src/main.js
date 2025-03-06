import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// Vue-toast
// import ToastPlugin from 'vue-toast-notification';
import VueToast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';
// Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App)
// app.use(ToastPlugin);
app.use(VueToast, {
    // One of the options
    position: 'top'
})
app.use(router)

app.mount('#app')

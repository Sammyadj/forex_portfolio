import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TradingView from '@/views/TradingView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/trade',
    name: 'trade',
    component: TradingView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('access_token');
  const goingToLoginPage = to.name === 'login' || to.name === 'register';

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if trying to access a protected route without being authenticated
    next({ name: 'login' });
  } else if (isAuthenticated && goingToLoginPage) {
    // Prevent going to the login or register page if already authenticated
    next({ name: 'dashboard' });
  } else {
    // Proceed as normal for any other case
    next();
  }
});

// router.beforeEach((to, from, next) => {
//   console.log('Navigating to:', to.name);
//   const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
//   const isAuthenticated = localStorage.getItem('access_token');
//   console.log('Requires Auth:', requiresAuth);
//   console.log('Is Authenticated:', isAuthenticated);

//   if (requiresAuth && !isAuthenticated) {
//     console.log('Redirecting to Login...');
//     next({ name: 'login' });
//   } else {
//     next();
//   }
// });


export default router

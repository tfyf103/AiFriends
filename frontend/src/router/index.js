import { createRouter, createWebHistory } from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import ProfileIndex from "@/views/profile/ProfileIndex.vue";
// 补上缺失导入
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomepageIndex,
      name: 'homepage-index',
    },
    {
      path: '/user/profile',
      component: ProfileIndex,
      name: 'user-profile-index',
    },
    {
      path: '/user/space/:user_id',
      component: SpaceIndex,
      name: 'user-space-index',
    },
    {
      path: '/user/account/register',
      component: RegisterIndex,
      name: 'user-account-register-index',
    },
    {
      path: '/user/account/login',
      component: LoginIndex,
      name: 'user-account-login-index',
    },
    {
      path: '/friend',
      component: FriendIndex,
      name: 'friend-index',
    },
    {
      path: '/create',
      component: CreateIndex,
      name: 'create-index',
    },
    {
      path: '/404',
      component: NotFoundIndex,
      name: '404',
    },
    // 兜底404固定最后
    {
      path: '/:pathMatch(.*)*',
      component: NotFoundIndex,
      name: 'not-found',
    },
  ],
})

export default router
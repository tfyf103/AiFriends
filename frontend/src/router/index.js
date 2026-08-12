import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user.js'

// Route-level lazy loading keeps profile/create/edit dependencies out of the initial
// homepage bundle. The previous eager imports forced every page into index.js even
// when a visitor only opened the public Character discovery route.
const HomepageIndex = () => import('@/views/homepage/HomepageIndex.vue')
const FriendIndex = () => import('@/views/friend/FriendIndex.vue')
const NotFoundIndex = () => import('@/views/error/NotFoundIndex.vue')
const LoginIndex = () => import('@/views/user/account/LoginIndex.vue')
const RegisterIndex = () => import('@/views/user/account/RegisterIndex.vue')
const ProfileIndex = () => import('@/views/user/profile/ProfileIndex.vue')
const SpaceIndex = () => import('@/views/user/space/SpaceIndex.vue')
const CreateIndex = () => import('@/views/create/CreateIndex.vue')
const UpdateCharacter = () => import('@/views/create/character/UpdateCharacter.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomepageIndex,
      name: 'homepage-index',
      meta: { needLogin: false },
    },
    {
      path: '/user/profile',
      component: ProfileIndex,
      name: 'user-profile-index',
      meta: { needLogin: true },
    },
    {
      path: '/user/space/:user_id',
      component: SpaceIndex,
      name: 'user-space-index',
      meta: { needLogin: false },
    },
    {
      path: '/user/account/register',
      component: RegisterIndex,
      name: 'user-account-register-index',
      meta: { needLogin: false },
    },
    {
      path: '/user/account/login',
      component: LoginIndex,
      name: 'user-account-login-index',
      meta: { needLogin: false },
    },
    {
      path: '/friend',
      component: FriendIndex,
      name: 'friend-index',
      meta: { needLogin: true },
    },
    {
      path: '/create',
      component: CreateIndex,
      name: 'create-index',
      meta: { needLogin: true },
    },
    {
      path: '/create/character/update/:character_id/',
      component: UpdateCharacter,
      name: 'update-character',
      meta: { needLogin: true },
    },
    {
      path: '/404',
      component: NotFoundIndex,
      name: '404',
      meta: { needLogin: false },
    },
    {
      path: '/:pathMatch(.*)*',
      component: NotFoundIndex,
      name: 'not-found',
      meta: { needLogin: false },
    },
  ],
})

router.beforeEach((to) => {
  const user = useUserStore()
  if (to.meta.needLogin && user.hasPulledUserInfo && !user.isLogin()) {
    return { name: 'user-account-login-index' }
  }
  return true
})

export default router

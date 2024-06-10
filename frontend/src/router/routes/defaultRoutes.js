import MainPageDashboard from "@/layout/dashboard/MainDashboard.vue";

const MainSearchPage = () => import("@/views/MainSearchPage.vue");
const ProfilePage = () => import("@/views/account/ProfilePage.vue");

const defaultRoutes = [
  {
    path: "",
    component: MainPageDashboard,
    children: [
      {
        path: "",
        name: "main",
        component: MainSearchPage,
      },
    ]
  },
  {
    path: "profile/:nickname",
    component: MainPageDashboard,
    children: [
      {
        path: "",
        name: "profile",
        component: ProfilePage,
      },
    ],
  },
]

export default defaultRoutes;
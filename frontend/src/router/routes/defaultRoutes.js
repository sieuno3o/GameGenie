import MainPageDashboard from "@/layout/dashboard/MainDashboard.vue";

const MainSearchPage = () => import("@/views/MainSearchPage.vue");

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
]

export default defaultRoutes;
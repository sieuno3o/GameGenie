import MainPageDashboard from "@/layout/dashboard/MainDashboard.vue";
import DefaultDashboard from "@/layout/dashboard/DefaultDashboard.vue";

const MainSearchPage = () => import("@/views/MainSearchPage.vue");
const RecommendPage = () => import("@/views/RecommendPage.vue");

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
    path: "recommend",
    component: DefaultDashboard,
    children: [
      {
        path: "",
        name: "recommend",
        component: RecommendPage,
      },
    ]
  }
]

export default defaultRoutes;
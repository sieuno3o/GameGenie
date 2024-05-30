import MainPageDashboard from "@/layout/dashboard/MainDashboard.vue";

const RecommendPage = () => import("@/views/RecommendPage.vue");

const recommendationsRoutes = [
  {
    path: "",
    component: MainPageDashboard,
    children: [
      {
        path: "",
        name: "recommends",
        component: RecommendPage,
      },
    ],
  },
];

export default recommendationsRoutes;
